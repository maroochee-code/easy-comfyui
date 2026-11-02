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

### H. SDXL Anime img2img + ControlNet (사진 → 애니 변환, 포즈 유지) ✅ 실제 실행 검증됨
2026-11 Windows ComfyUI Desktop, RTX 2060 6GB에서 실행해 결과 확인(첫 실행 268초). 아래 항목 중 "(HF 확인)"은 Hugging Face 저장소 페이지에서 직접 확인한 값.
- **Models & Folders**:
  - Checkpoint (`models/checkpoints/`): `animagine-xl-3.1.safetensors` (6.94GB, cagliostrolab/animagine-xl-3.1, openrail++) (HF 확인)
  - ControlNet (`models/controlnet/`), 두 방식 중 택일:
    - 전용 모델 2개: `xinsir_openpose_sdxl.safetensors`(포즈), `xinsir_canny_sdxl_v2.safetensors`(윤곽선) — 사용자 환경에서 실제 동작 확인
    - Union 1개: xinsir/controlnet-union-sdxl-1.0 저장소의 `diffusion_pytorch_model_promax.safetensors` (2.51GB, 이름이 `_promax`로 끝나는 쪽) (HF 확인). 저장소 파일명이 일반적이라 `controlnet-union-sdxl-1.0_promax.safetensors`처럼 바꿔 두면 구분이 쉽다. 이 경우 `SetUnionControlNetType`이 필요하나 Union 구성은 **실행 검증하지 못함 [확인 필요]**.
- **Custom Node**: `comfyui_controlnet_aux` (fannovel16, Manager에서 검색어 `controlnet aux`). `DWPreprocessor`, `LineArtPreprocessor` 제공. 같은 이름 계열(`ComfyUI-ControlnetAux` cvalentin, `ComfyUI-ControlNet-Nodes`)과 혼동 주의.
- **Key Nodes (API class_type)**: `LoadImage`, `ImageScaleToTotalPixels`(megapixels 1.0, lanczos), `CheckpointLoaderSimple`, `DWPreprocessor`(detect_hand/body/face `enable`, resolution 1024, bbox `yolox_l.onnx`, pose `dw-ll_ucoco_384.onnx`, `scale_stick_for_xinsr_cn` `enable`), `Canny`(low 0.4 / high 0.8, 코어 노드), `ControlNetLoader`, `ControlNetApplyAdvanced`(포즈 강도 0.9 end 0.8 → 윤곽선 강도 0.5 end 0.6 순서로 직렬 연결), `CLIPTextEncode`×2, `VAEEncode`, `KSampler`, `VAEDecode`, `SaveImage`.
- **Recommended Settings**: Steps 28, CFG 6.0, Sampler `euler_ancestral`, Scheduler `normal`, **Denoise 0.62**(원본 유지와 스타일 변화의 균형. 0.7↑ 더 애니, 0.5↓ 원본에 가까움).
- **Prompt Rule**: 긍정에 `anime style, 1boy` + 사진 속 특징(안경, 옷, 소품, 배경, 포즈)을 말로 다시 적고, 부정에 `photo, realistic, 3d, lowres, bad hands, extra fingers`로 실사 회귀를 막는다.
- **Low VRAM(6GB 이하) 팁**: 윤곽선 ControlNet 제거, megapixels 0.7, steps 20.
- **대안(미검증)**: Qwen Image Edit 계열에 "애니 스타일로, 포즈 유지" 프롬프트만 주는 방식. 파일명 검증 필요.

### I. IP-Adapter 얼굴 유지 + ControlNet 포즈 (인물 사진의 소년이 다른 사진의 자세를 하도록) ✅ 실제 실행 검증됨
2026-11 Windows ComfyUI Desktop, RTX 2060 6GB. 위 H항목의 체크포인트·openpose 모델과 `comfyui_controlnet_aux`를 그대로 쓰고, 얼굴 유지용으로 IP-Adapter를 더한다. (파일명·크기는 Hugging Face 저장소 페이지로 확인)
- **Custom Node**: `ComfyUI_IPAdapter_plus` (cubiq, Manager 검색어 `ipadapter plus`). 2025-04-14부터 "maintenance only" 상태라 ComfyUI 업데이트 후 호환 문제가 생길 수 있다.
- **Models & Folders** (`models/` 아래):
  - `ipadapter/ip-adapter-plus-face_sdxl_vit-h.safetensors` (848MB, h94/IP-Adapter `sdxl_models`). 같은 이름의 `.bin`(1.01GB)이 아닌 `.safetensors`.
  - `clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors` (2.53GB). h94/IP-Adapter `models/image_encoder`의 `model.safetensors`를 **이 이름으로 바꿔야** Unified Loader가 찾는다.
  - `ipadapter` 폴더는 처음엔 없어서 직접 만들어야 하고, 만든 뒤 ComfyUI를 재시작한다.
- **Key Nodes (API class_type)**: `PrepImageForClipVision`(interpolation `LANCZOS`, crop_position `top`, sharpening 0.0), `IPAdapterUnifiedLoader`(preset `PLUS FACE (portraits)`, 출력 MODEL·IPADAPTER), `IPAdapterAdvanced`(입력 model·ipadapter·image, weight 0.8, weight_type `linear`, combine_embeds `concat`, start 0.0, end 1.0, embeds_scaling `V only`, 출력 MODEL).
- **연결 순서**: 체크포인트 MODEL → UnifiedLoader → IPAdapterAdvanced → **KSampler.model**. 인물 사진 → PrepImage → Advanced.image. UnifiedLoader의 ipadapter → Advanced.ipadapter. (UnifiedLoader 출력을 KSampler에 바로 이으면 IP-Adapter가 적용되지 않는다.)
- **포즈 쪽**: 참고 사진 → 크기 조정 → DWPreprocessor(scale_stick_for_xinsr_cn enable) → ControlNetApplyAdvanced(strength 1.0, end 0.9). 시작 latent는 포즈 사진을 VAEEncode한 것을 쓰되 KSampler `denoise 1.0`이라 크기만 남는다. 윤곽선 ControlNet은 포즈 사진 속 옷·체형까지 따라 하므로 쓰지 않는다.
- **슬롯 색**: IPADAPTER `#ff8fb8`(표준 외 추가색).
- **한계**: 전신에서는 얼굴이 작아 닮은 정도가 제한적이다. 개선은 얼굴 영역 재생성(FaceDetailer 등)이 필요하나 미검증 `[확인 필요]`. 6GB VRAM에서는 모델 오프로딩으로 느리다.
