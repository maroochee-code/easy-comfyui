# easy-comfyui

ComfyUI를 쉽게 쓰기 위한 Claude Code 스킬입니다. 원하는 기능을 자연어로 말하면 최적의 AI 엔진을 추천하고, 노드 연결 방법과 설계도를 만들어 줍니다.

## 하는 일

요청마다 아래 4단계를 순서대로 출력합니다.

1. **추천 AI 엔진 & 모델 준비**: 추천 이유, 필요한 모델 파일, 저장할 폴더 경로
2. **노드 리스트 & 단계별 연결 가이드**: `[Core]` / `[Custom: 패키지명]` 뱃지, 슬롯 연결 순서, 권장 파라미터
3. **HTML 설계도**: 자동 배선되는 단일 HTML 노드 다이어그램. 노드에 마우스를 올리면 역할과 이유가 말풍선으로 뜨고, 아래에 **연결 확인표**와 **필요 파일 표**가 자동으로 붙습니다
4. **워크플로우 JSON**: 노드·연결 중심의 경량 JSON(참고용)과, ComfyUI 화면에 끌어다 놓으면 노드와 선이 자동 생성되는 실행용 API 형식 JSON

카탈로그에 없는 모델이나 커스텀 노드는 Hugging Face, Civitai, Comfy Registry, GitHub에서 확인하고, 검증하지 못한 노드에는 `[외부 검색 노드: 설치 및 슬롯 확인 필요]` 뱃지를 붙입니다.

구성 전에 **0단계 설치 점검**을 먼저 합니다. 이 PC의 모델·커스텀 노드·GPU를 읽고, 필요한 파일 표와 설치 순서를 안내하고, 사용자가 "준비 완료"라고 한 뒤에 진행합니다. (SKILL.md의 '0단계'와 '작업 전 점검 규칙' 참고)

## 파일 구성

| 파일 | 설명 |
| :--- | :--- |
| `SKILL.md` | 스킬 본문. 이름, 호출 조건, 0단계 설치 점검, 응답 4단계 프로토콜, 설계도·JSON 작성 규칙, 작업 전 점검 규칙, 외부 탐색 규칙 |
| `scripts/preflight_check.py` | 필요한 모델 파일(이름·크기)과 커스텀 노드가 PC에 있는지 확인. 이름만 다른 파일도 크기로 찾아 알려 줌 |
| `scripts/validate_workflow.py` | 실행용 JSON의 연결과 모델 이름(실제 파일 존재 여부)을 검증. ComfyUI가 없는 이름을 조용히 다른 파일로 바꾸는 사고를 막음 |
| `references/engine_catalog.md` | 엔진 카탈로그. 한글 발음 표기 → 공식 영문명 매핑, 엔진별 모델 파일·폴더·핵심 노드·권장 설정 (Flux, Qwen Image, Krea2, Z-Image, Wan, LTX, MiniMax H3, SDXL 애니 변환 + ControlNet, IP-Adapter 얼굴 유지 + 포즈) |
| `assets/blueprint_template.html` | HTML 설계도 템플릿. `WORKFLOW_DATA`의 nodes/links를 채우면 `getBoundingClientRect()`로 소켓 좌표를 읽어 베지어 곡선 배선을 그림. 노드별 말풍선(`tip`), 연결 확인표, 필요 파일 표(`files`), CONTROL_NET·IPADAPTER 색을 지원 |

## 점검 스크립트 사용법

```bash
python -I scripts/preflight_check.py --models-dir <ComfyUI models 폴더> --spec required.json --nodes-dir <custom_nodes 폴더>
python -I scripts/validate_workflow.py workflow_api.json --models-dir <ComfyUI models 폴더>
```

파일의 **이름과 크기**만 확인하며, 내용 손상 여부는 검사하지 않습니다.

## 설치

이 폴더를 통째로 스킬 디렉터리에 넣습니다.

- 프로젝트용: `<프로젝트>/.claude/skills/easy-comfyui/`
- 전체 공용: `~/.claude/skills/easy-comfyui/`

새 세션에서 `/easy-comfyui`로 호출하거나, "ComfyUI로 ○○ 워크플로우 만들어줘"처럼 말하면 자동으로 쓰입니다.

## 슬롯 색상 표준

MODEL `#b58df1` · CLIP `#ffd166` · VAE `#ff6b6b` · CONDITIONING `#f77f00` · LATENT `#c77dff` · IMAGE `#4cc9f0` · MASK `#e0e0e0` · AUDIO `#2ecc71`

표준 8색 외에 CONTROL_NET `#00c2a8`(청록), IPADAPTER `#ff8fb8`(분홍)을 추가로 씁니다.

## 변경 기록

버전별 변경 내용은 [CHANGELOG.md](CHANGELOG.md)를 참고하세요.

## 라이선스

[MIT License](LICENSE)입니다. 자유롭게 사용, 수정, 배포할 수 있고, 저작권 표시와 라이선스 문구만 유지하면 됩니다. 소프트웨어는 보증 없이 있는 그대로 제공됩니다.
