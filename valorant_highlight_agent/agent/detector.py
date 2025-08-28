import cv2
import numpy as np

class HighlightDetector:
    def __init__(self, config):
        self.threshold = config.get("highlight_threshold", 0.8)  # normalized motion threshold
        self.clip_length = config.get("clip_length", 20)         # in seconds

    def detect(self, video_path):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps

        motion_scores = []
        ret, prev = cap.read()
        if not ret:
            return []

        prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            diff = cv2.absdiff(prev_gray, gray)
            score = np.sum(diff) / diff.size
            motion_scores.append(score)
            prev_gray = gray

        cap.release()

        if not motion_scores:
            return []

        # Normalize scores to 0–1
        max_score = max(motion_scores)
        norm_scores = [s / max_score for s in motion_scores]

        highlights = []
        used_ranges = []

        for i, score in enumerate(norm_scores):
            if score >= self.threshold:
                highlight_time = i / fps
                half = self.clip_length / 2

                start = max(0, highlight_time - half)
                end = min(duration, highlight_time + half)

                # Avoid overlapping clips
                if any(abs(start - r[0]) < 2 for r in used_ranges):
                    continue

                highlights.append((start, end))
                used_ranges.append((start, end))

        return highlights
