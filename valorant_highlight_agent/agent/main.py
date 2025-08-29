import yaml
import argparse
import os
import shutil
from agent.detector import HighlightDetector
from agent.clipper import ClipSaver
from agent.uploader import YouTubeUploader


def process_video(video_path, config, output_folder, uploader=None, archive_folder=None):
    print(f"\n[INFO] Processing video: {video_path}")
    detector = HighlightDetector(config)

    try:
        clips = detector.detect(video_path)
    except Exception as e:
        print(f"[ERROR] Failed to detect highlights for {video_path}: {e}")
        return

    print(f"[INFO] Detected {len(clips)} highlight(s).")
    if not clips:
        print("[WARNING] No highlights were detected. Try lowering the threshold in config.yaml.")
        return

    saver = ClipSaver(config)

    for idx, (start, end) in enumerate(clips, 1):
        try:
            print(f"[INFO] Saving clip {idx}: start={start:.2f}s, end={end:.2f}s")
            clip_path = saver.save_clip(video_path, start, end, idx)
            print(f"[INFO] Saved: {clip_path}")

            if uploader:
                print(f"[INFO] Uploading clip {idx} to YouTube...")
                url = uploader.upload(clip_path)
                print(f"[INFO] Uploaded: {url}")
                with open("uploaded_clips.log", "a") as logf:
                    logf.write(f"{clip_path} -> {url}\n")
        except Exception as e:
            print(f"[ERROR] Failed to save/upload clip {idx} from {video_path}: {e}")

    # Move processed video to archive
    if archive_folder:
        os.makedirs(archive_folder, exist_ok=True)
        dest = os.path.join(archive_folder, os.path.basename(video_path))
        try:
            shutil.move(video_path, dest)
            print(f"[INFO] Archived processed video to {dest}")
        except Exception as e:
            print(f"[WARNING] Could not archive {video_path}: {e}")


def main(config_path):
    print(f"[INFO] Loading config from: {config_path}")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    output_folder = config.get("output_folder", "output")
    os.makedirs(output_folder, exist_ok=True)

    # Setup uploader if enabled
    uploader = None
    if config.get("upload", {}).get("enabled", False):
        uploader = YouTubeUploader(config)
        print("[INFO] YouTube uploading is enabled.")

    # Decide which videos to process
    video_files = []
    if config.get("process_all", False):
        videos_folder = config.get("videos_folder", "videos")
        video_files = [
            os.path.join(videos_folder, f)
            for f in os.listdir(videos_folder)
            if f.endswith(".mp4")
        ]
        print(f"[INFO] Found {len(video_files)} video(s) in {videos_folder}")
    else:
        video_files = [config["input_video"]]
        print(f"[INFO] Single video mode: {video_files[0]}")

    archive_folder = config.get("archive_folder", "archive")

    for video_path in video_files:
        process_video(video_path, config, output_folder, uploader, archive_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/config.yaml")
    args = parser.parse_args()
    main(args.config)
