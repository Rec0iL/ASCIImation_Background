#!/usr/bin/env python3
import os
import json

def convert():
    txt_path = "starwars.txt"
    out_dir = "org.kde.plasma.starwars/contents/ui/code"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "frames.js")

    if not os.path.exists(txt_path):
        print(f"Error: {txt_path} not found.")
        return

    with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
        raw_lines = f.readlines()

    frames = []
    idx = 0
    total_lines = len(raw_lines)

    while idx < total_lines:
        delay_str = raw_lines[idx].strip()
        if not delay_str:
            idx += 1
            continue
        try:
            delay = int(delay_str)
        except ValueError:
            idx += 1
            continue

        frame_lines = []
        for j in range(13):
            if idx + 1 + j < total_lines:
                frame_lines.append(raw_lines[idx + 1 + j].rstrip("\r\n"))
            else:
                frame_lines.append("")

        # store delay and text block
        frames.append([delay, "\n".join(frame_lines)])
        idx += 14

    print(f"Parsed {len(frames)} frames.")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(".pragma library;\n\n")
        f.write("var movieFrames = ")
        json.dump(frames, f, ensure_ascii=False, separators=(',', ':'))
        f.write(";\n")

    print(f"Generated {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    convert()
