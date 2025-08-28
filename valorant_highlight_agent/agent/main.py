import yaml
import argparse
import os
from agent.detector import HighlightDetector
from agent.clipper import ClipSaver
from agent.uploader import YouTubeUploader

def main(config_path):
    print(f"[INFO] Loading config from: {config_path}")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    input_video = config["input_video"]
    output_folder = config.get("output_folder", "output")
    os.makedirs(output_folder, exist_ok=True)

    print(f"[INFO] Input video: {input_video}")
    print(f"[INFO] Output folder: {output_folder}")

    detector = HighlightDetector(config)
    print(f"[INFO] Starting highlight detection...")
    clips = detector.detect(input_video)
    print(f"[INFO] Detected {len(clips)} highlight(s).")

    if not clips:
        print("[WARNING] No highlights were detected. Try lowering the threshold in config.yaml.")
        return

    saver = ClipSaver(config)
    uploader = None

    if config.get("upload", {}).get("enabled", False):
        uploader = YouTubeUploader(config)
        print("[INFO] YouTube uploading is enabled.")

    for idx, (start, end) in enumerate(clips, 1):
        print(f"[INFO] Saving clip {idx}: start={start:.2f}s, end={end:.2f}s")
        clip_path = saver.save_clip(input_video, start, end, idx)
        print(f"[INFO] Saved: {clip_path}")

        if uploader:
            print(f"[INFO] Uploading clip {idx} to YouTube...")
            url = uploader.upload(clip_path)
            print(f"[INFO] Uploaded: {url}")
            with open("uploaded_clips.log", "a") as logf:
                logf.write(f"{clip_path} -> {url}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/config.yaml")
    args = parser.parse_args()
    main(args.config)
