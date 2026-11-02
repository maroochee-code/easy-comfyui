# easy-compyui

ComfyUI를 쉽게 쓰기 위한 Claude Code 스킬입니다. 원하는 기능을 자연어로 말하면 최적의 AI 엔진을 추천하고, 노드 연결 방법과 설계도를 만들어 줍니다.

## 하는 일

요청마다 아래 4단계를 순서대로 출력합니다.

1. **추천 AI 엔진 & 모델 준비**: 추천 이유, 필요한 모델 파일, 저장할 폴더 경로
2. **노드 리스트 & 단계별 연결 가이드**: `[Core]` / `[Custom: 패키지명]` 뱃지, 슬롯 연결 순서, 권장 파라미터
3. **HTML 설계도**: 자동 배선되는 단일 HTML 노드 다이어그램
4. **워크플로우 JSON**: 노드·연결 중심의 경량 JSON과 실행용 스켈레톤 JSON

카탈로그에 없는 모델이나 커스텀 노드는 Hugging Face, Civitai, Comfy Registry, GitHub에서 확인하고, 검증하지 못한 노드에는 `[외부 검색 노드: 설치 및 슬롯 확인 필요]` 뱃지를 붙입니다.

## 파일 구성

| 파일 | 설명 |
| :--- | :--- |
| `SKILL.md` | 스킬 본문. 이름, 호출 조건, 응답 4단계 프로토콜, 외부 탐색 규칙 |
| `references/engine_catalog.md` | 엔진 카탈로그. 한글 발음 표기 → 공식 영문명 매핑, 엔진별 모델 파일·폴더·핵심 노드·권장 설정 (Flux, Qwen Image, Krea2, Z-Image, Wan, LTX, MiniMax H3) |
| `assets/blueprint_template.html` | HTML 설계도 템플릿. `WORKFLOW_DATA`의 nodes/links를 채우면 `getBoundingClientRect()`로 소켓 좌표를 읽어 베지어 곡선 배선을 그림 |

## 설치

이 폴더를 통째로 스킬 디렉터리에 넣습니다.

- 프로젝트용: `<프로젝트>/.claude/skills/easy-compyui/`
- 전체 공용: `~/.claude/skills/easy-compyui/`

새 세션에서 `/easy-compyui`로 호출하거나, "ComfyUI로 ○○ 워크플로우 만들어줘"처럼 말하면 자동으로 쓰입니다.

## 슬롯 색상 표준

MODEL `#b58df1` · CLIP `#ffd166` · VAE `#ff6b6b` · CONDITIONING `#f77f00` · LATENT `#c77dff` · IMAGE `#4cc9f0` · MASK `#e0e0e0` · AUDIO `#2ecc71`
