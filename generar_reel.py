"""
PREMIUM MEDICAL AESTHETICS REEL
Carlos Dueñas — Estética Médica
Duration: 10 seconds | Format: 1080x1920 (9:16) | 30fps
Style: Clinical · Minimalist · Premium
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy import ImageClip, concatenate_videoclips, CompositeVideoClip
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────
W, H    = 1080, 1920
FPS     = 30
TOTAL_S = 10.0
FRAMES  = int(TOTAL_S * FPS)

FONTS_DIR  = "/home/user/clinica-estetica/fonts"
OUTPUT_DIR = "/home/user/clinica-estetica"
FRAMES_DIR = "/tmp/reel_frames"
os.makedirs(FRAMES_DIR, exist_ok=True)

# ── PALETA PREMIUM ────────────────────────────────────────────────────────────
WHITE      = (252, 250, 247)   # blanco cálido, no frío
BEIGE_SOFT = (242, 236, 226)   # beige muy suave
BEIGE_MID  = (210, 198, 182)   # beige medio
GREY_LIGHT = (195, 190, 182)   # gris calido claro
GREY_MID   = (140, 132, 122)   # gris calido medio
DARK       = (28,  24,  20)    # casi negro cálido
GOLD       = (180, 152, 100)   # dorado apagado

# ── FUENTES ───────────────────────────────────────────────────────────────────
def font(size, style="serif"):
    try:
        p = f"{FONTS_DIR}/PlayfairDisplay-Bold.ttf" if style == "serif" \
            else f"{FONTS_DIR}/Montserrat-Light.ttf"
        return ImageFont.truetype(p, size)
    except:
        return ImageFont.load_default()

# ── HELPERS ───────────────────────────────────────────────────────────────────
def ease_in_out(t):
    """Curva de animación suave."""
    return t * t * (3 - 2 * t)

def lerp(a, b, t):
    return a + (b - a) * t

def alpha_blend(fg, bg, alpha):
    """Mezcla fg sobre bg con alpha 0-1."""
    return tuple(int(lerp(b, f, alpha)) for f, b in zip(fg[:3], bg[:3]))

def draw_centered(draw, text, y, fnt, color, tracking=0):
    """Texto centrado con tracking (letter spacing)."""
    if tracking == 0:
        bb   = draw.textbbox((0,0), text, font=fnt)
        x    = (W - (bb[2]-bb[0])) // 2
        draw.text((x, y), text, font=fnt, fill=color)
    else:
        # Manual letter spacing
        total_w = sum(draw.textbbox((0,0), c, font=fnt)[2] for c in text) \
                  + tracking * (len(text) - 1)
        x = (W - total_w) // 2
        for ch in text:
            draw.text((x, y), ch, font=fnt, fill=color)
            bb = draw.textbbox((0,0), ch, font=fnt)
            x += (bb[2]-bb[0]) + tracking

def draw_line_h(draw, y, x1_frac, x2_frac, color, width=1):
    draw.line([(int(W*x1_frac), y), (int(W*x2_frac), y)], fill=color, width=width)

# ── GENERADOR DE FONDOS ───────────────────────────────────────────────────────
def make_gradient_bg(t_norm, variant=0):
    """
    Fondo con gradiente vertical suave que respira levemente.
    variant 0: blanco→beige (apertura)
    variant 1: beige→blanco (cierre)
    """
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    for row in range(H):
        frac  = row / H
        breath = 0.02 * np.sin(t_norm * np.pi)  # respiración muy sutil
        if variant == 0:
            top_c = np.array(WHITE,      dtype=float)
            bot_c = np.array(BEIGE_SOFT, dtype=float)
        else:
            top_c = np.array(BEIGE_SOFT, dtype=float)
            bot_c = np.array(WHITE,      dtype=float)
        mixed = top_c + (bot_c - top_c) * (frac + breath)
        mixed = np.clip(mixed, 0, 255).astype(np.uint8)
        arr[row, :] = mixed
    return Image.fromarray(arr, "RGB")

# ── PARTÍCULAS / PUNTOS SUTILES ───────────────────────────────────────────────
def draw_particles(draw, t_norm, alpha_mult=1.0):
    """Puntos muy pequeños que representan células/moléculas."""
    np.random.seed(42)
    positions = [(np.random.randint(80, W-80),
                  np.random.randint(200, H-200))
                 for _ in range(18)]
    for i, (px, py) in enumerate(positions):
        phase  = (t_norm * 0.3 + i * 0.17) % 1.0
        a      = int(ease_in_out(min(phase * 3, 1.0)) *
                     ease_in_out(max(1.0 - (phase - 0.7) * 3, 0.0)) *
                     55 * alpha_mult)
        r      = np.random.randint(2, 5)
        col    = (*GREY_LIGHT, a)
        draw.ellipse([(px-r, py-r), (px+r, py+r)], fill=col)

# ── LÍNEAS GEOMÉTRICAS SUTILES ────────────────────────────────────────────────
def draw_geometry(draw, t_norm, alpha_mult=1.0):
    """Líneas horizontales finas — muy tenues, médico-científicas."""
    base_a = int(35 * alpha_mult)
    # Línea central superior
    a1 = int(base_a * ease_in_out(min(t_norm * 2, 1.0)))
    draw.line([(W//2-200, H//2-420), (W//2+200, H//2-420)],
              fill=(*GREY_MID, a1), width=1)
    # Línea central inferior
    a2 = int(base_a * ease_in_out(min(max(t_norm*2-0.3, 0), 1.0)))
    draw.line([(W//2-140, H//2+420), (W//2+140, H//2+420)],
              fill=(*GREY_MID, a2), width=1)

# ══════════════════════════════════════════════════════════════════════════════
#  GENERACIÓN FRAME A FRAME
# ══════════════════════════════════════════════════════════════════════════════
#
#  TIMING:
#  0.0 – 1.5s  → ESCENA 1: Apertura — fondo respira, partículas aparecen
#  1.5 – 7.5s  → ESCENA 2: Texto principal aparece letra a letra con líneas
#  7.5 – 10.0s → ESCENA 3: Cierre — monograma CD + tagline + fade out
#
# ── ESCENA 1: APERTURA ────────────────────────────────────────────────────────
S1_START, S1_END = 0.0,  1.5
# ── ESCENA 2: TEXTO ───────────────────────────────────────────────────────────
S2_START, S2_END = 1.5,  7.5
# ── ESCENA 3: CIERRE ──────────────────────────────────────────────────────────
S3_START, S3_END = 7.5, 10.0

print("Generando frames...")

for f in range(FRAMES):
    t      = f / FPS          # tiempo en segundos
    t_norm = f / FRAMES       # 0→1 global

    # ── Fondo ─────────────────────────────────────────────────────────────────
    img = make_gradient_bg(t_norm, variant=0).convert("RGBA")
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    draw    = ImageDraw.Draw(overlay)

    # ── ESCENA 1: Apertura ────────────────────────────────────────────────────
    if S1_START <= t < S1_END:
        prog = (t - S1_START) / (S1_END - S1_START)
        draw_particles(draw, prog, alpha_mult=ease_in_out(prog))
        draw_geometry(draw, prog,  alpha_mult=ease_in_out(prog)*0.6)

    # ── ESCENA 2: Texto principal ─────────────────────────────────────────────
    elif S2_START <= t < S2_END:
        prog = (t - S2_START) / (S2_END - S2_START)

        # Partículas se quedan pero se atenúan
        draw_particles(draw, 1.0, alpha_mult=0.35)
        draw_geometry(draw,  1.0, alpha_mult=0.4)

        # ── Línea decorativa superior (aparece primero) ───────────────────────
        line_a = ease_in_out(min(prog * 4, 1.0))
        lw     = int(line_a * 180)
        lx     = W // 2
        draw.line([(lx-lw, H//2-280), (lx+lw, H//2-280)],
                  fill=(*GOLD, int(100*line_a)), width=1)

        # ── Supertítulo "ESTÉTICA MÉDICA" ─────────────────────────────────────
        sup_a = ease_in_out(min(max(prog - 0.08, 0) * 6, 1.0))
        f_sup = font(38, "sans")
        sup   = "ESTÉTICA MÉDICA"
        bb    = draw.textbbox((0,0), sup, font=f_sup)
        sup_x = (W - (bb[2]-bb[0])) // 2
        draw.text((sup_x, H//2 - 250),
                  sup, font=f_sup,
                  fill=(*GOLD, int(180 * sup_a)))

        # ── Headline principal — aparece por palabras ─────────────────────────
        words     = ["Where", "science", "meets", "rejuvenation."]
        word_delay = 0.14   # segundos entre palabras (relativo a prog)

        f_big = font(102, "serif")
        line1 = ["Where", "science"]
        line2 = ["meets"]
        line3 = ["rejuvenation."]

        def word_alpha(word_idx, prog):
            trigger = word_idx * word_delay / (S2_END - S2_START) + 0.12
            local   = (prog - trigger) / 0.22
            return ease_in_out(max(0, min(local, 1.0)))

        # Línea 1
        for wi, word in enumerate(line1):
            a = word_alpha(wi, prog)
            if a > 0:
                f_w = font(98, "serif")
                bb  = draw.textbbox((0,0), word, font=f_w)
                # posición manual: centrar las 2 palabras juntas
                combined = "Where science"
                bb_c = draw.textbbox((0,0), combined, font=f_w)
                base_x = (W - (bb_c[2]-bb_c[0])) // 2
                if wi == 0:
                    wx = base_x
                else:
                    bb0 = draw.textbbox((0,0), "Where ", font=f_w)
                    wx  = base_x + (bb0[2]-bb0[0])
                # slide-in desde abajo muy sutilmente
                offset_y = int((1-a) * 22)
                draw.text((wx, H//2 - 150 + offset_y), word,
                          font=f_w, fill=(*DARK, int(242*a)))

        # Línea 2
        a2 = word_alpha(2, prog)
        if a2 > 0:
            f_w2 = font(98, "serif")
            bb2  = draw.textbbox((0,0), "meets", font=f_w2)
            off2 = int((1-a2)*22)
            draw.text(((W-(bb2[2]-bb2[0]))//2, H//2 + 10 + off2),
                      "meets", font=f_w2, fill=(*DARK, int(242*a2)))

        # Línea 3
        a3 = word_alpha(3, prog)
        if a3 > 0:
            f_w3   = font(86, "serif")
            txt3   = "rejuvenation."
            bb3    = draw.textbbox((0,0), txt3, font=f_w3)
            off3   = int((1-a3)*22)
            draw.text(((W-(bb3[2]-bb3[0]))//2, H//2 + 170 + off3),
                      txt3, font=f_w3,
                      fill=(*GOLD, int(210*a3)))

        # ── Línea decorativa inferior ─────────────────────────────────────────
        line_b_a = ease_in_out(min(max(prog - 0.6, 0) * 4, 1.0))
        lw2      = int(line_b_a * 120)
        draw.line([(lx-lw2, H//2+320), (lx+lw2, H//2+320)],
                  fill=(*GOLD, int(90*line_b_a)), width=1)

    # ── ESCENA 3: Cierre — Monograma CD ──────────────────────────────────────
    elif S3_START <= t <= S3_END:
        prog = (t - S3_START) / (S3_END - S3_START)

        # Fade out suave del texto anterior (overlay oscuro→blanco)
        fade_a = ease_in_out(min(prog * 1.8, 1.0))

        # Partículas desaparecen
        draw_particles(draw, 1.0, alpha_mult=max(0, 0.3 - prog*0.3))

        # ── Monograma C | D ───────────────────────────────────────────────────
        mono_a = ease_in_out(min(max(prog - 0.15, 0) * 3, 1.0))
        if mono_a > 0:
            f_mono = font(168, "serif")
            mono   = "C | D"
            bb_m   = draw.textbbox((0,0), mono, font=f_mono)
            mx     = (W - (bb_m[2]-bb_m[0])) // 2
            my     = H//2 - 110
            # Slide from below
            off_m  = int((1-mono_a) * 40)
            draw.text((mx, my + off_m), mono,
                      font=f_mono, fill=(*DARK, int(235*mono_a)))

        # ── Línea bajo monograma ───────────────────────────────────────────────
        div_a = ease_in_out(min(max(prog - 0.25, 0) * 4, 1.0))
        dw    = int(div_a * 160)
        draw.line([(W//2-dw, H//2+110), (W//2+dw, H//2+110)],
                  fill=(*GOLD, int(130*div_a)), width=1)

        # ── Tagline ───────────────────────────────────────────────────────────
        tag_a = ease_in_out(min(max(prog - 0.4, 0) * 3.5, 1.0))
        if tag_a > 0:
            f_tag = font(40, "sans")
            tag   = "LONGEVITY  ·  AESTHETICS"
            bb_t  = draw.textbbox((0,0), tag, font=f_tag)
            draw.text(((W-(bb_t[2]-bb_t[0]))//2, H//2+140),
                      tag, font=f_tag,
                      fill=(*GREY_MID, int(200*tag_a)))

        # ── Fade a negro suave al final ───────────────────────────────────────
        if prog > 0.75:
            fade_to_black = ease_in_out((prog - 0.75) / 0.25)
            draw.rectangle([(0,0),(W,H)],
                           fill=(12, 10, 8, int(200 * fade_to_black)))

    # ── Compositing ───────────────────────────────────────────────────────────
    img = Image.alpha_composite(img, overlay).convert("RGB")

    # Guardar frame
    img.save(f"{FRAMES_DIR}/frame_{f:04d}.png")

    if f % 30 == 0:
        pct = int(f / FRAMES * 100)
        print(f"  {pct}% — frame {f}/{FRAMES}")

print("Frames generados. Compilando vídeo...")

# ── COMPILAR A MP4 ────────────────────────────────────────────────────────────
from moviepy import VideoClip

frame_files = sorted([
    f"{FRAMES_DIR}/{fn}" for fn in os.listdir(FRAMES_DIR)
    if fn.startswith("frame_") and fn.endswith(".png")
])

def make_frame(t):
    fi = min(int(t * FPS), len(frame_files)-1)
    return np.array(Image.open(frame_files[fi]))

clip = VideoClip(make_frame, duration=TOTAL_S)
out  = f"{OUTPUT_DIR}/reel_carlos_duenas.mp4"
clip.write_videofile(out, fps=FPS, codec="libx264",
                     preset="slow", bitrate="8000k",
                     audio=False, logger=None)

print(f"\nVídeo guardado: {out}")
print("Para añadir música: importa el MP4 en CapCut, InShot o Premiere")
print("Música recomendada: búsca en Epidemic Sound 'minimal ambient medical'")
