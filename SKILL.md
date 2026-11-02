---
name: easy-compyui
description: EasyCompyUI 스킬. 자연어로 원하는 기능을 말하면 ComfyUI 최적 AI 엔진 추천, 필수 모델 저장 경로, 단계별 노드 연결 가이드, 자바스크립트 자동 배선 HTML 설계도 및 경량 연결 JSON을 생성합니다. Use when the user asks to create a ComfyUI workflow, requests step-by-step node connection tutorials, asks for an HTML visual node diagram, or wants a ComfyUI workflow format.
---

# EasyCompyUI (ComfyUI Workflow Architect)

사용자의 자연어 요구사항을 분석하여 최적의 ComfyUI AI 엔진을 추천하고, 단계별 노드 연결 가이드, 브라우저에서 실행 가능한 자동 배선 HTML 설계도, 그리고 ComfyUI 호환형 구조 JSON을 생성합니다.

## 참조 파일
- `references/engine_catalog.md`: 엔진별 모델 파일명, 폴더 경로, 핵심 노드, 권장 파라미터와 한글 발음 표기 → 공식 영문명 매핑. 엔진을 추천하거나 모델 경로를 안내하기 전에 먼저 읽습니다.
- `assets/blueprint_template.html`: HTML 설계도 템플릿. `WORKFLOW_DATA`만 교체해서 출력합니다.

## 응답 표준 4단계 프로토콜

사용자가 특정 기능을 요청하면 반드시 아래 4가지 섹션을 순서대로 출력합니다:

### 1. 추천 AI 엔진 & 모델 준비
- 작업에 가장 최적화된 엔진/모델 추천 이유.
- 필요한 모델 파일 목록과 정확한 로컬 폴더 경로 안내:
  - 디퓨전 모델 (`models/diffusion_models/`)
  - 텍스트 인코더 (`models/text_encoders/`)
  - VAE (`models/vae/`)
  - LoRA (`models/loras/`)
  - ControlNet / 패치 (`models/controlnet/` 또는 `models/model_patches/`)

### 2. 노드 리스트 및 단계별 연결 가이드 (Step-by-Step)
- 사용할 노드 이름과 뱃지 (`[Core]` 또는 `[Custom: 패키지명]`) 표기.
- 초보자도 그대로 따라 꽂을 수 있는 1., 2., 3. 순서의 슬롯 연결 설명 (예: `Load Checkpoint의 MODEL(보라색) -> KSampler의 model`).
- 권장 핵심 파라미터 세팅값 (Steps, CFG, Sampler, Scheduler, Denoise, 해상도/프레임 제약 조건).

### 3. 정밀 슬롯 배선 HTML 설계도 (Interactive HTML Blueprint)
- `assets/blueprint_template.html` 기반의 단일 독립형 HTML 출력.
- **슬롯 색상 표준 준수**: MODEL(보라 `#b58df1`), CLIP(노란 `#ffd166`), VAE(빨강 `#ff6b6b`), CONDITIONING(주황 `#f77f00`), LATENT(연보라 `#c77dff`), IMAGE(파랑 `#4cc9f0`).
- 자바스크립트(`getBoundingClientRect()`)가 소켓 중심 좌표를 자동으로 찾아 베지어 곡선 배선을 그리므로 좌표 오류가 발생하지 않음.

### 4. 워크플로우 JSON 출력
- 상세 파라미터(`widgets_values`) 오류를 방지하기 위해 노드 종류와 연결 흐름 중심의 **경량 구조 JSON**을 기본 제공하고, 검증된 템플릿 기반의 **실행용 스켈레톤 JSON**을 이원화 제공.

## 외부 탐색 및 Fallback 규칙
- 사전 정의된 목록에 없는 최신 모델이나 커스텀 노드 요청 시:
  - **Hugging Face / Civitai**를 조회하여 모델 아키텍처와 폴더 경로를 확인.
  - **Comfy Registry (`registry.comfy.org`) / GitHub**를 조회하여 노드의 입출력 슬롯 규격을 검증.
  - 검증되지 않은 외부 노드는 `[외부 검색 노드: 설치 및 슬롯 확인 필요]` 뱃지를 표기하여 환각(Hallucination) 방지.