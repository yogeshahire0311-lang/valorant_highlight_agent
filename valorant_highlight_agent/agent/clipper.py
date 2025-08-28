import subprocess
import os

class ClipSaver:
    def __init__(self, config):
        self.output_folder = config.get("output_folder", "output")

    def save_clip(self, input_video, start, end, idx):
        out_file = os.path.join(self.output_folder, f"clip_{idx:02d}.mp4")
        duration = end - start
        cmd = [
            "ffmpeg", "-y", "-i", input_video,
            "-ss", str(start), "-t", str(duration),
            "-c", "copy", out_file
        ]
        print(f"[CLIPPER] Running FFmpeg: clip {idx}, duration={duration:.2f}s")
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return out_file
