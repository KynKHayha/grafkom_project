# -*- coding: utf-8 -*-
"""
Asset Generator untuk Journey to Knowledge
Membuat semua texture yang dibutuhkan menggunakan Pillow
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import math

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def generate_ground_texture():
    """Texture tanah/lantai sekolah - motif keramik biru muda"""
    img = Image.new('RGB', (256, 256), color=(220, 235, 255))
    draw = ImageDraw.Draw(img)
    
    # Grid keramik
    for x in range(0, 256, 64):
        for y in range(0, 256, 64):
            draw.rectangle([x+1, y+1, x+62, y+62], fill=(200, 220, 250), outline=(160, 190, 230), width=2)
            # Highlight pojok
            draw.rectangle([x+3, y+3, x+15, y+15], fill=(230, 240, 255))
    
    img.save('assets/textures/ground.png')
    print("[OK] ground.png generated")

def generate_sky_texture():
    """Texture langit gradasi biru ke ungu (langit pengetahuan)"""
    img = Image.new('RGB', (512, 512))
    draw = ImageDraw.Draw(img)
    
    for y in range(512):
        ratio = y / 512
        r = int(20 + ratio * 100)
        g = int(30 + ratio * 80)
        b = int(80 + ratio * 120)
        draw.line([(0, y), (512, y)], fill=(r, g, b))
    
    # Bintang/partikel
    import random
    random.seed(42)
    for _ in range(80):
        x = random.randint(0, 511)
        y = random.randint(0, 300)
        size = random.randint(1, 3)
        draw.ellipse([x-size, y-size, x+size, y+size], fill=(255, 255, 200))
    
    img.save('assets/textures/sky.png')
    print("[OK] sky.png generated")

def generate_book_texture():
    """Texture buku merah dengan detail"""
    img = Image.new('RGB', (128, 128), color=(180, 30, 30))
    draw = ImageDraw.Draw(img)
    
    # Cover depan
    draw.rectangle([10, 5, 118, 123], fill=(200, 40, 40), outline=(120, 10, 10), width=3)
    # Spine
    draw.rectangle([0, 0, 12, 128], fill=(140, 20, 20))
    # Garis halaman
    for i in range(3):
        y = 30 + i * 20
        draw.line([(20, y), (110, y)], fill=(255, 200, 200), width=2)
    # Simbol bintang/ilmu
    draw.text((50, 60), "★", fill=(255, 220, 50))
    
    img.save('assets/textures/book.png')
    print("[OK] book.png generated")

def generate_coin_texture():
    """Texture koin pengetahuan - emas dengan simbol graduation cap"""
    img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Lingkaran emas (menggunakan algoritma lingkaran)
    cx, cy = 64, 64
    r = 58
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(255, 200, 30), outline=(200, 140, 0), width=4)
    
    # Inner circle
    draw.ellipse([cx-45, cy-45, cx+45, cy+45], fill=(255, 215, 50))
    
    # Simbol buku/graduation
    draw.rectangle([34, 44, 94, 84], fill=(180, 90, 0), outline=(120, 50, 0), width=2)
    draw.text((48, 55), "📚", fill=(255, 255, 200))
    
    img.save('assets/textures/coin.png')
    print("[OK] coin.png generated")

def generate_wall_texture():
    """Texture dinding sekolah - bata putih modern"""
    img = Image.new('RGB', (256, 256), color=(240, 240, 245))
    draw = ImageDraw.Draw(img)
    
    # Bata pattern
    brick_h = 32
    brick_w = 64
    for row in range(8):
        offset = (brick_w // 2) if row % 2 == 1 else 0
        y = row * brick_h
        for col in range(-1, 5):
            x = col * brick_w + offset
            draw.rectangle([x+2, y+2, x+brick_w-2, y+brick_h-2], 
                          fill=(235, 235, 242), outline=(200, 200, 215), width=2)
    
    img.save('assets/textures/wall.png')
    print("[OK] wall.png generated")

def generate_platform_texture():
    """Texture platform melayang - kayu dengan efek cahaya"""
    img = Image.new('RGB', (256, 64), color=(139, 90, 43))
    draw = ImageDraw.Draw(img)
    
    # Serat kayu
    for i in range(0, 64, 8):
        offset = (i % 16) * 2
        draw.line([(offset, i), (256+offset, i+2)], fill=(120, 75, 30), width=1)
        draw.line([(offset+30, i+4), (256+offset+30, i+6)], fill=(160, 110, 60), width=1)
    
    # Top highlight
    draw.rectangle([0, 0, 256, 6], fill=(180, 130, 70))
    # Bottom shadow
    draw.rectangle([0, 58, 256, 64], fill=(80, 50, 20))
    
    img.save('assets/textures/platform.png')
    print("[OK] platform.png generated")

def generate_enemy_texture():
    """Texture musuh - monster kebodohan, warna gelap"""
    img = Image.new('RGB', (128, 128), color=(50, 20, 80))
    draw = ImageDraw.Draw(img)
    
    # Badan gelap
    draw.ellipse([10, 10, 118, 118], fill=(70, 30, 110), outline=(30, 10, 60), width=3)
    # Mata merah
    draw.ellipse([30, 35, 55, 60], fill=(255, 50, 50))
    draw.ellipse([73, 35, 98, 60], fill=(255, 50, 50))
    draw.ellipse([38, 43, 47, 52], fill=(255, 0, 0))
    draw.ellipse([81, 43, 90, 52], fill=(255, 0, 0))
    # Mulut jahat
    draw.arc([35, 65, 93, 95], start=0, end=180, fill=(200, 0, 0), width=4)
    # Simbol X (kebodohan)
    draw.text((50, 10), "✗", fill=(255, 80, 80))
    
    img.save('assets/textures/enemy.png')
    print("[OK] enemy.png generated")

def generate_player_texture():
    """Texture player - siswa dengan seragam"""
    img = Image.new('RGB', (128, 128), color=(100, 149, 237))
    draw = ImageDraw.Draw(img)
    
    # Kepala
    draw.ellipse([44, 5, 84, 45], fill=(255, 218, 185), outline=(200, 160, 120), width=2)
    # Rambut
    draw.ellipse([44, 5, 84, 25], fill=(60, 40, 20))
    # Badan (seragam putih-biru)
    draw.rectangle([34, 45, 94, 95], fill=(240, 240, 255), outline=(100, 100, 200), width=2)
    # Dasi merah
    draw.polygon([(60, 50), (68, 50), (65, 85), (63, 85)], fill=(200, 30, 30))
    # Kaki
    draw.rectangle([38, 95, 58, 125], fill=(50, 50, 150))
    draw.rectangle([70, 95, 90, 125], fill=(50, 50, 150))
    # Sepatu
    draw.rectangle([35, 120, 60, 128], fill=(30, 20, 10))
    draw.rectangle([68, 120, 93, 128], fill=(30, 20, 10))
    
    img.save('assets/textures/player.png')
    print("[OK] player.png generated")

def generate_star_texture():
    """Texture bintang - partikel efek"""
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Bintang 5 sudut
    cx, cy = 32, 32
    points = []
    for i in range(10):
        angle = math.pi * i / 5 - math.pi / 2
        r = 28 if i % 2 == 0 else 12
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))
    
    draw.polygon(points, fill=(255, 230, 0, 230), outline=(255, 180, 0, 255))
    draw.polygon(points[:5:2] + points[1::2], fill=(255, 245, 100, 180))
    
    img.save('assets/textures/star.png')
    print("[OK] star.png generated")

def generate_background_panel():
    """Panel UI background"""
    img = Image.new('RGBA', (400, 100), (20, 10, 50, 200))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([2, 2, 398, 98], radius=15, fill=(30, 20, 70, 210), outline=(100, 80, 200, 255), width=2)
    img.save('assets/textures/panel.png')
    print("[OK] panel.png generated")

def generate_pencil_texture():
    """Texture pensil kuning"""
    img = Image.new('RGB', (64, 128), color=(255, 220, 50))
    draw = ImageDraw.Draw(img)
    
    # Badan pensil
    draw.rectangle([15, 10, 49, 100], fill=(255, 215, 30), outline=(200, 150, 0), width=2)
    # Ujung pensil
    draw.polygon([(15, 100), (49, 100), (32, 120)], fill=(200, 150, 100))
    draw.polygon([(24, 105), (40, 105), (32, 118)], fill=(50, 30, 10))
    # Penghapus merah
    draw.rectangle([15, 5, 49, 18], fill=(255, 100, 100), outline=(200, 50, 50), width=1)
    # Garis tengah
    draw.line([(32, 10), (32, 100)], fill=(220, 180, 0), width=2)
    
    img.save('assets/textures/pencil.png')
    print("[OK] pencil.png generated")

def generate_quote_bg():
    """Background untuk quote pendidikan"""
    img = Image.new('RGBA', (600, 150), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Gradient gelap transparan
    for y in range(150):
        alpha = int(180 * (1 - abs(y - 75) / 75))
        r, g, b = 10, 5, 40
        draw.line([(0, y), (600, y)], fill=(r, g, b, alpha))
    
    draw.rounded_rectangle([5, 5, 595, 145], radius=20, outline=(150, 100, 255, 200), width=2)
    
    img.save('assets/textures/quote_bg.png')
    print("[OK] quote_bg.png generated")

def generate_graduation_cap_texture():
    """Texture toga/graduation cap - item spesial"""
    img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Papan toga (hitam)
    draw.polygon([(10, 55), (118, 55), (118, 45), (10, 45)], fill=(20, 20, 20))
    # Lingkaran tengah
    draw.ellipse([40, 35, 88, 73], fill=(30, 30, 30), outline=(80, 80, 80), width=2)
    # Tali kuning
    draw.line([(64, 54), (64, 100)], fill=(255, 200, 0), width=4)
    draw.ellipse([56, 98, 72, 114], fill=(255, 180, 0))
    # Kilap
    draw.ellipse([44, 38, 56, 48], fill=(80, 80, 80, 150))
    
    img.save('assets/textures/graduation_cap.png')
    print("[OK] graduation_cap.png generated")

if __name__ == '__main__':
    # Buat direktori assets
    ensure_dir('assets/textures')
    ensure_dir('assets/sounds')
    ensure_dir('assets/models')
    
    print("[*] Generating game assets...")
    print("=" * 40)
    
    generate_ground_texture()
    generate_sky_texture()
    generate_book_texture()
    generate_coin_texture()
    generate_wall_texture()
    generate_platform_texture()
    generate_enemy_texture()
    generate_player_texture()
    generate_star_texture()
    generate_background_panel()
    generate_pencil_texture()
    generate_quote_bg()
    generate_graduation_cap_texture()
    
    print("=" * 40)
    print("[OK] All assets generated successfully!")
    print("[>] Location: assets/textures/")
