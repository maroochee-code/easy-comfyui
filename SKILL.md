---
name: easy-compyui
description: EasyCompyUI 스킬. 자연어로 원하는 기능을 말하면 ComfyUI 최적 AI 엔진 추천, 필수 모델 저장 경로, 단계별 노드 연결 가이드, 자바스크립트 자동 배선 HTML 설계도 및 경량 연결 JSON을 생성합니다. Use when the user asks to create a ComfyUI workflow, requests step-by-step node connection tutorials, asks for an HTML visual node diagram, or wants a ComfyUI workflow format.
---

# EasyCompyUI (ComfyUI Workflow Architect)

사용자의 자연어 요구사항을 분석하여 최적의 ComfyUI AI 엔진을 추천하고, 단계별 노드 연결 가이드, 브라우저에서 실행 가능한 자동 배선 HTML 설계도, 그리고 ComfyUI 호환형 구조 JSON을 생성합니다.

## 참조 파일

- `references/engine_catalog.md`: 엔진별 모델 파일명, 폴더, 핵심 노드, 권장 파라미터, 한글 발음 표기 → 공식 영문명 대응표. 엔진을 추천하거나 노드를 구성하기 전에 먼저 읽는다.
  - 카탈로그의 모델명과 파일명 중 일부는 공식 문서로 검증되지 않았다. 사용자에게 안내할 때는 `[확인 필요]`로 표시하고, 가능하면 Hugging Face나 Comfy Registry에서 확인한다.
- `assets/blueprint_template.html`: HTML 설계도 템플릿. 복사한 뒤 `WORKFLOW_DATA`(nodes, links)만 교체한다.

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
- **슬롯 색상 표준 준수**: MODEL(보라 `#b58df1`), CLIP(노란 `#ffd166`), VAE(빨강 `#ff6b6b`), CONDITIONING(주황 `#f77f00`), LATENT(연보라 `#c77dff`), IMAGE(파랑 `#4cc9f0`), MASK(회백 `#e0e0e0`), AUDIO(초록 `#2ecc71`).
- 자바스크립트(`getBoundingClientRect()`)가 소켓 중심 좌표를 자동으로 찾아 베지어 곡선 배선을 그리므로 좌표 오류가 발생하지 않음.
- **ControlNet 사용 시** CONTROL_NET 슬롯은 표준 8색에 없으므로 청록 `#00c2a8`을 쓰고, 범례에 "표준 외 추가색"이라고 밝힌다. (템플릿에 이미 들어 있음)
- **노드별 말풍선(`tip`)**: 모든 노드에 `tip: [{label:"역할", text}, {label:"왜", text}]`를 넣는다. 마우스를 올리면 설명이 뜬다. 기획자가 읽는 말로 쓰고, 설정값을 넣을 때는 "올리면/내리면 어떻게 되는지"까지 적는다. 핵심 노드(KSampler의 denoise 등)는 `핵심` 라벨로 강조한다.
- **레이아웃 규칙**: 노드 높이는 `헤더 40 + 슬롯줄 수 × 28 + 파라미터줄 수 × 18 + 여백` 정도로 넉넉히 잡는다. 같은 열의 노드는 y 간격을 높이보다 20px 이상 크게 둔다. 작성 후 브라우저에서 `getBoundingClientRect()`로 노드끼리 겹치는지 검사한다. 긴 뱃지 텍스트는 줄바꿈되므로 `Custom: 패키지명`처럼 짧게 쓴다.
- **작성 후 검증**: (1) 모든 링크의 출발·도착 슬롯이 존재하고 타입이 같은지, (2) 노드 수와 배선 수가 의도와 같은지, (3) 말풍선이 모든 노드에서 뜨는지를 코드로 확인한다. 노드가 많으면 파이썬 등으로 `WORKFLOW_DATA`를 생성하고 링크 타입 일치를 `assert`로 검사한다.

### 4. 워크플로우 JSON 출력
- 상세 파라미터(`widgets_values`) 오류를 방지하기 위해 노드 종류와 연결 흐름 중심의 **경량 구조 JSON**을 기본 제공하고, 검증된 템플릿 기반의 **실행용 스켈레톤 JSON**을 이원화 제공.
- **실행용 JSON은 API 형식**(`{"1": {"class_type": "...", "inputs": {...}}}`)으로 만든다. 연결은 `["노드ID", 출력인덱스]`로 쓴다. ComfyUI Desktop 캔버스에 끌어다 놓으면 노드와 선이 자동 생성되는 것을 실제로 확인했다.
- 경량 JSON은 참고용이며 ComfyUI에 넣는 파일이 아니다. 사용자에게 "넣을 파일은 실행용 JSON"이라고 분명히 알린다. (파일 링크를 클릭하면 내용만 미리 보이고 다운로드되지 않는 점도 안내한다. 파일은 이미 PC 폴더에 있다.)
- 모델 파일명(`ckpt_name`, `control_net_name` 등)은 사용자의 설치 상태와 다르면 목록 첫 번째 파일로 **조용히 대체**된다. 만들기 전에 사용자가 가진 모델 이름을 확인하고, 실행 전에 해당 칸이 의도한 모델인지 확인하도록 안내한다.

## 작업 전 점검 규칙 (실전에서 얻은 교훈)

1. **설치 상태부터 확인한다.** 사용자가 이미 가진 모델과 커스텀 노드를 먼저 묻거나, 화면 캡처의 모델 목록을 확인한다. 가진 모델로 구성을 바꿀 수 있으면 새로 받게 하지 않는다. (예: Union ControlNet 대신 이미 설치된 openpose/canny 전용 모델 두 개를 쓰도록 구성 변경)
2. **모델 파일명과 크기는 Hugging Face 저장소 페이지(`/tree/main`)에서 확인한 뒤 안내한다.** 저장소 파일명과 ComfyUI가 기대하는 이름이 다를 수 있으니, 이름 변경이 필요하면 명시한다. 확인하지 못한 것은 `[확인 필요]`.
3. **하드웨어를 확인한다.** `nvidia-smi --query-gpu=name,memory.total --format=csv`로 GPU와 VRAM을 본다. VRAM이 모델 합계보다 작으면 느려질 것(오프로딩)을 미리 알리고, 가벼운 대안(ControlNet 하나 빼기, 해상도 낮추기, 스텝 줄이기)을 제시한다. 예상 시간은 추정이라고 밝힌다.
4. **Manager 안내**: ComfyUI Desktop의 Manager는 "커스텀 노드 관리자"로, 노드 설치용이다. 모델 파일은 대부분 직접 받아 `models/` 폴더에 넣어야 한다. 모델 폴더는 Desktop 기준 `ComfyUI-Shared\models\...`일 수 있으니 사용자의 저장 창 경로를 확인한다.
5. **용어를 구분해서 설명한다.** "체크포인트(모델 파일)"와 "Load Checkpoint(그 파일을 불러오는 노드)", "HTML 설계도(지도, 클릭 불가)"와 "실행용 JSON(ComfyUI에 넣는 파일)"을 사용자가 혼동하기 쉽다.
6. **파라미터 수치는 '시작값'이라고 밝힌다.** 특히 img2img 계열은 `denoise`가 핵심 다이얼이다. 올리면 새로 그리는 비율이 커지고(스타일 변화↑, 원본 유지↓), 내리면 반대다. 조절법을 표로 안내한다.
7. **커스텀 노드 위젯은 버전마다 다르다.** 설치된 버전에서 새 위젯이 생길 수 있다(예: DWPose의 `scale_stick_for_xinsr_cn`). 사용자가 보내는 캡처에서 차이를 확인하고 구성에 반영한다.
8. **결과 후 설명 요청에 대비해 노드별 `역할 / 왜 이렇게 구성했는지`를 정리해 둔다.** 설계도 `tip`에 같은 내용을 넣어 한 번에 해결한다.

## 외부 탐색 및 Fallback 규칙
- 사전 정의된 목록에 없는 최신 모델이나 커스텀 노드 요청 시:
  - **Hugging Face / Civitai**를 조회하여 모델 아키텍처와 폴더 경로를 확인.
  - **Comfy Registry (`registry.comfy.org`) / GitHub**를 조회하여 노드의 입출력 슬롯 규격을 검증.
  - 검증되지 않은 외부 노드는 `[외부 검색 노드: 설치 및 슬롯 확인 필요]` 뱃지를 표기하여 환각(Hallucination) 방지.
