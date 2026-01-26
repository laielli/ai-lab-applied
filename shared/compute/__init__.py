"""
ComputeTarget abstraction for experiment execution.

Provides a unified interface for running experiments on local or remote compute.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional
import json
import os
import subprocess
import time


class ExecutionStatus(Enum):
    """Status of an experiment execution."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ExecutionResult:
    """Result of an experiment execution."""
    status: ExecutionStatus
    return_code: int
    stdout: str
    stderr: str
    duration_seconds: float
    artifacts_path: Optional[Path] = None
    metrics: Optional[dict] = None

    def to_dict(self) -> dict:
        return {
            "status": self.status.value,
            "return_code": self.return_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "duration_seconds": self.duration_seconds,
            "artifacts_path": str(self.artifacts_path) if self.artifacts_path else None,
            "metrics": self.metrics
        }


class ComputeTarget(ABC):
    """Abstract base class for compute targets."""

    @abstractmethod
    def run(self, script: str, config: dict, work_dir: Path) -> ExecutionResult:
        """
        Execute a script on this compute target.

        Args:
            script: Path to the Python script or module to run
            config: Configuration dictionary for the experiment
            work_dir: Working directory for the experiment

        Returns:
            ExecutionResult with status, outputs, and artifacts
        """
        pass

    @abstractmethod
    def get_status(self) -> str:
        """Get the current status of this compute target."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this compute target is available for use."""
        pass

    @abstractmethod
    def get_capabilities(self) -> dict:
        """Return capabilities of this compute target."""
        pass


class LocalCPU(ComputeTarget):
    """Run experiments on local machine, CPU only."""

    def __init__(self, timeout_hours: float = 8.0):
        self.timeout_hours = timeout_hours

    def run(self, script: str, config: dict, work_dir: Path) -> ExecutionResult:
        """Run script on local CPU."""
        start_time = time.time()

        # Write config to temp file
        config_path = work_dir / "config_run.yaml"
        import yaml
        with open(config_path, "w") as f:
            yaml.safe_dump(config, f)

        # Build command
        cmd = [
            "python", "-m", script,
            "--config", str(config_path),
            "--device", "cpu"
        ]

        try:
            result = subprocess.run(
                cmd,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=self.timeout_hours * 3600,
                env={**os.environ, "CUDA_VISIBLE_DEVICES": ""}
            )

            duration = time.time() - start_time
            status = ExecutionStatus.COMPLETED if result.returncode == 0 else ExecutionStatus.FAILED

            return ExecutionResult(
                status=status,
                return_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                duration_seconds=duration,
                artifacts_path=work_dir / "results"
            )

        except subprocess.TimeoutExpired as e:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                return_code=-1,
                stdout=e.stdout or "",
                stderr=f"Timeout after {self.timeout_hours} hours",
                duration_seconds=self.timeout_hours * 3600
            )
        except Exception as e:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                return_code=-1,
                stdout="",
                stderr=str(e),
                duration_seconds=time.time() - start_time
            )

    def get_status(self) -> str:
        return "available"

    def is_available(self) -> bool:
        return True

    def get_capabilities(self) -> dict:
        return {
            "type": "local_cpu",
            "gpu": False,
            "gpu_memory_gb": 0,
            "max_runtime_hours": self.timeout_hours
        }


class LocalGPU(ComputeTarget):
    """Run experiments on local machine with GPU (MPS for Apple Silicon)."""

    def __init__(self, timeout_hours: float = 8.0):
        self.timeout_hours = timeout_hours
        self._detect_gpu_type()

    def _detect_gpu_type(self):
        """Detect available GPU type."""
        import platform

        self.gpu_type = "none"
        self.gpu_memory_gb = 0

        if platform.system() == "Darwin" and platform.processor() == "arm":
            # Apple Silicon - use MPS
            self.gpu_type = "mps"
            self.gpu_memory_gb = 16  # Conservative estimate for unified memory
            self.device = "mps"
        else:
            # Try CUDA
            try:
                result = subprocess.run(
                    ["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    self.gpu_type = "cuda"
                    self.gpu_memory_gb = int(result.stdout.strip().split("\n")[0]) / 1024
                    self.device = "cuda"
            except FileNotFoundError:
                pass

    def run(self, script: str, config: dict, work_dir: Path) -> ExecutionResult:
        """Run script on local GPU."""
        if not self.is_available():
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                return_code=-1,
                stdout="",
                stderr="No GPU available",
                duration_seconds=0
            )

        start_time = time.time()

        # Write config to temp file
        config_path = work_dir / "config_run.yaml"
        import yaml
        with open(config_path, "w") as f:
            yaml.safe_dump(config, f)

        # Build command
        cmd = [
            "python", "-m", script,
            "--config", str(config_path),
            "--device", self.device
        ]

        try:
            result = subprocess.run(
                cmd,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=self.timeout_hours * 3600
            )

            duration = time.time() - start_time
            status = ExecutionStatus.COMPLETED if result.returncode == 0 else ExecutionStatus.FAILED

            return ExecutionResult(
                status=status,
                return_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                duration_seconds=duration,
                artifacts_path=work_dir / "results"
            )

        except subprocess.TimeoutExpired as e:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                return_code=-1,
                stdout=e.stdout or "",
                stderr=f"Timeout after {self.timeout_hours} hours",
                duration_seconds=self.timeout_hours * 3600
            )
        except Exception as e:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                return_code=-1,
                stdout="",
                stderr=str(e),
                duration_seconds=time.time() - start_time
            )

    def get_status(self) -> str:
        return "available" if self.is_available() else "unavailable"

    def is_available(self) -> bool:
        return self.gpu_type != "none"

    def get_capabilities(self) -> dict:
        return {
            "type": "local_gpu",
            "gpu": self.is_available(),
            "gpu_type": self.gpu_type,
            "gpu_memory_gb": self.gpu_memory_gb,
            "max_runtime_hours": self.timeout_hours
        }


class LambdaCloudClient:
    """Client for Lambda Labs Cloud API."""

    API_BASE = "https://cloud.lambdalabs.com/api/v1"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("LAMBDA_API_KEY")
        if not self.api_key:
            raise ValueError("LAMBDA_API_KEY not set in environment")

    def _request(self, method: str, endpoint: str, data: Optional[dict] = None) -> dict:
        """Make authenticated API request."""
        import urllib.request
        import urllib.error

        url = f"{self.API_BASE}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=body, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if e.fp else ""
            raise RuntimeError(f"Lambda API error {e.code}: {error_body}")

    def list_instances(self) -> list:
        """List all active instances."""
        response = self._request("GET", "instances")
        return response.get("data", [])

    def list_instance_types(self) -> list:
        """List available instance types with availability."""
        response = self._request("GET", "instance-types")
        return response.get("data", {})

    def launch(
        self,
        instance_type: str = "gpu_1x_a10",
        region: str = "us-east-1",
        ssh_key_names: Optional[list] = None,
        name: Optional[str] = None
    ) -> dict:
        """
        Launch a new instance.

        Args:
            instance_type: Instance type (e.g., "gpu_1x_a10", "gpu_1x_a100_sxm4")
            region: Region name
            ssh_key_names: List of SSH key names to add
            name: Optional instance name

        Returns:
            Instance details including id and ip
        """
        data = {
            "instance_type_name": instance_type,
            "region_name": region,
        }
        if ssh_key_names:
            data["ssh_key_names"] = ssh_key_names
        if name:
            data["name"] = name

        response = self._request("POST", "instance-operations/launch", data)
        instances = response.get("data", {}).get("instance_ids", [])

        if not instances:
            raise RuntimeError("No instance launched")

        return {"instance_id": instances[0]}

    def terminate(self, instance_ids: list) -> dict:
        """Terminate instances by ID."""
        data = {"instance_ids": instance_ids}
        return self._request("POST", "instance-operations/terminate", data)

    def get_instance(self, instance_id: str) -> dict:
        """Get instance details by ID."""
        response = self._request("GET", f"instances/{instance_id}")
        return response.get("data", {})

    def wait_for_ready(self, instance_id: str, timeout_seconds: int = 600) -> dict:
        """Wait for instance to be ready (SSH available)."""
        start = time.time()
        while time.time() - start < timeout_seconds:
            instance = self.get_instance(instance_id)
            if instance.get("status") == "active":
                return instance
            elif instance.get("status") in ("terminated", "failed"):
                raise RuntimeError(f"Instance entered {instance['status']} state")
            time.sleep(10)
        raise TimeoutError(f"Instance not ready after {timeout_seconds}s")


class RemoteLambda(ComputeTarget):
    """Run experiments on Lambda.ai cloud instance."""

    # Map simple names to Lambda instance types
    GPU_TYPE_MAP = {
        "A10": "gpu_1x_a10",
        "A10G": "gpu_1x_a10",
        "A100": "gpu_1x_a100_sxm4",
        "A100-80GB": "gpu_1x_a100_sxm4",
        "H100": "gpu_1x_h100_pcie",
    }

    def __init__(
        self,
        gpu_type: str = "A10",
        region: str = "us-east-1",
        ssh_key_name: Optional[str] = None
    ):
        self.gpu_type = gpu_type
        self.region = region
        self.ssh_key_name = ssh_key_name or os.environ.get("LAMBDA_SSH_KEY_NAME")
        self.instance_type = self.GPU_TYPE_MAP.get(gpu_type, gpu_type)

        # Initialize client (will fail if no API key)
        try:
            self.client = LambdaCloudClient()
        except ValueError:
            self.client = None

    def run(self, script: str, config: dict, work_dir: Path) -> ExecutionResult:
        """Run script on remote Lambda instance."""
        if not self.is_available():
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                return_code=-1,
                stdout="",
                stderr="Lambda API key not configured",
                duration_seconds=0
            )

        start_time = time.time()
        instance_id = None

        try:
            # 1. Launch instance
            ssh_keys = [self.ssh_key_name] if self.ssh_key_name else None
            launch_result = self.client.launch(
                instance_type=self.instance_type,
                region=self.region,
                ssh_key_names=ssh_keys,
                name=f"exp-{script.replace('.', '-')}"
            )
            instance_id = launch_result["instance_id"]

            # 2. Wait for ready
            instance = self.client.wait_for_ready(instance_id)
            ip_address = instance.get("ip")

            if not ip_address:
                raise RuntimeError("No IP address assigned to instance")

            # 3. Upload code
            self._upload_code(ip_address, work_dir)

            # 4. Write config and execute
            import yaml
            config_yaml = yaml.safe_dump(config)
            self._execute_remote(ip_address, script, config_yaml, work_dir)

            # 5. Download results
            results_path = work_dir / "results"
            self._download_results(ip_address, results_path)

            duration = time.time() - start_time

            return ExecutionResult(
                status=ExecutionStatus.COMPLETED,
                return_code=0,
                stdout=f"Experiment completed on Lambda {self.gpu_type}",
                stderr="",
                duration_seconds=duration,
                artifacts_path=results_path
            )

        except Exception as e:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                return_code=-1,
                stdout="",
                stderr=str(e),
                duration_seconds=time.time() - start_time
            )
        finally:
            # Always terminate instance
            if instance_id and self.client:
                try:
                    self.client.terminate([instance_id])
                except Exception:
                    pass  # Best effort cleanup

    def _upload_code(self, ip: str, work_dir: Path):
        """Upload code to remote instance via rsync."""
        cmd = [
            "rsync", "-avz", "--progress",
            "-e", "ssh -o StrictHostKeyChecking=no",
            f"{work_dir}/",
            f"ubuntu@{ip}:~/experiment/"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode != 0:
            raise RuntimeError(f"Upload failed: {result.stderr}")

    def _execute_remote(self, ip: str, script: str, config_yaml: str, work_dir: Path):
        """Execute script on remote instance."""
        # Create a script to run remotely
        remote_script = f"""
cd ~/experiment
echo '{config_yaml}' > config_run.yaml
python -m {script} --config config_run.yaml
"""
        cmd = [
            "ssh", "-o", "StrictHostKeyChecking=no",
            f"ubuntu@{ip}",
            remote_script
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600 * 24)
        if result.returncode != 0:
            raise RuntimeError(f"Execution failed: {result.stderr}")

    def _download_results(self, ip: str, results_path: Path):
        """Download results from remote instance."""
        results_path.mkdir(parents=True, exist_ok=True)
        cmd = [
            "rsync", "-avz", "--progress",
            "-e", "ssh -o StrictHostKeyChecking=no",
            f"ubuntu@{ip}:~/experiment/results/",
            f"{results_path}/"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode != 0:
            raise RuntimeError(f"Download failed: {result.stderr}")

    def get_status(self) -> str:
        if not self.client:
            return "not_configured"
        try:
            instances = self.client.list_instances()
            return f"{len(instances)} active instances"
        except Exception as e:
            return f"error: {e}"

    def is_available(self) -> bool:
        return self.client is not None

    def get_capabilities(self) -> dict:
        return {
            "type": "remote_lambda",
            "gpu": True,
            "gpu_type": self.gpu_type,
            "instance_type": self.instance_type,
            "region": self.region
        }


def select_target(spec: dict) -> ComputeTarget:
    """
    Auto-select compute target based on experiment spec requirements.

    Args:
        spec: Experiment spec with compute requirements

    Returns:
        Appropriate ComputeTarget instance
    """
    # Extract requirements from spec
    compute_budget = spec.get("compute_budget", {})
    gpu_hours = compute_budget.get("gpu_hours", 0)
    requires_gpu = compute_budget.get("requires_gpu", False)
    memory_gb = compute_budget.get("memory_gb", 0)

    # CPU-only experiments
    if not requires_gpu:
        return LocalCPU()

    # Check local GPU availability
    local_gpu = LocalGPU()
    if local_gpu.is_available():
        caps = local_gpu.get_capabilities()

        # If local GPU has enough memory and runtime is short
        if caps["gpu_memory_gb"] >= memory_gb and gpu_hours <= 2:
            return local_gpu

    # Default to remote for larger experiments
    if gpu_hours > 2 or memory_gb > 16:
        return RemoteLambda(gpu_type="A10" if memory_gb <= 24 else "A100")

    # Fallback to local GPU if available
    if local_gpu.is_available():
        return local_gpu

    # Last resort: local CPU
    return LocalCPU()


# Convenience exports
__all__ = [
    "ComputeTarget",
    "LocalCPU",
    "LocalGPU",
    "RemoteLambda",
    "LambdaCloudClient",
    "ExecutionResult",
    "ExecutionStatus",
    "select_target"
]
