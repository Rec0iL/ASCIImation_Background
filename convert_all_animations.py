#!/usr/bin/env python3
import os
import json
import math
import random

def parse_starwars(txt_path):
    if not os.path.exists(txt_path):
        print(f"Warning: {txt_path} not found.")
        return []
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
        frames.append([delay, "\n".join(frame_lines)])
        idx += 14
    return frames

def gen_nyan_cat_frames():
    frames = []
    rainbow_wave1 = "~_=-_=-_=-_=-_=-_=-_=-_=-_=-_=-_=-"
    rainbow_wave2 = "_=-_=-_=-_=-_=-_=-_=-_=-_=-_=-_=-~"

    for f in range(12):
        r_line1 = rainbow_wave1[f % 6:] + rainbow_wave1[:f % 6]
        r_line2 = rainbow_wave2[f % 6:] + rainbow_wave2[:f % 6]
        star = "  *  " if f % 2 == 0 else "   + "
        star2 = " +   " if f % 2 == 0 else "  *  "

        c_lines = [
            f"       {star}                                 {star2}",
            f"{r_line1[:28]}   /\\_/\\ ",
            f"{r_line2[:28]} =( o.o )=",
            f"{r_line1[:28]}   (   ) ",
            f"{r_line2[:28]}   \"\" \"\" ",
            f"       {star2}                                 {star}"
        ]
        frames.append([2, "\n".join(c_lines)])
    return frames

def gen_party_parrot_frames():
    frames = []
    head_positions = [
        ("  .---.  ", " / o o \\ ", "|  (__) |", " \\__=__/ "),
        ("   .---. ", "  / o o \\", " | (__) |", "  \\__=__/"),
        ("    .---.", "   / o o \\", "  | (__) |", "   \\__=__/"),
        ("   .---. ", "  / o o \\", " | (__) |", "  \\__=__/"),
        ("  .---.  ", " / o o \\ ", "|  (__) |", " \\__=__/ "),
        (" .---.   ", "/ o o \\  ", "| (__) | ", "\\__=__/  "),
        (".---.    ", "/ o o \\  ", "| (__) | ", "\\__=__/  "),
        (" .---.   ", "/ o o \\  ", "| (__) | ", "\\__=__/  ")
    ]
    for i, h in enumerate(head_positions):
        lines = [
            "          PARTY PARROT ASCII",
            f"           {h[0]}",
            f"           {h[1]}",
            f"           {h[2]}",
            f"           {h[3]}",
            "         ~~( PARTY TIME! )~~"
        ]
        frames.append([2, "\n".join(lines)])
    return frames

def gen_3d_cube_frames(count=48):
    frames = []
    width, height = 54, 15
    for f in range(count):
        angle = (f / count) * 2 * math.pi
        sin_a, cos_a = math.sin(angle), math.cos(angle)
        sin_b, cos_b = math.sin(angle * 0.8), math.cos(angle * 0.8)

        nodes = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1, 1],  [1, -1, 1],  [1, 1, 1],  [-1, 1, 1]
        ]
        edges = [
            (0,1), (1,2), (2,3), (3,0),
            (4,5), (5,6), (6,7), (7,4),
            (0,4), (1,5), (2,6), (3,7)
        ]

        canvas = [[' ' for _ in range(width)] for _ in range(height)]
        proj = []
        for x, y, z in nodes:
            xz = x * cos_a - z * sin_a
            zz = x * sin_a + z * cos_a
            yz = y * cos_b - zz * sin_b
            zz = y * sin_b + zz * cos_b
            fov = 3.6
            px = int(width / 2 + (xz * fov / (zz + 4.2)) * (width / 2.4))
            py = int(height / 2 + (yz * fov / (zz + 4.2)) * (height / 2.4))
            proj.append((px, py))
            if 0 <= px < width and 0 <= py < height:
                canvas[py][px] = '#'

        for p1, p2 in edges:
            x0, y0 = proj[p1]
            x1, y1 = proj[p2]
            dx, dy = abs(x1 - x0), abs(y1 - y0)
            steps = max(dx, dy, 1)
            for i in range(steps + 1):
                cx = int(x0 + (x1 - x0) * i / steps)
                cy = int(y0 + (y1 - y0) * i / steps)
                if 0 <= cx < width and 0 <= cy < height:
                    if canvas[cy][cx] == ' ':
                        canvas[cy][cx] = '*'

        frame_text = '\n'.join(''.join(row) for row in canvas)
        frames.append([2, frame_text])
    return frames

# ============================================================
# NEW ANIMATIONS
# ============================================================

def gen_matrix_rain_frames(count=360):
    """Seamlessly looping Matrix digital rain effect with authentic katakana/matrix glyphs."""
    random.seed(42)
    width, height = 64, 20
    chars = "0123456789AZXCVBNM<>*+:!?ｦｱｳｴｵｶｷｹｺｻｼｽｾｿﾀﾂﾃﾅﾆﾇﾈﾊﾋﾎﾏﾐﾑﾒﾓﾔﾕﾗﾘﾜ"

    num_cols = width // 2
    columns = []

    for c in range(num_cols):
        speed = random.choice([1, 1, 2, 2, 3])
        length = random.randint(7, 15)
        total_dist = count * speed
        target_h = height + length + random.randint(4, 12)
        valid_h = [h for h in range(target_h - 4, target_h + 8) if total_dist % h == 0]
        if not valid_h:
            valid_h = [h for h in range(16, 50) if total_dist % h == 0]
        cycle_h = random.choice(valid_h) if valid_h else 30

        start_offset = random.randint(0, cycle_h - 1)
        col_chars = [random.choice(chars) for _ in range(cycle_h)]

        columns.append({
            'x': c * 2 + (0 if c % 2 == 0 else 1),
            'speed': speed,
            'length': length,
            'cycle_h': cycle_h,
            'start_offset': start_offset,
            'chars': col_chars
        })

    frames = []
    for f in range(count):
        canvas = [[' ' for _ in range(width)] for _ in range(height)]

        for col in columns:
            head_pos = (col['start_offset'] + f * col['speed']) % col['cycle_h']
            head_y = head_pos - 5

            for j in range(col['length']):
                cy = head_y - j
                if 0 <= cy < height:
                    char_idx = (col['start_offset'] + f + j) % len(col['chars'])
                    if j == 0:
                        canvas[cy][col['x']] = col['chars'][char_idx].upper()
                    else:
                        canvas[cy][col['x']] = col['chars'][char_idx]

        frame_text = '\n'.join(''.join(row) for row in canvas)
        frames.append([1, frame_text])
    return frames


def gen_aquarium_frames(count=60):
    """ASCII aquarium with fish, bubbles, and seaweed."""
    random.seed(123)
    width, height = 60, 16

    # Fish templates (facing right and left)
    fish_r = ["><>", "><))'>", ">--->", "><((*>"]
    fish_l = ["<><", "<'((<>", "<---<", "<*))><"]

    fishes = []
    for i in range(6):
        direction = random.choice([1, -1])
        fish_idx = i % len(fish_r)
        template = fish_r[fish_idx] if direction > 0 else fish_l[fish_idx]
        fishes.append({
            'x': random.randint(0, width - 8),
            'y': random.randint(2, height - 4),
            'dir': direction,
            'speed': random.choice([1, 1, 2]),
            'template': template,
            'fish_idx': fish_idx
        })

    # Seaweed positions
    seaweed_x = [5, 15, 28, 42, 52]
    # Bubble columns
    bubbles = []
    for i in range(4):
        bubbles.append({
            'x': random.randint(3, width - 3),
            'y': random.randint(0, height - 1),
            'speed': 1
        })

    frames = []
    for f in range(count):
        canvas = [[' ' for _ in range(width)] for _ in range(height)]

        # Draw water surface
        for x in range(width):
            wave_char = '~' if (x + f) % 3 != 0 else '^'
            canvas[0][x] = wave_char

        # Draw sandy bottom
        for x in range(width):
            canvas[height - 1][x] = random.choice(['_', '.', ',', '_', '_'])

        # Draw seaweed (swaying)
        for sx in seaweed_x:
            sway = 1 if (f // 4) % 2 == 0 else -1
            for sy in range(height - 4, height - 1):
                wx = sx + (sway if sy < height - 2 else 0)
                if 0 <= wx < width:
                    canvas[sy][wx] = random.choice([')', '(', '|'])

        # Draw bubbles
        for b in bubbles:
            if 1 <= b['y'] < height - 1 and 0 <= b['x'] < width:
                canvas[b['y']][b['x']] = 'o'
            b['y'] -= b['speed']
            if b['y'] < 1:
                b['y'] = height - 3
                b['x'] = random.randint(3, width - 3)

        # Draw fish
        for fish in fishes:
            tx = fish['x']
            ty = fish['y']
            template = fish['template']
            for ci, ch in enumerate(template):
                px = tx + ci
                if 1 <= ty < height - 1 and 0 <= px < width:
                    canvas[ty][px] = ch

            fish['x'] += fish['dir'] * fish['speed']
            # Wrap around
            if fish['dir'] > 0 and fish['x'] > width:
                fish['x'] = -len(fish['template'])
                fish['y'] = random.randint(2, height - 4)
            elif fish['dir'] < 0 and fish['x'] < -len(fish['template']):
                fish['x'] = width
                fish['y'] = random.randint(2, height - 4)

        frame_text = '\n'.join(''.join(row) for row in canvas)
        frames.append([2, frame_text])
    return frames


def gen_rotating_donut_frames(count=60):
    """The classic spinning 3D ASCII donut/torus."""
    width, height = 50, 20
    frames = []
    luminance_chars = ".,-~:;=!*#$@"

    for f in range(count):
        A = f * 0.07
        B = f * 0.03
        z_buffer = [0.0] * (width * height)
        output = [' '] * (width * height)

        sin_A, cos_A = math.sin(A), math.cos(A)
        sin_B, cos_B = math.sin(B), math.cos(B)

        theta = 0.0
        while theta < 2 * math.pi:
            sin_t, cos_t = math.sin(theta), math.cos(theta)
            phi = 0.0
            while phi < 2 * math.pi:
                sin_p, cos_p = math.sin(phi), math.cos(phi)

                # Torus parametric coordinates (R1=1, R2=2)
                circle_x = cos_t + 2
                circle_y = sin_t

                # 3D rotation
                x = circle_x * (cos_B * cos_p + sin_A * sin_B * sin_p) - circle_y * cos_A * sin_B
                y = circle_x * (sin_B * cos_p - sin_A * cos_B * sin_p) + circle_y * cos_A * cos_B
                z = circle_x * cos_A * sin_p + circle_y * sin_A
                ooz = 1.0 / (z + 5)  # Perspective divide

                xp = int(width / 2 + width * 0.35 * ooz * x)
                yp = int(height / 2 - height * 0.35 * ooz * y)

                # Luminance from surface normal dot light direction
                L = cos_p * cos_t * sin_B - cos_A * cos_t * sin_p - sin_A * sin_t + cos_B * (cos_A * sin_t - cos_t * sin_A * sin_p)

                if 0 <= xp < width and 0 <= yp < height:
                    idx = yp * width + xp
                    if ooz > z_buffer[idx]:
                        z_buffer[idx] = ooz
                        lum_idx = max(0, int(L * 8))
                        lum_idx = min(lum_idx, len(luminance_chars) - 1)
                        output[idx] = luminance_chars[lum_idx]

                phi += 0.07
            theta += 0.07

        lines = []
        for row in range(height):
            line = ''.join(output[row * width:(row + 1) * width])
            lines.append(line)
        frames.append([1, '\n'.join(lines)])
    return frames


def gen_fireworks_frames(count=48):
    """Fireworks bursting in the night sky."""
    random.seed(77)
    width, height = 60, 18
    spark_chars = ['.', '*', '+', 'o', 'O', '#', '@', '*']

    # Pre-compute several firework bursts
    bursts = []
    for b in range(6):
        cx = random.randint(10, width - 10)
        cy = random.randint(3, height - 6)
        start_frame = b * 8
        num_sparks = random.randint(10, 20)
        sparks = []
        for s in range(num_sparks):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 2.5)
            sparks.append((angle, speed))
        bursts.append({
            'cx': cx, 'cy': cy,
            'start': start_frame,
            'sparks': sparks,
            'life': 10
        })

    frames = []
    for f in range(count):
        canvas = [[' ' for _ in range(width)] for _ in range(height)]

        # Occasional stars in the sky
        random.seed(42)
        for _ in range(15):
            sx = random.randint(0, width - 1)
            sy = random.randint(0, height - 3)
            if (f + sx) % 7 < 5:
                canvas[sy][sx] = '.'

        # Draw ground line
        for x in range(width):
            canvas[height - 1][x] = '_'

        # Draw active bursts
        for burst in bursts:
            age = f - burst['start']
            if age < 0:
                # Draw rising rocket trail
                trail_age = burst['start'] - f
                if trail_age <= 5:
                    trail_y = height - 2 - int((5 - trail_age) * (height - burst['cy'] - 2) / 5)
                    if 0 <= trail_y < height - 1 and 0 <= burst['cx'] < width:
                        canvas[trail_y][burst['cx']] = '|'
                        if trail_y + 1 < height - 1:
                            canvas[trail_y + 1][burst['cx']] = ':'
                continue
            if age >= burst['life']:
                continue

            # Draw sparks expanding outward
            progress = age / burst['life']
            for angle, speed in burst['sparks']:
                dx = math.cos(angle) * speed * age * 0.8
                dy = math.sin(angle) * speed * age * 0.5 + age * 0.15  # Gravity
                sx = int(burst['cx'] + dx)
                sy = int(burst['cy'] + dy)
                if 0 <= sx < width and 0 <= sy < height - 1:
                    fade = max(0, min(len(spark_chars) - 1, len(spark_chars) - 1 - int(progress * len(spark_chars))))
                    canvas[sy][sx] = spark_chars[fade]

        frame_text = '\n'.join(''.join(row) for row in canvas)
        frames.append([2, frame_text])

    return frames


def gen_dvd_bounce_frames(count=80):
    """The classic bouncing DVD logo screensaver."""
    width, height = 60, 18
    logo = [
        " _____  _     _ _____ ",
        "|  __ \\| |   | |  __ \\",
        "| |  | | |   | | |  | |",
        "| |  | | \\   / | |  | |",
        "| |__| |  \\ /  | |__| |",
        "|_____/    V   |_____/ ",
    ]
    logo_w = max(len(line) for line in logo)
    logo_h = len(logo)

    x, y = 5, 3
    dx, dy = 1, 1

    frames = []
    for f in range(count):
        canvas = [[' ' for _ in range(width)] for _ in range(height)]

        # Draw the logo
        for ly, line in enumerate(logo):
            for lx, ch in enumerate(line):
                px, py = x + lx, y + ly
                if 0 <= px < width and 0 <= py < height:
                    canvas[py][px] = ch

        frame_text = '\n'.join(''.join(row) for row in canvas)
        frames.append([2, frame_text])

        # Move
        x += dx
        y += dy

        # Bounce off walls
        if x + logo_w >= width or x <= 0:
            dx = -dx
            x += dx
        if y + logo_h >= height or y <= 0:
            dy = -dy
            y += dy

    return frames


def gen_sine_wave_frames(count=48):
    """Animated sine wave oscillating across the screen."""
    width, height = 60, 16
    frames = []

    for f in range(count):
        canvas = [[' ' for _ in range(width)] for _ in range(height)]

        # Draw horizontal axis
        mid_y = height // 2
        for x in range(width):
            canvas[mid_y][x] = '-'

        # Draw sine wave
        for x in range(width):
            phase = (f / count) * 2 * math.pi
            val = math.sin((x / width) * 4 * math.pi + phase)
            # Second harmonic
            val += 0.4 * math.sin((x / width) * 8 * math.pi - phase * 1.5)
            y = int(mid_y - val * (height / 2 - 1.5))
            y = max(0, min(height - 1, y))
            if canvas[y][x] == '-':
                canvas[y][x] = '+'
            else:
                canvas[y][x] = '*'

            # Draw vertical trace from axis to wave
            step = 1 if y > mid_y else -1
            if y != mid_y:
                for ty in range(mid_y + step, y, step):
                    if 0 <= ty < height:
                        canvas[ty][x] = ':'

        frame_text = '\n'.join(''.join(row) for row in canvas)
        frames.append([2, frame_text])
    return frames


def gen_3d_globe_frames(count=48):
    """Rotating wireframe globe/sphere."""
    width, height = 50, 18
    frames = []

    for f in range(count):
        canvas = [[' ' for _ in range(width)] for _ in range(height)]
        angle = (f / count) * 2 * math.pi

        radius = min(width // 4, height // 2 - 1)
        cx, cy = width // 2, height // 2

        # Draw latitude lines (horizontal circles)
        for lat in range(-2, 3):
            lat_angle = lat * math.pi / 5
            r = radius * math.cos(lat_angle)
            y_offset = radius * math.sin(lat_angle) * 0.6
            for i in range(80):
                t = (i / 80) * 2 * math.pi
                x3d = r * math.cos(t)
                z3d = r * math.sin(t)
                # Rotate around Y axis
                rx = x3d * math.cos(angle) - z3d * math.sin(angle)
                rz = x3d * math.sin(angle) + z3d * math.cos(angle)
                # Only draw front-facing points
                if rz > -radius * 0.3:
                    px = int(cx + rx)
                    py = int(cy + y_offset)
                    if 0 <= px < width and 0 <= py < height:
                        canvas[py][px] = '.' if rz < radius * 0.5 else '-'

        # Draw longitude lines (vertical great circles)
        for lon in range(6):
            lon_angle = lon * math.pi / 3 + angle
            for i in range(60):
                t = (i / 60) * 2 * math.pi
                x3d = radius * math.cos(t) * math.cos(lon_angle)
                y3d = radius * math.sin(t)
                z3d = radius * math.cos(t) * math.sin(lon_angle)
                # Only draw front-facing
                if z3d > -radius * 0.2:
                    px = int(cx + x3d)
                    py = int(cy + y3d * 0.6)
                    if 0 <= px < width and 0 <= py < height:
                        canvas[py][px] = '|' if abs(x3d) < 2 else '/'

        # Draw equator with thicker line
        for i in range(120):
            t = (i / 120) * 2 * math.pi
            x3d = radius * math.cos(t)
            z3d = radius * math.sin(t)
            rx = x3d * math.cos(angle) - z3d * math.sin(angle)
            rz = x3d * math.sin(angle) + z3d * math.cos(angle)
            if rz > -radius * 0.1:
                px = int(cx + rx)
                py = cy
                if 0 <= px < width:
                    canvas[py][px] = '='

        frame_text = '\n'.join(''.join(row) for row in canvas)
        frames.append([2, frame_text])
    return frames


def build():
    out_dir = "org.kde.plasma.starwars/contents/ui/code"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "animations.js")
    legacy_frames_path = os.path.join(out_dir, "frames.js")

    starwars_frames = parse_starwars("starwars.txt")
    nyan_frames = gen_nyan_cat_frames()
    parrot_frames = gen_party_parrot_frames()
    cube_frames = gen_3d_cube_frames()
    matrix_frames = gen_matrix_rain_frames()
    aquarium_frames = gen_aquarium_frames()
    donut_frames = gen_rotating_donut_frames()
    fireworks_frames = gen_fireworks_frames()
    dvd_frames = gen_dvd_bounce_frames()
    sine_frames = gen_sine_wave_frames()
    globe_frames = gen_3d_globe_frames()

    animations = [
        {"name": "Star Wars: Episode IV", "frames": starwars_frames},
        {"name": "Nyan Cat Rainbow Flight", "frames": nyan_frames},
        {"name": "Party Parrot Dance", "frames": parrot_frames},
        {"name": "3D Spinning Wireframe Cube", "frames": cube_frames},
        {"name": "Matrix Digital Rain", "frames": matrix_frames},
        {"name": "ASCII Aquarium", "frames": aquarium_frames},
        {"name": "Rotating Donut (Torus)", "frames": donut_frames},
        {"name": "Fireworks Display", "frames": fireworks_frames},
        {"name": "DVD Bouncing Logo", "frames": dvd_frames},
        {"name": "Sine Wave Oscillator", "frames": sine_frames},
        {"name": "Rotating Wireframe Globe", "frames": globe_frames},
    ]

    print("Building animations library...")
    for anim in animations:
        print(f" - {anim['name']}: {len(anim['frames'])} frames")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(".pragma library;\n\n")
        f.write("var animationLibrary = ")
        json.dump(animations, f, ensure_ascii=False, separators=(',', ':'))
        f.write(";\n")

    # Also keep legacy frames.js backwards compatible
    with open(legacy_frames_path, "w", encoding="utf-8") as f:
        f.write(".pragma library;\n\n")
        f.write("var movieFrames = ")
        json.dump(starwars_frames, f, ensure_ascii=False, separators=(',', ':'))
        f.write(";\n")

    print(f"Generated {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    build()
