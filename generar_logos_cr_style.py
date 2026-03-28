#!/usr/bin/env python3
"""
Generador de logos CD - Estilo CR Reljuvenation
6 variaciones inspiradas en: monograma bold, letra espejada,
fondo negro de lujo, tagline minimalista, acento decorativo.
Carlos Dueñas · Estética Médica
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, math

W, H = 1080, 1080
BLACK  = (8, 8, 8)
WHITE  = (255, 255, 255)
GOLD   = (196, 164, 108)
GRAY   = (160, 160, 160)
OUTPUT = "/home/user/clinica-estetica/logos_cr_style"

os.makedirs(OUTPUT, exist_ok=True)

FONT_BOLD  = "/home/user/clinica-estetica/fonts/PlayfairDisplay-Bold.ttf"
FONT_LIGHT = "/home/user/clinica-estetica/fonts/Montserrat-Light.ttf"


def canvas_dark():
    img = Image.new("RGB", (W, H), BLACK)
    draw = ImageDraw.Draw(img)
    return img, draw


def add_subtle_texture(img):
    """Añade textura sutil al fondo negro."""
    import random
    pix = img.load()
    for y in range(0, H, 3):
        for x in range(0, W, 3):
            r, g, b = pix[x, y]
            noise = random.randint(-6, 6)
            pix[x, y] = (
                max(0, min(255, r + noise)),
                max(0, min(255, g + noise)),
                max(0, min(255, b + noise)),
            )
    return img


def draw_4point_star(draw, cx, cy, size, color):
    """Estrella de 4 puntas estilo diamante."""
    pts = []
    for i in range(8):
        angle = math.radians(i * 45 - 90)
        r = size if i % 2 == 0 else size * 0.2
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(pts, fill=color)


def logo_1_cd_espejado():
    """CD con D espejada horizontalmente, igual concepto que CR referencia."""
    img, draw = canvas_dark()
    add_subtle_texture(img)

    try:
        fnt_big = ImageFont.truetype(FONT_BOLD, 380)
        fnt_tag = ImageFont.truetype(FONT_LIGHT, 36)
    except:
        fnt_big = ImageFont.load_default()
        fnt_tag = ImageFont.load_default()

    # Renderizar C
    c_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(c_img)
    c_draw.text((220, 120), "C", font=fnt_big, fill=WHITE, anchor="lt")

    # Renderizar D espejada
    d_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(d_img)
    d_draw.text((540, 120), "D", font=fnt_big, fill=WHITE, anchor="lt")
    # Espejo horizontal solo de la D: recortar, voltear, pegar
    d_crop = d_img.crop((500, 100, 1050, 650))
    d_mirror = d_crop.transpose(Image.FLIP_LEFT_RIGHT)

    # Componer
    img_rgba = img.convert("RGBA")
    img_rgba.paste(c_img, (0, 0), c_img)
    img_rgba.paste(d_mirror, (500, 100), d_mirror)

    img_final = img_rgba.convert("RGB")
    draw_final = ImageDraw.Draw(img_final)

    # Tagline
    draw_final.text((W // 2, 730), "Estética Médica", font=fnt_tag,
                    fill=GRAY, anchor="mm")

    # Línea separadora fina
    draw_final.line([(340, 710), (740, 710)], fill=GRAY, width=1)

    # Estrella decorativa esquina inferior derecha
    draw_4point_star(draw_final, 1010, 1010, 18, GRAY)

    img_final.save(f"{OUTPUT}/logo_1_cd_espejado.png")
    print("✓ logo_1_cd_espejado.png")


def logo_2_minimalista_lineal():
    """C y D solo en trazos finos (outline), muy contemporáneo."""
    img, draw = canvas_dark()
    add_subtle_texture(img)

    try:
        fnt_big = ImageFont.truetype(FONT_BOLD, 420)
        fnt_tag = ImageFont.truetype(FONT_LIGHT, 32)
        fnt_sub = ImageFont.truetype(FONT_LIGHT, 22)
    except:
        fnt_big = ImageFont.load_default()
        fnt_tag = ImageFont.load_default()
        fnt_sub  = ImageFont.load_default()

    # Crear letras sólidas y extraer contorno
    letters_img = Image.new("L", (W, H), 0)
    l_draw = ImageDraw.Draw(letters_img)
    l_draw.text((W // 2, 380), "CD", font=fnt_big, fill=255, anchor="mm")

    # Outline: dilatar - original
    from PIL import ImageFilter
    dilated = letters_img.filter(ImageFilter.MaxFilter(7))
    outline = Image.fromarray(
        __import__("numpy").clip(
            __import__("numpy").array(dilated, dtype=int) -
            __import__("numpy").array(letters_img, dtype=int), 0, 255
        ).astype("uint8")
    )

    result = img.copy()
    result.paste((220, 220, 220), mask=outline)

    draw2 = ImageDraw.Draw(result)
    draw2.text((W // 2, 700), "CARLOS DUEÑAS", font=fnt_tag,
               fill=WHITE, anchor="mm")
    draw2.text((W // 2, 740), "· ESTÉTICA MÉDICA ·", font=fnt_sub,
               fill=GRAY, anchor="mm")

    draw_4point_star(draw2, W // 2, 810, 14, GOLD)

    result.save(f"{OUTPUT}/logo_2_cd_lineal.png")
    print("✓ logo_2_cd_lineal.png")


def logo_3_sello_circular():
    """CD central con texto circular alrededor — estilo sello notarial de lujo."""
    img, draw = canvas_dark()
    add_subtle_texture(img)

    try:
        fnt_mono = ImageFont.truetype(FONT_BOLD, 320)
        fnt_circ = ImageFont.truetype(FONT_LIGHT, 28)
    except:
        fnt_mono = ImageFont.load_default()
        fnt_circ = ImageFont.load_default()

    cx, cy = W // 2, H // 2 - 20

    # Monograma CD central
    draw.text((cx, cy - 30), "CD", font=fnt_mono, fill=WHITE, anchor="mm")

    # Dos círculos concéntricos
    r1, r2 = 340, 360
    draw.ellipse([cx - r1, cy - r1, cx + r1, cy + r1], outline=GRAY, width=1)
    draw.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=GRAY, width=1)

    # Texto circular superior: "CARLOS DUEÑAS"
    text_top = "CARLOS  DUEÑAS"
    radius_text = 320
    start_angle = -math.pi * 0.75
    angle_span = math.pi * 1.5 / max(len(text_top), 1)

    for i, char in enumerate(text_top):
        angle = start_angle + i * angle_span
        tx = cx + radius_text * math.cos(angle - math.pi / 2)
        ty = cy + radius_text * math.sin(angle - math.pi / 2)
        char_angle = math.degrees(angle)
        char_img = Image.new("RGBA", (60, 60), (0, 0, 0, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((30, 30), char, font=fnt_circ, fill=WHITE, anchor="mm")
        char_rot = char_img.rotate(-char_angle, expand=False)
        img.paste(char_rot, (int(tx) - 30, int(ty) - 30), char_rot)

    # Texto circular inferior: "ESTÉTICA MÉDICA"
    text_bot = "· ESTÉTICA  MÉDICA ·"
    start_angle_bot = math.pi * 0.12
    angle_span_bot = math.pi * 0.76 / max(len(text_bot), 1)

    for i, char in enumerate(text_bot):
        angle = start_angle_bot + i * angle_span_bot
        tx = cx + radius_text * math.cos(angle - math.pi / 2)
        ty = cy + radius_text * math.sin(angle - math.pi / 2)
        char_angle = math.degrees(angle) + 180
        char_img = Image.new("RGBA", (60, 60), (0, 0, 0, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((30, 30), char, font=fnt_circ, fill=GRAY, anchor="mm")
        char_rot = char_img.rotate(-char_angle, expand=False)
        img.paste(char_rot, (int(tx) - 30, int(ty) - 30), char_rot)

    # Estrellas en los 4 puntos cardinales del círculo
    for angle_deg in [0, 90, 180, 270]:
        a = math.radians(angle_deg)
        sx = int(cx + 351 * math.cos(a))
        sy = int(cy + 351 * math.sin(a))
        draw_4point_star(draw, sx, sy, 8, GOLD)

    img.save(f"{OUTPUT}/logo_3_sello_circular.png")
    print("✓ logo_3_sello_circular.png")


def logo_4_diamante():
    """CD dentro de un rombo/diamante fino — estilo joyería de alta gama."""
    img, draw = canvas_dark()
    add_subtle_texture(img)

    try:
        fnt_mono = ImageFont.truetype(FONT_BOLD, 300)
        fnt_tag  = ImageFont.truetype(FONT_LIGHT, 30)
        fnt_sub  = ImageFont.truetype(FONT_LIGHT, 20)
    except:
        fnt_mono = ImageFont.load_default()
        fnt_tag  = ImageFont.load_default()
        fnt_sub  = ImageFont.load_default()

    cx, cy = W // 2, H // 2 - 30

    # Rombo
    margin = 280
    diamond_pts = [
        (cx, cy - margin),          # top
        (cx + margin * 0.7, cy),    # right
        (cx, cy + margin),          # bottom
        (cx - margin * 0.7, cy),    # left
    ]
    draw.polygon(diamond_pts, outline=WHITE, width=2)

    # Segundo rombo interior (decorativo)
    m2 = margin - 22
    inner_pts = [
        (cx, cy - m2),
        (cx + m2 * 0.7, cy),
        (cx, cy + m2),
        (cx - m2 * 0.7, cy),
    ]
    draw.polygon(inner_pts, outline=GRAY, width=1)

    # Monograma
    draw.text((cx, cy - 20), "CD", font=fnt_mono, fill=WHITE, anchor="mm")

    # Estrellas en los vértices del rombo
    for pt in diamond_pts:
        draw_4point_star(draw, int(pt[0]), int(pt[1]), 12, GOLD)

    # Tagline
    draw.text((cx, 820), "CARLOS DUEÑAS", font=fnt_tag, fill=WHITE, anchor="mm")
    draw.text((cx, 858), "ESTÉTICA MÉDICA", font=fnt_sub, fill=GRAY, anchor="mm")

    img.save(f"{OUTPUT}/logo_4_cd_diamante.png")
    print("✓ logo_4_cd_diamante.png")


def logo_5_grado_medico():
    """C° D — superíndice evocando precisión médica y distinción."""
    img, draw = canvas_dark()
    add_subtle_texture(img)

    try:
        fnt_c    = ImageFont.truetype(FONT_BOLD, 400)
        fnt_d    = ImageFont.truetype(FONT_BOLD, 400)
        fnt_deg  = ImageFont.truetype(FONT_BOLD, 130)
        fnt_tag  = ImageFont.truetype(FONT_LIGHT, 34)
        fnt_sub  = ImageFont.truetype(FONT_LIGHT, 22)
    except:
        fnt_c = fnt_d = fnt_deg = ImageFont.load_default()
        fnt_tag = fnt_sub = ImageFont.load_default()

    # C a la izquierda
    draw.text((270, 460), "C", font=fnt_c, fill=WHITE, anchor="mm")

    # Superíndice °
    draw.text((490, 220), "°", font=fnt_deg, fill=GOLD, anchor="mm")

    # D a la derecha
    draw.text((740, 460), "D", font=fnt_d, fill=WHITE, anchor="mm")

    # Separador fino horizontal
    draw.line([(200, 630), (880, 630)], fill=GRAY, width=1)

    # Tagline
    draw.text((W // 2, 670), "CARLOS DUEÑAS", font=fnt_tag,
               fill=WHITE, anchor="mm")
    draw.text((W // 2, 710), "MEDICINA  ESTÉTICA", font=fnt_sub,
               fill=GRAY, anchor="mm")

    # Acento dorado
    draw_4point_star(draw, W // 2, 780, 16, GOLD)

    img.save(f"{OUTPUT}/logo_5_cd_grado.png")
    print("✓ logo_5_cd_grado.png")


def logo_6_stacked_minimalista():
    """C y D apiladas verticalmente con línea dorada entre ellas."""
    img, draw = canvas_dark()
    add_subtle_texture(img)

    try:
        fnt_big  = ImageFont.truetype(FONT_BOLD, 360)
        fnt_tag  = ImageFont.truetype(FONT_LIGHT, 30)
        fnt_sub  = ImageFont.truetype(FONT_LIGHT, 20)
    except:
        fnt_big = ImageFont.load_default()
        fnt_tag = ImageFont.load_default()
        fnt_sub = ImageFont.load_default()

    cx = W // 2

    # C arriba
    draw.text((cx, 310), "C", font=fnt_big, fill=WHITE, anchor="mm")

    # Línea dorada central
    line_y = 530
    draw.line([(cx - 160, line_y), (cx + 160, line_y)], fill=GOLD, width=2)
    # Estrellas en extremos de línea
    draw_4point_star(draw, cx - 170, line_y, 10, GOLD)
    draw_4point_star(draw, cx + 170, line_y, 10, GOLD)

    # D abajo
    draw.text((cx, 760), "D", font=fnt_big, fill=WHITE, anchor="mm")

    # Tagline lateral vertical (rotado)
    tag_img = Image.new("RGBA", (300, 50), (0, 0, 0, 0))
    tag_draw = ImageDraw.Draw(tag_img)
    tag_draw.text((150, 25), "ESTÉTICA MÉDICA", font=fnt_sub,
                  fill=GRAY, anchor="mm")
    tag_rot = tag_img.rotate(90, expand=True)
    img.paste(tag_rot, (920, 390), tag_rot)

    # Nombre debajo
    draw2 = ImageDraw.Draw(img)
    draw2.text((cx, 930), "CARLOS  DUEÑAS", font=fnt_tag,
               fill=GRAY, anchor="mm")

    img.save(f"{OUTPUT}/logo_6_cd_stacked.png")
    print("✓ logo_6_cd_stacked.png")


def make_comparativa():
    """Comparativa 3x2 de los 6 logos."""
    files = [
        f"{OUTPUT}/logo_1_cd_espejado.png",
        f"{OUTPUT}/logo_2_cd_lineal.png",
        f"{OUTPUT}/logo_3_sello_circular.png",
        f"{OUTPUT}/logo_4_cd_diamante.png",
        f"{OUTPUT}/logo_5_cd_grado.png",
        f"{OUTPUT}/logo_6_cd_stacked.png",
    ]
    labels = [
        "1. CD Espejado", "2. Lineal Outline",
        "3. Sello Circular", "4. Diamante",
        "5. C° D Grado", "6. Stacked",
    ]

    COLS, ROWS = 3, 2
    THUMB = 600
    PAD = 20
    LABEL_H = 60

    cw = COLS * THUMB + (COLS + 1) * PAD
    ch = ROWS * (THUMB + LABEL_H) + (ROWS + 1) * PAD
    comp = Image.new("RGB", (cw, ch), (15, 15, 15))
    cdraw = ImageDraw.Draw(comp)

    try:
        fnt_lbl = ImageFont.truetype(FONT_LIGHT, 28)
    except:
        fnt_lbl = ImageFont.load_default()

    for i, (fpath, label) in enumerate(zip(files, labels)):
        if not os.path.exists(fpath):
            continue
        col = i % COLS
        row = i // COLS
        x = PAD + col * (THUMB + PAD)
        y = PAD + row * (THUMB + LABEL_H + PAD)

        logo = Image.open(fpath).resize((THUMB, THUMB), Image.LANCZOS)
        comp.paste(logo, (x, y))

        cdraw.text((x + THUMB // 2, y + THUMB + LABEL_H // 2),
                   label, font=fnt_lbl, fill=(180, 180, 180), anchor="mm")

    comp.save(f"{OUTPUT}/comparativa_cr_style.png")
    print("✓ comparativa_cr_style.png")


if __name__ == "__main__":
    print("Generando logos estilo CR Reljuvenation para CD...\n")
    logo_1_cd_espejado()
    logo_2_minimalista_lineal()
    logo_3_sello_circular()
    logo_4_diamante()
    logo_5_grado_medico()
    logo_6_stacked_minimalista()
    print("\nGenerando comparativa...")
    make_comparativa()
    print(f"\nTodos los logos guardados en: {OUTPUT}/")
