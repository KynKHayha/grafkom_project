# -*- coding: utf-8 -*-
"""
Generate semua asset gambar untuk Journey to Knowledge
Jalankan sekali: python generate_assets.py
"""
import os
import math
from PIL import Image, ImageDraw, ImageFilter

os.makedirs("assets/textures", exist_ok=True)

def save(img, name):
    path = f"assets/textures/{name}"
    img.save(path)
    print(f"  [OK] {path} ({img.size[0]}x{img.size[1]})")

print("Generating assets...")

# ── 1. WALL TEXTURE (bata merah-coklat) ────────────────
img = Image.new("RGB", (128,128), (80,45,22))
d = ImageDraw.Draw(img)
for row in range(0,128,20):
    offset = 32 if (row//20)%2 else 0
    d.line([(0,row),(128,row)], fill=(110,65,32), width=3)
    for col in range(-offset,128+40,40):
        d.line([(col,row),(col,row+20)], fill=(110,65,32), width=3)
        d.rectangle([col+3,row+3,col+36,row+16], fill=(95,55,25))
        # Highlight bata
        d.line([(col+3,row+3),(col+36,row+3)], fill=(120,75,40), width=1)
img = img.filter(ImageFilter.SMOOTH)
save(img, "wall.png")

# ── 2. FLOOR TEXTURE (lantai marmer hijau) ─────────────
img = Image.new("RGB", (128,128), (45,65,38))
d = ImageDraw.Draw(img)
for i in range(0,128,16):
    d.line([(i,0),(i,128)], fill=(55,78,45), width=1)
    d.line([(0,i),(128,i)], fill=(55,78,45), width=1)
for i in range(0,128,32):
    for j in range(0,128,32):
        d.ellipse([i+8,j+8,i+24,j+24], fill=(50,72,40))
save(img, "floor.png")

# ── 3. CEILING TEXTURE (langit bintang) ────────────────
img = Image.new("RGB", (128,128), (8,10,30))
d = ImageDraw.Draw(img)
import random; random.seed(42)
for _ in range(80):
    x,y = random.randint(0,127), random.randint(0,127)
    br = random.randint(150,255)
    r = random.randint(1,3)
    d.ellipse([x-r,y-r,x+r,y+r], fill=(br,br,255))
save(img, "ceiling.png")

# ── 4. BOOK SPRITE ─────────────────────────────────────
img = Image.new("RGBA", (96,96), (0,0,0,0))
d = ImageDraw.Draw(img)
# Badan buku
d.rectangle([8,4,88,92], fill=(200,40,40), outline=(140,20,20), width=2)
# Spine (punggung buku)
d.rectangle([8,4,24,92], fill=(240,80,80), outline=(180,40,40), width=1)
# Halaman
for y in range(18,92,10):
    d.line([(26,y),(86,y)], fill=(255,160,160), width=1)
# Judul
d.rectangle([28,20,84,50], fill=(180,25,25))
d.text((30,25), "BUKU\nILMU", fill=(255,220,180))
# Highlight
d.line([(10,6),(22,6)], fill=(255,150,150), width=2)
save(img, "book.png")

# ── 5. PENCIL SPRITE ───────────────────────────────────
img = Image.new("RGBA", (96,96), (0,0,0,0))
d = ImageDraw.Draw(img)
# Badan pensil
d.polygon([(38,4),(58,4),(58,82),(48,96),(38,82)], fill=(255,220,50), outline=(200,170,20), width=2)
# Ujung (kayu)
d.polygon([(38,82),(58,82),(48,96)], fill=(230,185,130), outline=(180,140,80))
# Garis badan
d.line([(38,4),(38,82)], fill=(200,165,20), width=2)
d.line([(58,4),(58,82)], fill=(200,165,20), width=2)
# Penghapus merah
d.rectangle([36,0,60,10], fill=(255,150,180), outline=(200,100,140))
d.line([(36,10),(60,10)], fill=(180,130,50), width=2)
# Garis-garis teks pada pensil
for y in range(20,80,12):
    d.line([(40,y),(56,y)], fill=(180,140,15), width=1)
save(img, "pencil.png")

# ── 6. GRADUATION CAP ──────────────────────────────────
img = Image.new("RGBA", (96,96), (0,0,0,0))
d = ImageDraw.Draw(img)
# Papan toga (persegi miring)
pts = [(48,8),(88,30),(48,52),(8,30)]
d.polygon(pts, fill=(60,40,180), outline=(40,25,140), width=2)
# Highlight papan
d.line([(48,8),(88,30)], fill=(100,80,220), width=2)
d.line([(48,8),(8,30)], fill=(100,80,220), width=2)
# Tali toga (kuning)
d.line([(88,30),(92,65)], fill=(255,200,50), width=4)
d.ellipse([86,62,98,76], fill=(255,200,50), outline=(200,150,20))
# Silinder bawah
d.ellipse([22,46,74,70], fill=(50,32,160), outline=(40,25,130))
d.rectangle([22,56,74,70], fill=(50,32,160))
save(img, "graduation_cap.png")

# ── 7. ENEMY SPRITE ────────────────────────────────────
img = Image.new("RGBA", (96,96), (0,0,0,0))
d = ImageDraw.Draw(img)
# Badan monster
d.ellipse([8,18,88,90], fill=(140,30,200), outline=(100,15,160), width=3)
# Highlight badan
d.ellipse([14,22,50,55], fill=(180,60,240), outline=None)
# Mata kiri (menyala merah)
d.ellipse([18,28,42,52], fill=(255,50,50), outline=(200,20,20), width=2)
d.ellipse([24,34,36,46], fill=(255,200,50))
d.ellipse([28,38,32,42], fill=(255,255,255))
# Mata kanan
d.ellipse([54,28,78,52], fill=(255,50,50), outline=(200,20,20), width=2)
d.ellipse([60,34,72,46], fill=(255,200,50))
d.ellipse([64,38,68,42], fill=(255,255,255))
# Mulut
d.arc([24,58,72,80], start=0, end=180, fill=(50,10,80), width=4)
for tx in [32,40,48,56,64]:
    d.line([(tx,68),(tx,76)], fill=(50,10,80), width=2)
# Tanduk kiri
d.polygon([(20,20),(10,4),(30,18)], fill=(120,20,180), outline=(80,10,130))
# Tanduk kanan
d.polygon([(76,20),(86,4),(66,18)], fill=(120,20,180), outline=(80,10,130))
save(img, "enemy.png")

# ── 8. PLAYER ICON (minimap) ───────────────────────────
img = Image.new("RGBA", (64,64), (0,0,0,0))
d = ImageDraw.Draw(img)
d.ellipse([8,8,56,56], fill=(80,160,255), outline=(50,120,220), width=3)
d.polygon([(32,12),(52,52),(32,44),(12,52)], fill=(50,120,220))
save(img, "player.png")

# ── 9. GROUND (lantai outdoor 2D backup) ───────────────
img = Image.new("RGB", (128,64), (50,90,40))
d = ImageDraw.Draw(img)
for i in range(0,128,6):
    h = random.randint(4,12)
    d.line([(i,0),(i-2,-h)], fill=(60+random.randint(0,20),110+random.randint(0,20),40))
    d.line([(i,0),(i+2,-h)], fill=(60+random.randint(0,20),110+random.randint(0,20),40))
save(img, "ground.png")

# ── 10. SKY ────────────────────────────────────────────
img = Image.new("RGB", (256,128))
d = ImageDraw.Draw(img)
for y in range(128):
    t = y/128
    r = int(5*(1-t)+15*t); g=int(8*(1-t)+25*t); b=int(28*(1-t)+80*t)
    d.line([(0,y),(256,y)], fill=(r,g,b))
for _ in range(100):
    x,y = random.randint(0,255), random.randint(0,60)
    br = random.randint(160,255)
    r = random.randint(0,2)
    d.ellipse([x-r,y-r,x+r,y+r], fill=(br,br,255))
# Bulan
d.ellipse([200,10,240,50], fill=(255,248,200))
d.ellipse([210,8,246,44], fill=(8,14,35))
save(img, "sky.png")

print(f"\nSemua asset berhasil dibuat di folder assets/textures/")
print("Total:", len(os.listdir("assets/textures")), "file")
