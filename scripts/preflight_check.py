#!/usr/bin/env python3
"""설치 점검(Preflight): 워크플로우에 필요한 모델 파일과 커스텀 노드가 PC에 있는지 확인한다.

사용법:
  python -I preflight_check.py --models-dir <ComfyUI models 폴더> --spec required.json
                               [--nodes-dir <custom_nodes 폴더>]

required.json 형식:
  {
    "files": [
      {"folder": "ipadapter", "name": "ip-adapter-plus-face_sdxl_vit-h.safetensors",
       "size_bytes": 847517512, "url": "https://huggingface.co/..."}
    ],
    "nodes": ["comfyui_controlnet_aux", "ComfyUI_IPAdapter_plus"]
  }

판정:
  OK        이름과 크기가 맞음
  이름변경   이름은 다르지만 크기가 같은 파일이 있음 (예: model.safetensors -> 정해진 이름)
  크기불일치 이름은 같지만 크기가 다름 (다운로드 중단 의심)
  없음      파일이 없음
파일 내용(손상 여부)은 검사하지 않는다. 이름과 크기만 본다.
"""
import argparse, json, os, sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

TOL = 0.005  # 크기 허용 오차 0.5%


def find_files(folder):
    """하위 폴더까지 포함해 {상대경로: 크기} 를 돌려준다."""
    found = {}
    for root, _, names in os.walk(folder):
        for n in names:
            p = os.path.join(root, n)
            try:
                found[os.path.relpath(p, folder).replace("\\", "/")] = os.path.getsize(p)
            except OSError:
                pass
    return found


def same_size(a, b):
    return b > 0 and abs(a - b) / b <= TOL


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models-dir", required=True)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--nodes-dir")
    a = ap.parse_args()
    spec = json.load(open(a.spec, encoding="utf-8"))
    problems = 0

    print("== 모델 파일 ==")
    for f in spec.get("files", []):
        folder = os.path.join(a.models_dir, f["folder"])
        want, size = f["name"], f.get("size_bytes")
        files = find_files(folder) if os.path.isdir(folder) else {}
        if want in files or any(k.endswith("/" + want) for k in files):
            have = files.get(want) or next(v for k, v in files.items() if k.endswith("/" + want))
            if size and not same_size(have, size):
                print(f"[크기불일치] {f['folder']}/{want}  현재 {have:,}B / 기대 {size:,}B  -> 다시 받기")
                problems += 1
            else:
                print(f"[OK]        {f['folder']}/{want}")
            continue
        alt = [k for k, v in files.items() if size and same_size(v, size)]
        if alt:
            print(f"[이름변경]   {f['folder']}/{alt[0]}  ->  {want}  (크기가 같음, 이름만 바꾸면 됨)")
        else:
            if not os.path.isdir(folder):
                print(f"[없음]      {f['folder']}/{want}  (폴더 자체가 없음)  받는 곳: {f.get('url', '-')}")
            else:
                print(f"[없음]      {f['folder']}/{want}  받는 곳: {f.get('url', '-')}")
        problems += 1

    if spec.get("nodes"):
        print("== 커스텀 노드 ==")
        if not a.nodes_dir or not os.path.isdir(a.nodes_dir):
            print("(--nodes-dir 를 주면 확인합니다)")
        else:
            installed = {d.lower() for d in os.listdir(a.nodes_dir)}
            for n in spec["nodes"]:
                if n.lower() in installed:
                    print(f"[OK]        {n}")
                else:
                    print(f"[설치필요]  {n}  (Manager에서 설치 후 재시작)")
                    problems += 1

    print(f"\n문제 {problems}건")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
