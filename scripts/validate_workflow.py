#!/usr/bin/env python3
"""실행용(API 형식) 워크플로우 JSON 검증.

사용법:
  python -I validate_workflow.py workflow_api.json [--models-dir <models 폴더>] [--input-dir <ComfyUI input 폴더>]

검사 항목:
  1. 모든 연결이 존재하는 노드와, 그 노드의 출력 칸 범위 안을 가리키는지
  2. (--models-dir) 모델 이름 칸의 값이 실제 파일로 존재하는지
     ComfyUI는 목록에 없는 이름이면 조용히 첫 번째 파일로 바꿔 버리므로, 이 검사가 그 사고를 막는다.
  3. (--input-dir) LoadImage 의 이미지 파일이 input 폴더에 있는지
알 수 없는 class_type 은 출력 칸 개수 검사를 건너뛰고 알려 준다. OUTPUTS 표에 추가하면 된다.
"""
import argparse, json, os, sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# class_type -> 출력 칸 개수 (공식 소스/실제 실행으로 확인한 것만)
OUTPUTS = {
    "LoadImage": 2, "ImageScaleToTotalPixels": 1, "CheckpointLoaderSimple": 3,
    "CLIPTextEncode": 1, "VAEEncode": 1, "VAEDecode": 1, "KSampler": 1, "SaveImage": 0, "PreviewImage": 0,
    "ControlNetLoader": 1, "ControlNetApplyAdvanced": 2, "Canny": 1,
    "DWPreprocessor": 2, "LineArtPreprocessor": 1,
    "IPAdapterUnifiedLoader": 2, "IPAdapterAdvanced": 1, "PrepImageForClipVision": 1,
    "EmptyLatentImage": 1, "SetUnionControlNetType": 1,
}

# 모델 이름 입력 칸 -> models 아래 폴더
MODEL_INPUTS = {
    "ckpt_name": "checkpoints", "control_net_name": "controlnet", "vae_name": "vae",
    "lora_name": "loras", "unet_name": "diffusion_models", "clip_name": "text_encoders",
    "upscale_model_name": "upscale_models",
}


def exists_model(models_dir, folder, name):
    base = os.path.join(models_dir, folder)
    if not os.path.isdir(base):
        return False
    target = name.replace("\\", "/")
    for root, _, files in os.walk(base):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), base).replace("\\", "/")
            if rel == target:
                return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workflow")
    ap.add_argument("--models-dir")
    ap.add_argument("--input-dir")
    a = ap.parse_args()
    wf = json.load(open(a.workflow, encoding="utf-8"))
    bad, skipped, links = 0, set(), 0

    for nid, node in wf.items():
        ct = node["class_type"]
        for key, val in node["inputs"].items():
            if isinstance(val, list):
                links += 1
                src = wf.get(val[0])
                if src is None:
                    print(f"[연결오류] {nid}:{ct}.{key} <- 없는 노드 {val[0]}")
                    bad += 1
                    continue
                sct = src["class_type"]
                if sct not in OUTPUTS:
                    skipped.add(sct)
                elif val[1] >= OUTPUTS[sct]:
                    print(f"[연결오류] {nid}:{ct}.{key} <- {val[0]}:{sct} 의 출력 {val[1]} (출력은 {OUTPUTS[sct]}개뿐)")
                    bad += 1
            elif a.models_dir and key in MODEL_INPUTS and isinstance(val, str):
                if not exists_model(a.models_dir, MODEL_INPUTS[key], val):
                    print(f"[모델없음] {nid}:{ct}.{key} = '{val}' 가 {MODEL_INPUTS[key]} 폴더에 없음 "
                          f"(ComfyUI가 다른 파일로 조용히 바꿀 수 있음)")
                    bad += 1
            elif a.input_dir and ct == "LoadImage" and key == "image":
                if not os.path.isfile(os.path.join(a.input_dir, val)):
                    print(f"[이미지없음] {nid}:LoadImage image = '{val}' 가 input 폴더에 없음 (노드에서 직접 올리기)")
                    bad += 1

    print(f"노드 {len(wf)}개, 연결 {links}개 검사, 문제 {bad}건")
    if skipped:
        print("출력 칸 개수를 몰라 건너뛴 노드:", ", ".join(sorted(skipped)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
