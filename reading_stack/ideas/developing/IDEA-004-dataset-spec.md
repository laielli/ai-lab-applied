# TinyVid Dataset Specification v0.1

## Overview

| Property | Value |
|----------|-------|
| Name | TinyVid |
| Version | 0.1 (draft) |
| Total clips | 10,000 - 20,000 |
| Resolution | 64×64 pixels |
| Frame rate | 8 fps (stored) |
| Frames per clip | 16 frames (2 seconds) |
| Format | MP4 (H.264) or NPY arrays |
| Total size | <500MB |

---

## Part A: TinyVid-Syn (Synthetic)

### Generation Framework

```
Canvas: 64×64 RGB
Background: Solid color (random or fixed)
Objects: 2-4 simple shapes
Actions: Predefined motion primitives
Duration: 16 frames
```

### Object Vocabulary

| Category | Objects |
|----------|---------|
| Shapes | circle, square, triangle, star, pentagon |
| Colors | red, blue, green, yellow, orange, purple, white |
| Sizes | small (8px), medium (16px), large (24px) |

**Total objects**: 5 shapes × 7 colors × 3 sizes = 105 object types

### Action Vocabulary (Temporal Primitives)

| Action | Parameters | Temporal Signature |
|--------|------------|-------------------|
| `move_left` | speed | x decreases over time |
| `move_right` | speed | x increases over time |
| `move_up` | speed | y decreases over time |
| `move_down` | speed | y increases over time |
| `move_diagonal` | angle, speed | x,y change together |
| `rotate_cw` | speed | angle increases |
| `rotate_ccw` | speed | angle decreases |
| `grow` | rate | size increases |
| `shrink` | rate | size decreases |
| `appear` | frame | opacity 0→1 |
| `disappear` | frame | opacity 1→0 |
| `bounce` | axis | reverses direction |
| `orbit` | center, radius | circular path |
| `zigzag` | amplitude | alternating direction |

### Compositional Templates

**Single object, single action**:
```
"{color} {shape} {action}"
→ "red circle moves left"
→ "blue square rotates clockwise"
```

**Single object, sequential actions**:
```
"{color} {shape} {action1} then {action2}"
→ "red circle moves left then moves up"
→ "green triangle grows then shrinks"
```

**Two objects, parallel actions**:
```
"{color1} {shape1} {action1} while {color2} {shape2} {action2}"
→ "red circle moves left while blue square moves right"
```

**Two objects, interaction**:
```
"{color1} {shape1} {action} toward {color2} {shape2}"
→ "red circle moves toward blue square"
```

### Hard Negatives

Critical for learning temporal features:

| Positive | Hard Negative | Difference |
|----------|---------------|------------|
| "circle moves left" | "circle moves right" | Direction |
| "circle moves then stops" | "circle stops then moves" | Order |
| "circle appears then disappears" | "circle disappears then appears" | Order |
| "A moves toward B" | "A moves away from B" | Relation |
| "A grows while B shrinks" | "A shrinks while B grows" | Swap |

### Generation Statistics

```
Single actions: 105 objects × 14 actions = 1,470
Sequential (2): 105 × 14 × 14 = 20,580
Parallel (2 obj): 105 × 105 × 14 × 14 / 2 = ~1M (sample 5K)
Interactions: 105 × 105 × 5 relations = ~55K (sample 3K)

Target: 10,000 clips with balanced categories
```

### Synthetic Generation Code Structure

```python
# tinyvid_syn/generator.py

class TinyVidSynGenerator:
    def __init__(self, resolution=64, num_frames=16):
        self.resolution = resolution
        self.num_frames = num_frames

    def generate_clip(self, template: str, objects: List[Object],
                      actions: List[Action]) -> Tuple[np.ndarray, str]:
        """Generate a single clip from template."""
        frames = np.zeros((self.num_frames, self.resolution, self.resolution, 3))

        for t in range(self.num_frames):
            frame = self.render_background()
            for obj, action in zip(objects, actions):
                obj_state = action.get_state(t / self.num_frames)
                frame = self.render_object(frame, obj, obj_state)
            frames[t] = frame

        caption = self.generate_caption(template, objects, actions)
        return frames, caption
```

---

## Part B: TinyVid-Real (Curated K400 Subset)

### Temporal-Critical Class Selection

**Criteria for inclusion**:
1. Action requires motion to recognize (not static pose)
2. Direction/order matters (pushing vs pulling)
3. Distinguishable at 64×64 resolution
4. Sufficient samples in K400

### Candidate Classes (from K400)

#### Motion Direction Classes (pairs)
| Forward | Reverse | Temporal Signal |
|---------|---------|-----------------|
| opening door | closing door | door position trajectory |
| pushing something | pulling something | object motion direction |
| picking up | putting down | hand/object trajectory |
| standing up | sitting down | body position trajectory |
| turning left | turning right | rotation direction |

#### Temporal Order Classes
| Action | Why Temporal? |
|--------|---------------|
| throwing | arm motion → release → flight |
| catching | flight → contact → secure |
| jumping | crouch → ascend → descend → land |
| clapping | hands apart → together → apart |
| waving | hand oscillation pattern |
| nodding | head oscillation pattern |
| shaking head | head oscillation (different axis) |

#### Interaction Classes
| Action | Why Temporal? |
|--------|---------------|
| high five | two hands approaching → contact |
| hugging | approach → embrace |
| shaking hands | approach → grip → motion |
| passing/receiving | object transfer trajectory |

### Proposed TinyVid-Real Classes (40 classes)

```python
TINYVID_REAL_CLASSES = {
    # Direction pairs (20 classes)
    'motion_direction': [
        ('opening door', 'closing door'),
        ('pushing something', 'pulling something'),
        ('picking up', 'putting down'),
        ('standing up', 'sitting down'),
        ('turning left', 'turning right'),
        ('moving forward', 'moving backward'),
        ('leaning left', 'leaning right'),
        ('raising hand', 'lowering hand'),
        ('bending over', 'straightening up'),
        ('spreading arms', 'folding arms'),
    ],

    # Order-sensitive (10 classes)
    'temporal_order': [
        'throwing',
        'catching',
        'jumping',
        'clapping',
        'waving hand',
        'nodding head',
        'shaking head',
        'bouncing ball',
        'kicking',
        'punching',
    ],

    # Interactions (10 classes)
    'interactions': [
        'high five',
        'hugging',
        'shaking hands',
        'passing object',
        'receiving object',
        'pushing person',
        'pulling person',
        'following',
        'chasing',
        'dancing together',
    ],
}
```

### Downsampling Pipeline

```
Original K400 clip (256×256, 30fps, ~10s)
    ↓
Temporal trim (center 2s)
    ↓
Spatial crop (center square)
    ↓
Resize to 64×64 (bicubic)
    ↓
Subsample to 8fps (16 frames)
    ↓
Quality filter (motion magnitude > threshold)
    ↓
TinyVid-Real clip
```

### Quality Filters

1. **Motion magnitude**: Optical flow must exceed threshold
2. **Clarity**: No excessive blur after downsampling
3. **Centering**: Main action must be visible in center crop
4. **Duration**: Action must complete within 2s window

### Statistics Target

```
40 classes × 250 clips/class = 10,000 clips
Storage: 10K × 16 frames × 64×64 × 3 bytes = ~200MB (raw)
         ~50MB compressed (MP4)
```

---

## Part C: Evaluation Protocol

### Retrieval Task

**Text-to-Video Retrieval**:
- Query: Text caption
- Gallery: All video clips
- Metric: Recall@K (K=1,5,10)

**Video-to-Text Retrieval**:
- Query: Video clip
- Gallery: All text captions
- Metric: Recall@K (K=1,5,10)

### Evaluation Splits

```
TinyVid-Syn:
  - Train: 7,000 clips
  - Val: 1,500 clips
  - Test: 1,500 clips

TinyVid-Real:
  - Train: 7,000 clips
  - Val: 1,500 clips
  - Test: 1,500 clips
```

### Diagnostic Subsets

For understanding model behavior:

| Subset | Purpose | Size |
|--------|---------|------|
| `direction_pairs` | Test direction sensitivity | 500 |
| `order_sensitive` | Test temporal order | 500 |
| `hard_negatives` | Test fine-grained temporal | 500 |
| `single_frame_solvable` | Control (should be easy) | 500 |

### Baseline Numbers (Targets)

| Model | TinyVid-Syn R@1 | TinyVid-Real R@1 |
|-------|-----------------|------------------|
| Random | 0.1% | 0.1% |
| Single-frame (no temporal) | ~30% | ~40% |
| Full temporal model | >60% | >50% |
| Human ceiling | ~95% | ~85% |

---

## Part D: Tiny Model Specification

### TinyViT-Video Architecture

```
TinyViT-S (Small):
  - Patch size: 8×8 (64 patches per frame)
  - Embedding dim: 256
  - Layers: 4
  - Heads: 4
  - MLP ratio: 2
  - Parameters: ~6M

TinyViT-T (Tiny):
  - Patch size: 8×8
  - Embedding dim: 128
  - Layers: 2
  - Heads: 2
  - MLP ratio: 2
  - Parameters: ~1.5M
```

### Training Configuration

```yaml
# TinyViT training config
data:
  dataset: tinyvid_real
  batch_size: 256
  num_workers: 4

model:
  name: tinyvit_s
  embed_dim: 256
  num_layers: 4
  num_heads: 4
  pooling: average  # or attention

training:
  epochs: 100
  lr: 1e-3
  warmup_epochs: 5
  optimizer: adamw
  weight_decay: 0.05

loss:
  type: contrastive
  temperature: 0.07
```

### Expected Training Time

| Hardware | TinyViT-S (100 epochs) |
|----------|------------------------|
| M4 MacBook (16GB) | ~30 minutes |
| T4 GPU | ~10 minutes |
| A100 GPU | ~3 minutes |

---

## File Structure

```
tinyvid/
├── README.md
├── LICENSE
├── data/
│   ├── tinyvid_syn/
│   │   ├── train/
│   │   ├── val/
│   │   ├── test/
│   │   └── metadata.json
│   └── tinyvid_real/
│       ├── train/
│       ├── val/
│       ├── test/
│       └── metadata.json
├── src/
│   ├── generator/          # Synthetic generation
│   ├── downsampler/        # K400 processing
│   ├── models/             # TinyViT implementations
│   └── evaluation/         # Retrieval evaluation
└── baselines/
    ├── tinyvit_s.pt
    └── results.json
```

---

## Next Steps

1. **Implement TinyVid-Syn generator** (2-3 days)
2. **Curate K400 class list** with human verification (1-2 days)
3. **Build downsampling pipeline** (1 day)
4. **Create evaluation harness** (1 day)
5. **Train TinyViT baselines** (1 day)
6. **Validate transfer to K400** (2-3 days)
