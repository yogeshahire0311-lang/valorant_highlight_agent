import random
import os

class CaptionGenerator:
    def __init__(self):
        self.templates = [
            "🔥 Epic moment in Valorant — clip #{idx}",
            "💥 Crazy highlight at {timestamp}",
            "🎯 Insane play — Valorant clutch #{idx}",
            "⚡ Non-stop action! Must-watch clip #{idx}"
        ]

    def generate(self, idx, start_time):
        template = random.choice(self.templates)
        minutes = int(start_time // 60)
        seconds = int(start_time % 60)
        timestamp = f"{minutes:02d}:{seconds:02d}"
        return template.format(idx=idx, timestamp=timestamp)

    def save_caption(self, clip_path, caption):
        txt_path = os.path.splitext(clip_path)[0] + ".txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(caption)
        return txt_path
