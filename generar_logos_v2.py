#!/usr/bin/env python3
"""
Generador de logos CD - 6 variaciones nuevas
Inspiradas en el estilo de monograma fusión (C y D casi formando un círculo)
Carlos Dueñas · Estética Médica
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import os, math

W, H = 1080, 1080
DARK   = (20, 16, 12)
WHITE  = (255, 255, 255)
GOLD   = (180, 152, 100)
CREAM  = (245, 240, 232)
MAUVE  = (74, 32, 64)
OUTPUT = "/home/user/clinica-estetica"

font_bold  = f"{OUTPUT}/fonts/PlayfairDisplay-Bold.ttf"
font_light = f"{OUTPUT}/fonts/Montserrat-Light.ttf"


def canvas(bg=WHITE):
    img = Image.new("RGB", (W, H), bg)
    return img, ImageDraw.Draw(img)


def save_dual(img_white, name):
    """Guarda versión fondo blanco y fondo oscuro."""
    img_white.save(f"{OUTPUT}/logo_v2_{name}_blanco.png")
    # Fondo oscuro: invertir colores del logo
    dark_bg = Image.new("RGB", (W, H), DARK)
    # Crear versión inverted para fondo oscuro
    logo_mask = img_white.copy()
    logo_dark = Image.new("RGB", (W, H), DARK)
    for y in range(H):
        for x in range(W):
            r, g, b = img_white.getpixel((x, y))
            if r < 200 and g < 200 and b < 200:  # pixel oscuro → blanco
                logo_dark.putpixel((x, y), WHITE)
            else:
                logo_dark.putpixel((x, y), DARK)
    logo_dark.save(f"{OUTPUT}/logo_v2_{name}_oscuro.png")
    print(f"  ✓ logo_v2_{name}_blanco/oscuro.png")


def make_stripe(img, draw, y, label, color=DARK):
    """Label pequeño debajo del logo."""
    try:
        fnt = ImageFont.truetype(font_light, 28)
        draw.text((W//2, y), label, font=fnt, fill=color, anchor="mm")
    except:
        pass

# ─────────────────────────────────────────────
# LOGO 1 · FUSIÓN ARCO  (inspirado en la referencia)
# C y D como arcos muy gruesos, casi formando un círculo
# ─────────────────────────────────────────────
def logo1_fusion_arco():
    img, draw = canvas(WHITE)
    cx, cy = W // 2, H // 2
    r = 290
    stroke = 88
    gap = 24  # separación entre letras

    # C: arco izquierdo, apertura a la derecha (35°→325° clockwise)
    c_cx = cx - gap // 2
    draw.arc(
        [c_cx - r, cy - r, c_cx + r, cy + r],
        start=38, end=322, fill=DARK, width=stroke
    )

    # D: arco derecho (espejo de C) → apertura a la izquierda (218°→142° cw = 218→360→142)
    d_cx = cx + gap // 2
    draw.arc(
        [d_cx - r, cy - r, d_cx + r, cy + r],
        start=218, end=142, fill=DARK, width=stroke
    )

    img.save(f"{OUTPUT}/logo_v2_1_fusion_arco.png")
    print("  ✓ logo_v2_1_fusion_arco.png")


# ─────────────────────────────────────────────
# LOGO 2 · SERIF LIGATURA
# C y D en Playfair Display Bold, kerning cero, muy grande
# ─────────────────────────────────────────────
def logo2_serif_ligatura():
    img, draw = canvas(WHITE)
    try:
        fnt = ImageFont.truetype(font_bold, 540)
        fnt_sub = ImageFont.truetype(font_light, 32)
    except:
        fnt = ImageFont.load_default()
        fnt_sub = fnt

    # Medir letras individualmente
    bb_c = draw.textbbox((0, 0), "C", font=fnt)
    bb_d = draw.textbbox((0, 0), "D", font=fnt)
    w_c = bb_c[2] - bb_c[0]
    w_d = bb_d[2] - bb_d[0]
    total_w = w_c + w_d - 20  # solapamiento ligero

    x_start = (W - total_w) // 2
    y_center = H // 2

    # Ajuste vertical (las fuentes tienen descenders)
    bb_full = draw.textbbox((0, 0), "CD", font=fnt)
    text_h = bb_full[3] - bb_full[1]
    y_top = y_center - text_h // 2 - bb_full[1]

    draw.text((x_start - bb_c[0], y_top), "C", font=fnt, fill=DARK)
    draw.text((x_start + w_c - 20 - bb_d[0], y_top), "D", font=fnt, fill=DARK)

    # Línea decorativa dorada debajo
    line_y = y_center + text_h // 2 + 40
    draw.line([(W//2 - 120, line_y), (W//2 + 120, line_y)], fill=GOLD, width=3)

    # Subtítulo
    draw.text((W//2, line_y + 30), "ESTÉTICA MÉDICA", font=fnt_sub, fill=GOLD, anchor="mm")

    img.save(f"{OUTPUT}/logo_v2_2_serif_ligatura.png")
    print("  ✓ logo_v2_2_serif_ligatura.png")


# ─────────────────────────────────────────────
# LOGO 3 · CÍRCULO NEGATIVO
# CD blanco recortado en círculo negro sólido
# ─────────────────────────────────────────────
def logo3_circulo_negativo():
    img, draw = canvas(WHITE)
    cx, cy = W // 2, H // 2
    r_circle = 370

    # Círculo oscuro sólido
    draw.ellipse([cx - r_circle, cy - r_circle, cx + r_circle, cy + r_circle], fill=DARK)

    # CD en blanco encima, grande
    try:
        fnt = ImageFont.truetype(font_bold, 400)
        fnt_sub = ImageFont.truetype(font_light, 36)
    except:
        fnt = ImageFont.load_default()
        fnt_sub = fnt

    bb = draw.textbbox((0, 0), "CD", font=fnt)
    x = cx - (bb[2] - bb[0]) // 2 - bb[0]
    y = cy - (bb[3] - bb[1]) // 2 - bb[1]
    draw.text((x, y - 20), "CD", font=fnt, fill=WHITE)

    # Línea fina + subtítulo en blanco
    draw.line([(cx - 100, cy + 200), (cx + 100, cy + 200)], fill=GOLD, width=2)
    draw.text((cx, cy + 228), "CARLOS DUEÑAS", font=fnt_sub, fill=GOLD, anchor="mm")

    img.save(f"{OUTPUT}/logo_v2_3_circulo_negativo.png")
    print("  ✓ logo_v2_3_circulo_negativo.png")


# ─────────────────────────────────────────────
# LOGO 4 · TRAZO FINO GEOMÉTRICO
# C y D construidas con arcos muy finos, estilo arquitectónico
# ─────────────────────────────────────────────
def logo4_geometrico_fino():
    img, draw = canvas(WHITE)
    cx, cy = W // 2, H // 2
    r = 280
    stroke = 22  # trazo fino, elegante
    gap = 30

    # C: arco fino izquierdo
    c_cx = cx - gap // 2
    draw.arc(
        [c_cx - r, cy - r, c_cx + r, cy + r],
        start=38, end=322, fill=DARK, width=stroke
    )

    # D: arco fino derecho (espejo)
    d_cx = cx + gap // 2
    draw.arc(
        [d_cx - r, cy - r, d_cx + r, cy + r],
        start=218, end=142, fill=DARK, width=stroke
    )

    # Punto central decorativo dorado
    dot_r = 10
    draw.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=GOLD)

    # Líneas horizontales estructurales (top y bottom)
    y_top  = cy - r + stroke // 2
    y_bot  = cy + r - stroke // 2
    draw.line([(cx - 60, y_top), (cx + 60, y_top)], fill=DARK, width=2)
    draw.line([(cx - 60, y_bot), (cx + 60, y_bot)], fill=DARK, width=2)

    # Subtítulo
    try:
        fnt_sub = ImageFont.truetype(font_light, 34)
        fnt_ini = ImageFont.truetype(font_bold, 120)
    except:
        fnt_sub = fnt_ini = ImageFont.load_default()

    # Iniciales dentro (pequeñas, apenas visibles)
    draw.text((cx - 68, cy), "C", font=fnt_ini, fill=(180, 175, 168), anchor="mm")
    draw.text((cx + 68, cy), "D", font=fnt_ini, fill=(180, 175, 168), anchor="mm")

    draw.text((cx, cy + r + 70), "CARLOS DUEÑAS", font=fnt_sub, fill=DARK, anchor="mm")
    draw.text((cx, cy + r + 108), "ESTÉTICA MÉDICA", font=fnt_sub, fill=GOLD, anchor="mm")

    img.save(f"{OUTPUT}/logo_v2_4_geometrico_fino.png")
    print("  ✓ logo_v2_4_geometrico_fino.png")


# ─────────────────────────────────────────────
# LOGO 5 · SELLO ROMBO  (Diamond Badge)
# CD en rombo / diamante con borde fino
# ─────────────────────────────────────────────
def logo5_sello_rombo():
    img, draw = canvas(WHITE)
    cx, cy = W // 2, H // 2
    size = 380  # semidiagonal del rombo

    # Rombo exterior
    diamond = [
        (cx, cy - size),
        (cx + size * 0.72, cy),
        (cx, cy + size),
        (cx - size * 0.72, cy),
    ]
    draw.polygon(diamond, outline=DARK, width=4)

    # Rombo interior (doble borde)
    inner = 16
    diamond_in = [
        (cx, cy - size + inner),
        (cx + (size - inner) * 0.72, cy),
        (cx, cy + size - inner),
        (cx - (size - inner) * 0.72, cy),
    ]
    draw.polygon(diamond_in, outline=DARK, width=1)

    # CD grande dentro
    try:
        fnt = ImageFont.truetype(font_bold, 340)
        fnt_sub = ImageFont.truetype(font_light, 30)
    except:
        fnt = ImageFont.load_default()
        fnt_sub = fnt

    bb = draw.textbbox((0, 0), "CD", font=fnt)
    x = cx - (bb[2] - bb[0]) // 2 - bb[0]
    y = cy - (bb[3] - bb[1]) // 2 - bb[1] - 15
    draw.text((x, y), "CD", font=fnt, fill=DARK)

    # Texto superior e inferior en el rombo
    draw.text((cx, cy - size + 80), "CARLOS", font=fnt_sub, fill=DARK, anchor="mm")
    draw.text((cx, cy + size - 80), "DUEÑAS", font=fnt_sub, fill=DARK, anchor="mm")

    img.save(f"{OUTPUT}/logo_v2_5_sello_rombo.png")
    print("  ✓ logo_v2_5_sello_rombo.png")


# ─────────────────────────────────────────────
# LOGO 6 · MONOGRAMA ENTRELAZADO
# C y D se solapan en el centro compartiendo espacio
# ─────────────────────────────────────────────
def logo6_entrelazado():
    img, draw = canvas(WHITE)
    cx, cy = W // 2, H // 2
    r = 310
    stroke = 72
    overlap = 80  # cuánto se solapan (offset hacia el centro)

    # C: centrado pero desplazado a la derecha para solapar con D
    c_cx = cx + overlap // 2
    draw.arc(
        [c_cx - r, cy - r, c_cx + r, cy + r],
        start=38, end=322, fill=DARK, width=stroke
    )

    # D: desplazado a la izquierda para solapar con C
    d_cx = cx - overlap // 2
    draw.arc(
        [d_cx - r, cy - r, d_cx + r, cy + r],
        start=218, end=142, fill=DARK, width=stroke
    )

    # Barra vertical de la D
    bar_left = d_cx - r + stroke // 2 - 4
    draw.rectangle(
        [bar_left - stroke // 2, cy - r + stroke // 4,
         bar_left + stroke // 2, cy + r - stroke // 4],
        fill=DARK
    )

    # Línea dorada decorativa centrada horizontal
    draw.line([(cx - 160, cy - r - 50), (cx + 160, cy - r - 50)], fill=GOLD, width=3)
    draw.line([(cx - 160, cy + r + 50), (cx + 160, cy + r + 50)], fill=GOLD, width=3)

    # Subtítulos
    try:
        fnt_sub = ImageFont.truetype(font_light, 34)
    except:
        fnt_sub = ImageFont.load_default()

    draw.text((cx, cy - r - 86), "CARLOS  DUEÑAS", font=fnt_sub, fill=DARK, anchor="mm")
    draw.text((cx, cy + r + 86), "ESTÉTICA MÉDICA", font=fnt_sub, fill=GOLD, anchor="mm")

    img.save(f"{OUTPUT}/logo_v2_6_entrelazado.png")
    print("  ✓ logo_v2_6_entrelazado.png")


# ─────────────────────────────────────────────
# PREVIEW COMPARATIVO (3x2 grid)
# ─────────────────────────────────────────────
def make_grid():
    logos = [
        f"{OUTPUT}/logo_v2_1_fusion_arco.png",
        f"{OUTPUT}/logo_v2_2_serif_ligatura.png",
        f"{OUTPUT}/logo_v2_3_circulo_negativo.png",
        f"{OUTPUT}/logo_v2_4_geometrico_fino.png",
        f"{OUTPUT}/logo_v2_5_sello_rombo.png",
        f"{OUTPUT}/logo_v2_6_entrelazado.png",
    ]
    labels = [
        "V1 · FUSIÓN ARCO",
        "V2 · SERIF LIGATURA",
        "V3 · CÍRCULO NEGATIVO",
        "V4 · GEOMÉTRICO FINO",
        "V5 · SELLO ROMBO",
        "V6 · ENTRELAZADO",
    ]
    cols, rows = 3, 2
    thumb = 540
    pad = 20
    label_h = 60
    GW = cols * thumb + (cols + 1) * pad
    GH = rows * (thumb + label_h) + (rows + 1) * pad + 120

    grid = Image.new("RGB", (GW, GH), (248, 246, 243))
    gd   = ImageDraw.Draw(grid)
    try:
        fnt_label = ImageFont.truetype(font_light, 28)
        fnt_title = ImageFont.truetype(font_bold,  52)
    except:
        fnt_label = fnt_title = ImageFont.load_default()

    gd.text((GW // 2, 55), "MONOGRAMAS CD", font=fnt_title, fill=DARK, anchor="mm")
    gd.text((GW // 2, 95), "Carlos Dueñas · Estética Médica · selecciona tu favorito",
            font=fnt_label, fill=(120, 110, 100), anchor="mm")

    for i, (path, label) in enumerate(zip(logos, labels)):
        col = i % cols
        row = i // cols
        x = pad + col * (thumb + pad)
        y = 120 + pad + row * (thumb + label_h + pad)

        if os.path.exists(path):
            logo = Image.open(path).resize((thumb, thumb), Image.LANCZOS)
        else:
            logo = Image.new("RGB", (thumb, thumb), (200, 190, 180))

        grid.paste(logo, (x, y))
        # Marco fino
        gd.rectangle([x - 1, y - 1, x + thumb, y + thumb], outline=(200, 195, 190), width=1)
        # Número
        gd.rectangle([x + 10, y + 10, x + 50, y + 44], fill=DARK)
        gd.text((x + 30, y + 27), str(i + 1), font=fnt_label, fill=WHITE, anchor="mm")
        # Label
        gd.text((x + thumb // 2, y + thumb + label_h // 2),
                label, font=fnt_label, fill=DARK, anchor="mm")

    out_path = f"{OUTPUT}/logos_v2_comparativa.png"
    grid.save(out_path)
    print(f"  ✓ logos_v2_comparativa.png")


# ─────────────────────────────────────────────
print("Generando logos V2...")
logo1_fusion_arco()
logo2_serif_ligatura()
logo3_circulo_negativo()
logo4_geometrico_fino()
logo5_sello_rombo()
logo6_entrelazado()
print("Generando comparativa...")
make_grid()
print("¡Listo!")
