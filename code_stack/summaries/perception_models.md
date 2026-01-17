# Perception Encoder (PE) Codebase Analysis

**Repository**: `github.com/facebookresearch/perception_models`
**Analyzed**: 2026-01-16
**Purpose**: Understanding temporal handling for IDEA-003 investigation

## Executive Summary

PE's video encoding has **NO temporal modeling whatsoever**. Frames are encoded independently with identical position encodings, then simply averaged. This confirms that any temporal information preserved must come from implicit signals in the visual content itself.

## Video Encoding Pipeline

### `CLIP.encode_video` (pe.py:717-723)

```python
def encode_video(self, video, normalize: bool = False): # b n c h w
    b, n, c, h, w = video.shape
    frms = video.reshape(b * n, c, h, w)
    frm_feats = self.encode_image(frms, normalize=normalize)  # Independent encoding!
    video_feats = frm_feats.reshape(b, n, -1)
    video_feats = video_feats.mean(dim=1)  # Pure average pooling
    return video_feats
```

**Key observations**:
1. Frames are reshaped into batch dimension and encoded as independent images
2. No cross-frame attention or temporal modeling
3. Final pooling is simple arithmetic mean
4. No temporal position information is injected

## Position Encoding: RoPE 2D

### `Rope2D` class (rope.py:303-348)

RoPE is applied **per-frame** with purely spatial (2D) coordinates:

```python
def update_grid(self, device, grid_h, grid_w):
    # Grid is (patch_x, patch_y) only - NO frame index
    freqs_y = self.rope(grid_y_range)[:, None].expand(grid_h, grid_w, -1)
    freqs_x = self.rope(grid_x_range)[None, :].expand(grid_h, grid_w, -1)
    freq = torch.cat([freqs_x, freqs_y], dim=-1).reshape(grid_h * grid_w, -1)
```

**Critical finding**: Frames 1 through N receive **identical** position encodings. There is no temporal dimension in the RoPE implementation.

## Frame Sampling

### `VideoTransform.load_video` (video_transform.py:79-130)

- Uses `torchcodec.VideoDecoder` for frame extraction
- Uniform sampling based on `sampling_fps` and `max_frames`
- No temporal augmentation beyond sampling strategy

## Implications for IDEA-003

### H3 (Position Encoding Signal): **REFUTED**
- No temporal position encoding exists in PE
- RoPE is purely 2D spatial
- This cannot explain average pooling's effectiveness

### H2 (Implicit Temporal Encoding): **PRIMARY HYPOTHESIS**
- The only possible explanation for temporal awareness
- Visual content must encode temporal information:
  - Motion blur patterns
  - Object positions/states
  - Mid-action poses
  - Scene progression indicators

### Next Steps
1. **Frame Order Probe** (Exp 1.2): Can we predict frame order from embeddings?
2. **Temporal Feature Analysis**: Which embedding dimensions vary systematically across frames?
3. **Frame Shuffle Test** (Exp 1.3): Baseline for H1 benchmark artifact hypothesis

## Model Architecture Notes

### VisionTransformer Configuration
- Uses attention pooling by default (`pool_type="attn"`)
- Supports RoPE 2D (`use_rope2d=True`)
- Optional absolute position embeddings (`use_abs_posemb=True`)
- Output projection to 1280-d embedding space

### Key Files
- `core/vision_encoder/pe.py`: Main encoder, CLIP model
- `core/vision_encoder/rope.py`: RoPE 2D implementation
- `core/transforms/video_transform.py`: Video loading and preprocessing
- `core/vision_encoder/config.py`: Model configurations
