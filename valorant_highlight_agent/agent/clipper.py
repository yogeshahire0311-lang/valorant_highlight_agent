# agent/clipper.py
import subprocess
import os
import re

class ClipSaver:
    def __init__(self, config):
        self.output_folder = config.get("output_folder", "output")
        os.makedirs(self.output_folder, exist_ok=True)

    def _safe_stem(self, path: str) -> str:
        """Return a filesystem-safe stem from the input video filename."""
        stem = os.path.splitext(os.path.basename(path))[0]
        # Replace anything not alnum, dot, underscore, or hyphen with underscore
        return re.sub(r'[^A-Za-z0-9._-]+', '_', stem)

    def _unique_path(self, base_stem: str, idx: int) -> str:
        """Build a unique output file path to avoid overwriting."""
        candidate = os.path.join(self.output_folder, f"{base_stem}_clip_{idx:02d}.mp4")
        if not os.path.exists(candidate):
            return candidate
        # If exists, add a numeric suffix
        counter = 2
        while True:
            alt = os.path.join(self.output_folder, f"{base_stem}_clip_{idx:02d}_{counter}.mp4")
            if not os.path.exists(alt):
                return alt
            counter += 1

    def save_clip(self, input_video: str, start: float, end: float, idx: int) -> str:
        """
        Save a clip using ffmpeg without re-encoding when possible.
        Output filename pattern: <original_video_stem>_clip_<idx>.mp4
        """
        duration = max(0.1, float(end) - float(start))
        stem = self._safe_stem(input_video)
        out_file = self._unique_path(stem, idx)

        cmd = [
            "ffmpeg",
            "-y",
            "-ss", f"{start:.3f}",  # input-side seek (faster, keyframe-aligned)
            "-i", input_video,
            "-t", f"{duration:.3f}",
            "-c", "copy",
            out_file
        ]

        # If stream copy fails (e.g., keyframe boundaries), re-encode quickly
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            reencode_cmd = [
                "ffmpeg", "-y",
                "-ss", f"{start:.3f}", "-i", input_video,
                "-t", f"{duration:.3f}",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
                "-c:a", "aac", "-b:a", "192k",
                out_file
            ]
            subprocess.run(reencode_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return out_file
