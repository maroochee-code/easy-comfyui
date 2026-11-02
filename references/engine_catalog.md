# ComfyUI Engine Catalog & Node Dictionary

## 1. Phonetic Korean to Official English Normalization

| Phonetic / Informal Name | Official English Name | Category |
| :--- | :--- | :--- |
| 눈차쿠 / 쌍절곤 로더 | `Nunchaku Flux DiT Loader` | 4-bit Quantized Inference Engine |
| 완 브이에이스 | `WanVideo VACE (Start to End Frame)` | Wan 2.1/2.2 Video-to-Video / Frame Control |
| 스케일 포즈 / 엔엘에프 | `Scail Pose (Render NLF Pose)` | 3D Neural Localizer Field Pose Control |
| 어니 이미지 | `Ernie Image Turbo` | Text-to-Image Model |
| 설퍼 모델 | `Sulphur Dev / Sulphur LoRA` | Uncensored Video/Image Model (LTX Base) |
| 부구 이미지 | `Boogu Image Edit` | Multi-Reference Image Editing Model |
| 이디오그램 포 | `Ideogram 4.0` (`DualModelCFGGuider`) | Typography & Poster Layout Model |
| 크레아 투 아이덴티티 | `Krea2 Turbo` + `Identity 1.2 LoRA` | Identity-Preserving Image Edit |
| 피아이디 업스케일 | `NVIDIA PiD (Pixel Space Diffusion)` | 4K Fast Upscale Model |

## 2. Core AI Engines, Folders & Standard Parameters

### A. Flux Series (Flux.1 Dev, Flux Fill, Flux Kontext Dev, Flux.2 Klein)
- **Models & Folders**:
  - Diffusion Model (`models/diffusion_models/`): `flux1-dev-fp8.safetensors`, `flux1-fill-dev.safetensors`, `flux1-dev-kontext-fp8.safetensors`, `flux2-klein-9b.safetensors`
  - Text Encoders (`models/text_encoders/`): `clip_l.safetensors` + `t5xxl_fp8_e4m3fn.safetensors` (Type: `flux`) or `qwen3_fp8.safetensors` (for Flux.2 Klein, Type: `flux2`)
  - VAE (`models/vae/`): `ae.safetensors` (Flux.1) or `flux2_vae.safetensors`
- **Key Nodes**: `LoadDiffusionModel`, `DualCLIPLoader`, `FluxGuidance` (default 3.5, Fill: 30.0), `ConditioningZeroOut`, `InpaintModelConditioning`, `DifferentialDiffusion`
- **Recommended Settings**: Steps: 20, CFG: 1.0, Sampler: `euler`, Scheduler: `simple`

### B. Qwen Image Series (Qwen Image 2.1 / Edit 2509 / 2512)
- **Models & Folders**:
  - Diffusion Model (`models/diffusion_models/`): `qwen_image_2.1_int8.safetensors` or `qwen_image_edit_2509_fp8.safetensors`
  - Text Encoder (`models/text_encoders/`): `qwen3_vl_8b_fp8.safetensors` (Type: `qwen_image`)
  - VAE (`models/vae/`): `qwen_image_vae.safetensors`
  - Optional LoRA (`models/loras/`): `qwen_lightning_4step.safetensors`, `3d_pose_v1.1.safetensors`
- **Key Nodes**: `TextEncodeQwenImage2.1` (accepts up to 10 reference images), `QwenImage2.1Cache`, `ResolutionSelector` (Character sheet recommended: 2.0 MP)
- **Recommended Settings**: Standard Steps: 20-25 (CFG 1.0-2.5), Lightning 4-Step LoRA: Steps 4, CFG 1.0

### C. Krea2 Turbo & Identity 1.2
- **Models & Folders**:
  - Diffusion Model (`models/diffusion_models/`): `krea2_turbo.safetensors`
  - Text Encoder (`models/text_encoders/`): `qwen3_vl_4b_fp8.safetensors` (Type: `krea2`)
  - VAE (`models/vae/`): `qwen_image_vae.safetensors`
  - LoRA (`models/loras/`): `krea2_identity_1.2.safetensors` (strength: 1.0)
- **Key Nodes**: `Krea2EditSourcePatch` (injects reference image latent into model), `Krea2EditPromptEncoder` (combines prompt + up to 2 reference images)
- **Prompt Rule**: Explicitly separate "What to change" and "What to keep (face, hair, lighting, pose)".

### D. Z-Image Turbo & ControlNet Union
- **Models & Folders**:
  - Diffusion Model (`models/diffusion_models/`): `z_image_turbo.safetensors`
  - Text Encoder (`models/text_encoders/`): `qwen3_8b.safetensors` (Type: `lumina2`)
  - VAE (`models/vae/`): `ae.safetensors` (Flux.1 VAE)
  - ControlNet (`models/model_patches/`): `z_image_turbo_controlnet_union_v2.0.safetensors` (Save in `model_patches`, not `controlnet`)
- **Key Nodes**: `ModelPatchLoader`, `QwenImageDiffsynthControlnet` (strength: 0.8), `AIO_Aux_Preprocessor` (OpenPose / DW), `EmptySD3LatentImage`
- **Recommended Settings**: Steps: 8, CFG: 1.0, Sampler: `euler`, Scheduler: `simple`

### E. Wan 2.1 / 2.2 Video & S2V
- **Models & Folders**:
  - Diffusion Models (`models/diffusion_models/`): `wan2.2_t2v_14b_high_noise_fp8.safetensors` + `wan2.2_t2v_14b_low_noise_fp8.safetensors`, or `wan2.2_s2v_fp8.safetensors`
  - Text Encoder (`models/text_encoders/`): `umt5_xxl_fp8.safetensors` (Type: `wan`)
  - VAE (`models/vae/`): `wan_2.1_vae.safetensors`
- **Key Nodes**: `ModelSamplingSD3` (shift: 8.0), `KSamplerAdvanced` (Pass 1 High-Noise: steps 0-10, Pass 2 Low-Noise: steps 10-20), `WanSoundImageToVideo` (Subgraph for S2V), `CreateVideo` (24 fps, 121 frames = ~5s), `SaveVideo`

### F. LTX 2.3 / 2.5 Video & Audio
- **Models & Folders**:
  - Checkpoint/Diffusion (`models/checkpoints/` or `models/diffusion_models/`): `ltx_2.3_distilled_fp8.safetensors` or `ltx_2.5_int8.safetensors`
  - Text Encoder (`models/text_encoders/`): `gemma3_fp4.safetensors` (LTX 2.3) or `gemma4_comfy_int8.safetensors` (LTX 2.5)
  - Latent Upscaler (`models/latent_upscale_models/`): `ltx_spatial_x2.safetensors`
- **Key Nodes**: Two-stage sampling (`SamplerCustomAdvanced` at half resolution -> `SeparateAVLatent` -> `LatentUpscaler` x2 -> `ConcatAVLatent` -> second `SamplerCustomAdvanced`), `LTXVDualCFGGuider`, `ICLoRALoaderModelOnly`
- **Constraints**: Resolution must be a multiple of 32 (e.g., 960x1280), Frames: 121 at 24 fps.

### G. MiniMax H3 Video
- **Models & Folders**:
  - Diffusion Model (`models/diffusion_models/`): `minimax_h3_ref_int8.safetensors`
  - Text Encoder (`models/text_encoders/`): `qwen3_vl_32b_int8.safetensors`
  - VAE (`models/vae/`): Requires both `minimax_video_vae.safetensors` and `minimax_audio_vae.safetensors`
- **Key Nodes**: `MiniMaxH3ReferenceToVideo`, `ResolutionSelector` (0.2-0.5 MP for initial low-res pass -> Latent Upscale -> High-res pass), `MathExpression` (24 fps * seconds).