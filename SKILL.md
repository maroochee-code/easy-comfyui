---
name: easy-comfyui
description: EasyComfyUI 스킬. 자연어로 원하는 기능을 말하면 ComfyUI 최적 AI 엔진 추천, 필수 모델 저장 경로, 단계별 노드 연결 가이드, 자바스크립트 자동 배선 HTML 설계도 및 경량 연결 JSON을 생성합니다. Use when the user asks to create a ComfyUI workflow, requests step-by-step node connection tutorials, asks for an HTML visual node diagram, or wants a ComfyUI workflow format.
---

# EasyComfyUI (ComfyUI Workflow Architect)

사용자의 자연어 요구사항을 분석하여 최적의 ComfyUI AI 엔진을 추천하고, 단계별 노드 연결 가이드, 브라우저에서 실행 가능한 자동 배선 HTML 설계도, 그리고 ComfyUI 호환형 구조 JSON을 생성합니다.

## 참조 파일

- `references/engine_catalog.md`: 엔진별 모델 파일명, 폴더, 핵심 노드, 권장 파라미터, 한글 발음 표기 → 공식 영문명 대응표. 엔진을 추천하거나 노드를 구성하기 전에 먼저 읽는다.
  - 카탈로그의 모델명과 파일명 중 일부는 공식 문서로 검증되지 않았다. 사용자에게 안내할 때는 `[확인 필요]`로 표시하고, 가능하면 Hugging Face나 Comfy Registry에서 확인한다.
- `assets/blueprint_template.html`: HTML 설계도 템플릿. 복사한 뒤 `WORKFLOW_DATA`(nodes, links, files)만 교체한다. 노드별 말풍선(`tip`), **연결 확인표**, **필요 파일 표**가 `WORKFLOW_DATA`에서 자동 생성된다.
- `scripts/preflight_check.py`: 필요한 모델 파일(이름·크기)과 커스텀 노드가 PC에 있는지 확인한다. 이름만 다른 파일(예: `model.safetensors`)도 크기로 찾아 "이름변경"이라고 알려 준다.
- `scripts/validate_workflow.py`: 실행용(API 형식) JSON의 연결 검증, **모델 이름이 실제 파일로 존재하는지** 검증(ComfyUI는 없는 이름을 조용히 다른 파일로 바꾼다), LoadImage 파일 존재 확인.
  - 사용 예: `python -I scripts/validate_workflow.py workflow_api.json --models-dir <models 폴더>`
  - `OUTPUTS` 표에 없는 class_type은 출력 칸 검사를 건너뛰므로, 새 노드를 쓰면 공식 소스에서 출력 개수를 확인해 표에 추가한다.

## 0단계: 설치 점검 (구성 전에 먼저, 사용자에게 보여 주고 "준비 완료"를 기다린다)

설치가 필요한 구성(커스텀 노드, 새 모델)이면 노드를 만들기 전에 아래를 먼저 한다. 건너뛰면 "빨간 노드", "모델 없음", "연결 끊김" 오류가 한꺼번에 나온다.

1. **PC 상태를 읽는다.** ComfyUI의 `models` 폴더와 `custom_nodes` 폴더를 직접 열어 이미 있는 것을 확인한다. (Desktop은 `ComfyUI-Shared/models`와 `ComfyUI-Installs/.../custom_nodes`처럼 위치가 나뉜다. 사용자의 저장 창·캡처로 경로를 확인한다.) GPU/VRAM도 `nvidia-smi`로 확인한다.
2. **이미 가진 것으로 구성을 바꿀 수 있으면 바꾼다.** 새로 받게 하기 전에 대안을 찾는다.
3. **필요 파일 표를 만든다.** 항목은 `폴더 / 파일 이름 / 공식 크기 / 이름 변경 여부 / 받는 곳(URL)`이고, URL과 크기는 Hugging Face 저장소 페이지에서 확인한 값만 쓴다. 같은 표를 `required.json`으로도 만든다(`scripts/preflight_check.py` 형식).
4. **사용자가 직접 할 일을 순서대로 안내한다.** 순서는 고정이다: ① Manager에서 커스텀 노드 설치 → ② ComfyUI 재시작 → ③ 모델 파일 받기·이름 변경 → ④ `R` 새로고침 → ⑤ **새 탭**에서 JSON 불러오기. 노드 패키지 설치 **전에** JSON을 불러오면 그 노드들의 연결이 끊긴 채 탭에 남는다. 이미 그렇게 됐다면 탭을 모두 닫고 **파일 이름을 바꾼 새 사본**으로 다시 불러오게 한다.
5. 사용자가 "받았어"라고 하면 `preflight_check.py`로 이름·크기를 확인해 알려 준 뒤, 문제 없을 때만 실행을 안내한다.
6. **내 작업 결과를 낸 뒤** `validate_workflow.py`를 돌려 연결과 모델 이름을 검증하고, 통과한 것만 전달한다.

## 응답 표준 4단계 프로토콜

사용자가 특정 기능을 요청하면 반드시 아래 4가지 섹션을 순서대로 출력합니다:

### 1. 추천 AI 엔진 & 모델 준비
- 작업에 가장 최적화된 엔진/모델 추천 이유.
- **필요 파일 표**(폴더 / 파일 이름 / 크기 / 이름 변경 / 받는 곳)를 반드시 포함한다. 받은 뒤 이름을 바꿔야 하는 파일은 "이름 변경 필요"를 굵게 적고 바꿀 이름을 한 글자씩 대조할 수 있게 코드 블록으로 보여 준다.
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
- **표준 외 슬롯 색**: CONTROL_NET은 청록 `#00c2a8`, IPADAPTER는 분홍 `#ff8fb8`을 쓴다. 새 슬롯 종류가 나오면 템플릿의 CSS 변수와 `types` 배열에 같이 추가한다(안 하면 선 색이 안 나온다).
- **연결 확인표와 필요 파일 표**는 템플릿이 `WORKFLOW_DATA`(`links`, `files`)에서 자동으로 만든다. `files`를 반드시 채운다. 사용자가 ComfyUI 화면에서 노드가 겹쳐 가려지거나 선을 잘못 이었을 때 이 표와 비교해 바로잡는다.
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
4. **Manager 안내**: ComfyUI Desktop의 Manager는 "커스텀 노드 관리자"로, 노드 설치용이다. 모델 파일은 대부분 직접 받아 `models/` 폴더에 넣어야 한다. 모델 폴더는 Desktop 기준 `ComfyUI-Sharedmodels\...`일 수 있으니 사용자의 저장 창 경로를 확인한다.
5. **용어를 구분해서 설명한다.** "체크포인트(모델 파일)"와 "Load Checkpoint(그 파일을 불러오는 노드)", "HTML 설계도(지도, 클릭 불가)"와 "실행용 JSON(ComfyUI에 넣는 파일)"을 사용자가 혼동하기 쉽다.
6. **파라미터 수치는 '시작값'이라고 밝힌다.** 특히 img2img 계열은 `denoise`가 핵심 다이얼이다. 올리면 새로 그리는 비율이 커지고(스타일 변화↑, 원본 유지↓), 내리면 반대다. 조절법을 표로 안내한다.
7. **커스텀 노드 위젯은 버전마다 다르다.** 설치된 버전에서 새 위젯이 생길 수 있다(예: DWPose의 `scale_stick_for_xinsr_cn`). 사용자가 보내는 캡처에서 차이를 확인하고 구성에 반영한다.
8. **결과 후 설명 요청에 대비해 노드별 `역할 / 왜 이렇게 구성했는지`를 정리해 둔다.** 설계도 `tip`에 같은 내용을 넣어 한 번에 해결한다.
9. **이름 일치 검사.** 스킬 이름(`name`), 폴더명, 저장소명, 문서 속 호출 명령이 서로 같은지 확인한다. 기존 파일의 이름이 이상해 보이면(오타 의심) 그대로 따라 쓰지 말고 사용자에게 먼저 짚는다. 수정 후에는 `grep`으로 잘못된 표기가 남았는지 확인한다.
10. **모델 이름은 사용자 PC의 실제 파일 이름으로 쓴다.** JSON에 일반적인 이름을 넣으면 ComfyUI가 조용히 다른 파일로 바꾼다. `validate_workflow.py --models-dir`로 확인하고, 사용자가 실행 전에 해당 칸의 모델 이름을 눈으로도 확인하게 안내한다.
11. **오류 화면을 받으면 원인부터 구분한다.** (a) 빨간 노드 = 패키지 미설치, (b) "연결 누락" = 선이 빠짐(연결 확인표와 비교), (c) "~ model not found" = 모델 파일 없음/이름 다름(`preflight_check.py`), (d) 같은 증상이 설치 후에도 남으면 불러온 탭이 오래된 것이니 새 탭+새 파일 이름으로 다시 불러오기.
12. **API 형식 JSON의 한계**: 불러올 때 노드가 없으면 연결이 끊긴다. 계속 문제가 되면 ComfyUI 자체 저장 형식(노드 위치·연결 포함)으로 다시 만들되, 칸 순서가 틀리면 값이 어긋나므로 설치된 버전의 화면(캡처)으로 순서를 확인한 뒤 만든다.

## 외부 탐색 및 Fallback 규칙
- 사전 정의된 목록에 없는 최신 모델이나 커스텀 노드 요청 시:
  - **Hugging Face / Civitai**를 조회하여 모델 아키텍처와 폴더 경로를 확인.
  - **Comfy Registry (`registry.comfy.org`) / GitHub**를 조회하여 노드의 입출력 슬롯 규격을 검증.
  - 검증되지 않은 외부 노드는 `[외부 검색 노드: 설치 및 슬롯 확인 필요]` 뱃지를 표기하여 환각(Hallucination) 방지.
