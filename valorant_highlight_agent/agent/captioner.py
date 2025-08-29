import random
import os

class CaptionGenerator:
    def __init__(self):
        # Valorant-specific templates for more engaging captions
        self.templates = [
            "🔥 Insane Ace at {timestamp} — Valorant Highlight #{idx}",
            "💥 1v5 Clutch Moment — Unbelievable Play #{idx}",
            "🎯 Crazy Headshot Streak at {timestamp}",
            "⚡ Non-stop action! Epic Round #{idx}",
            "🚀 Jaw-dropping Flick Shot at {timestamp}",
            "😱 Wild Spray Control — Clip #{idx}",
            "🏆 Game-Changing Clutch at {timestamp}"
        ]

    def generate(self, idx, start_time):
        print(f"[INFO] Generating caption for clip {idx}...")
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
