"""
Visualizador de Feed — Simula cómo queda el grid de Instagram
con todos los posts en orden de publicación
"""
from PIL import Image, ImageDraw, ImageFont
import os

POSTS_DIR  = "/home/user/clinica-estetica/posts"
FONTS_DIR  = "/home/user/clinica-estetica/fonts"
OUTPUT_DIR = "/home/user/clinica-estetica"

# Orden de publicación (1 = más antiguo, último = más reciente)
# Instagram muestra el más reciente arriba-izquierda
FEED_ORDER = [
    # (archivo, etiqueta_color)
    ("post_01_presentacion.png",            "CREMA"),
    ("post_02_vanidad.png",                 "MARRÓN"),
    ("FOTO_03.jpg",                         "FOTO"),   # foto propia del usuario
    ("post_06_nurse_math.png",              "CREMA"),
    ("FOTO_05.jpg",                         "FOTO"),   # foto propia del usuario
    ("post_07_precio.png",                  "OLIVA"),
    ("post_11_piel_memoria.png",            "MARRÓN"),
    ("FOTO_08.jpg",                         "FOTO"),   # foto propia del usuario
    ("post_08_testimonio.png",              "CREMA"),
    ("post_13_ciencia_naturaleza.png",      "OLIVA"),
    ("FOTO_11.jpg",                         "FOTO"),   # foto propia del usuario
    ("post_19_bienestar.png",               "CREMA"),
    ("FOTO_13.jpg",                         "FOTO"),   # foto propia del usuario
    ("post_14_5_senales_cover.png",         "CREMA"),
    ("post_16_marketing.png",               "MARRÓN"),
    ("post_12_pov_reel.png",                "CREMA"),
    ("FOTO_17.jpg",                         "FOTO"),   # foto propia del usuario
    ("post_17_ingredientes.png",            "CREMA"),
    ("post_18_franquicia_vs_especialista.png", "MALVA"),
    ("FOTO_20.jpg",                         "FOTO"),   # foto propia del usuario
    ("post_20_pregunta_correcta.png",       "OLIVA"),
    ("post_10_cta_final.png",               "MARRÓN"),
    ("FOTO_23.jpg",                         "FOTO"),   # foto propia del usuario
    ("post_14b_senal_01.png",              "CREMA"),
    ("FOTO_25.jpg",                         "FOTO"),   # foto propia del usuario
    ("post_09_flowchart.png",              "CREMA"),   # (si existe, si no placeholder)
    ("post_04_educativo.png",              "CREMA"),   # placeholder
    ("FOTO_28.jpg",                         "FOTO"),
    ("post_03_statement.png",              "MARRÓN"),  # placeholder
    ("post_05_resultado.png",              "CREMA"),   # placeholder
]

# Colores para el mapa visual
COLOR_MAP = {
    "CREMA":  (245, 240, 232),
    "MARRÓN": (58,  31,  13),
    "OLIVA":  (92, 106, 69),
    "MALVA":  (74,  32,  64),
    "FOTO":   (180, 155, 130),
}
TEXT_COLOR = {
    "CREMA":  (80,  50,  20),
    "MARRÓN": (245, 240, 232),
    "OLIVA":  (245, 240, 232),
    "MALVA":  (245, 240, 232),
    "FOTO":   (50,  30,  15),
}

CELL   = 200
GAP    = 8
COLS   = 3
HEADER = 80

rows   = (len(FEED_ORDER) + COLS - 1) // COLS
W      = COLS * CELL + (COLS + 1) * GAP
H      = rows * CELL + (rows + 1) * GAP + HEADER

img  = Image.new("RGB", (W, H), (240, 232, 220))
draw = ImageDraw.Draw(img)

try:
    f_title = ImageFont.truetype(f"{FONTS_DIR}/PlayfairDisplay-Bold.ttf", 28)
    f_small = ImageFont.truetype(f"{FONTS_DIR}/Montserrat-Light.ttf", 18)
    f_num   = ImageFont.truetype(f"{FONTS_DIR}/PlayfairDisplay-Bold.ttf", 44)
except:
    f_title = f_small = f_num = ImageFont.load_default()

# Título
draw.text((GAP, 18), "FEED MAP — Carlos Dueñas Estética Médica",
          font=f_title, fill=(44, 24, 10))
draw.text((GAP, 52), "Instagram grid · orden de publicación (1=más antiguo, últimos arriba)",
          font=f_small, fill=(120, 90, 60))

# El feed muestra el MÁS RECIENTE arriba-izquierda
# Invertimos el orden para dibujar el feed como lo ve el visitante
feed_visual = list(reversed(FEED_ORDER))

for idx, (fname, color_name) in enumerate(feed_visual):
    col = idx % COLS
    row = idx // COLS
    x   = GAP + col * (CELL + GAP)
    y   = HEADER + GAP + row * (CELL + GAP)

    bg   = COLOR_MAP[color_name]
    fg   = TEXT_COLOR[color_name]

    # Intentar cargar imagen real
    fpath = os.path.join(POSTS_DIR, fname)
    if os.path.exists(fpath):
        try:
            thumb = Image.open(fpath).convert("RGB").resize((CELL, CELL))
            img.paste(thumb, (x, y))
            # Overlay semitransparente con número
            ov = Image.new("RGBA", (CELL, CELL), (0,0,0,0))
            dov = ImageDraw.Draw(ov)
            dov.rectangle([(0, CELL-40), (CELL, CELL)], fill=(0,0,0,120))
            img.paste(ov, (x, y), mask=ov.split()[3])
            pub_num = len(FEED_ORDER) - idx  # número de publicación real
            draw.text((x + 6, y + CELL - 34),
                      f"#{pub_num}",
                      font=f_small, fill=(245, 240, 232))
            continue
        except:
            pass

    # Placeholder de color si no existe el archivo
    draw.rectangle([x, y, x+CELL, y+CELL], fill=bg)
    draw.rectangle([x, y, x+CELL, y+CELL], outline=(200,185,165), width=1)

    pub_num = len(FEED_ORDER) - idx
    # Número de publicación
    draw.text((x + CELL//2 - 18, y + CELL//2 - 40),
              f"#{pub_num}", font=f_num, fill=fg)
    # Nombre de color
    draw.text((x + 8, y + CELL - 30),
              color_name, font=f_small, fill=fg)

out_path = f"{OUTPUT_DIR}/feed_map_preview.png"
img.save(out_path)
print(f"Feed map guardado: {out_path}")
print(f"Total posts en el mapa: {len(FEED_ORDER)}")
