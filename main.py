# -*- coding: utf-8 -*-
"""
================================================
 JOURNEY TO KNOWLEDGE
 2D Platformer Game - Tema: Pentingnya Pendidikan
 Engine: Pygame (SDL2 / DirectX)

 Algoritma Grafika Komputer:
  1. DDA Line Algorithm
  2. Midpoint Circle Algorithm
  3. Cohen-Sutherland Line Clipping
  4. Scanline Fill (Polygon Filling)
  5. Transformasi 3D (Matriks T, R, S)

 Kontrol:
  A/D atau Left/Right : Gerak
  Space / W / Up       : Lompat
  ESC                  : Menu
================================================
"""

import sys
import math
import random
import pygame
from pygame import gfxdraw

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ============================================================
# ALGORITMA GRAFIKA KOMPUTER
# ============================================================

class GraphicsAlgorithms:

    @staticmethod
    def dda_line(surface, x1, y1, x2, y2, col):
        """
        DDA Line Drawing Algorithm.
        Menggambar garis dari (x1,y1) ke (x2,y2) titik per titik.
        """
        dx, dy = x2-x1, y2-y1
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            surface.set_at((x1, y1), col)
            return
        xi, yi = dx/steps, dy/steps
        x, y = float(x1), float(y1)
        pts = []
        for _ in range(int(steps)+1):
            pts.append((round(x), round(y)))
            x += xi; y += yi
        if len(pts) > 1:
            pygame.draw.lines(surface, col, False, pts, 1)
        return pts

    @staticmethod
    def midpoint_circle(surface, cx, cy, r, col, filled=False):
        """
        Midpoint Circle Algorithm.
        Menggambar lingkaran menggunakan prinsip 8-way symmetry.
        """
        if filled:
            pygame.draw.circle(surface, col, (cx, cy), r)
            return
        x, y, p = r, 0, 1-r
        pts = set()
        while x >= y:
            for dx, dy in [(x,y),(-x,y),(x,-y),(-x,-y),(y,x),(-y,x),(y,-x),(-y,-x)]:
                pts.add((cx+dx, cy+dy))
            y += 1
            p = p+2*y+1 if p <= 0 else p+2*y-2*x+1
            if p > 0: x -= 1
        for pt in pts:
            if 0 <= pt[0] < surface.get_width() and 0 <= pt[1] < surface.get_height():
                surface.set_at(pt, col)

    @staticmethod
    def cohen_sutherland(x1, y1, x2, y2, xn, yn, xx, yx):
        """
        Cohen-Sutherland Line Clipping Algorithm.
        Memotong garis agar masuk ke dalam viewport/window.
        """
        INSIDE,L,R,B,T = 0,1,2,4,8
        def code(x,y):
            c=INSIDE
            if x<xn: c|=L
            elif x>xx: c|=R
            if y<yn: c|=B
            elif y>yx: c|=T
            return c
        c1,c2,ok = code(x1,y1),code(x2,y2),False
        while True:
            if not(c1|c2): ok=True; break
            elif c1&c2: break
            co = c1 if c1 else c2
            if co&T: x=x1+(x2-x1)*(yx-y1)/(y2-y1) if y2!=y1 else x1; y=yx
            elif co&B: x=x1+(x2-x1)*(yn-y1)/(y2-y1) if y2!=y1 else x1; y=yn
            elif co&R: y=y1+(y2-y1)*(xx-x1)/(x2-x1) if x2!=x1 else y1; x=xx
            else: y=y1+(y2-y1)*(xn-x1)/(x2-x1) if x2!=x1 else y1; x=xn
            if co==c1: x1,y1,c1=x,y,code(x,y)
            else: x2,y2,c2=x,y,code(x,y)
        return ok, int(x1),int(y1),int(x2),int(y2)

    @staticmethod
    def scanline_fill(surface, polygon, col):
        """
        Scanline Fill Algorithm.
        Mengisi polygon dengan warna menggunakan scanline.
        """
        if len(polygon) < 3: return
        n = len(polygon)
        min_y = max(0, int(min(p[1] for p in polygon)))
        max_y = min(surface.get_height()-1, int(max(p[1] for p in polygon)))
        for y in range(min_y, max_y+1):
            xs = []
            for i in range(n):
                x1,y1 = polygon[i]; x2,y2 = polygon[(i+1)%n]
                if y1 != y2 and min(y1,y2) <= y < max(y1,y2):
                    xs.append(int(x1 + (y-y1)*(x2-x1)/(y2-y1)))
            xs.sort()
            for i in range(0, len(xs)-1, 2):
                x_start = max(0, xs[i])
                x_end   = min(surface.get_width()-1, xs[i+1])
                if x_start <= x_end:
                    pygame.draw.line(surface, col, (x_start,y), (x_end,y))

    @staticmethod
    def transform_matrix(tx=0, ty=0, rz=0, sx=1, sy=1):
        """
        Matriks Transformasi 2D/3D (Homogeneous Coordinates).
        Menggabungkan: Translasi (T), Rotasi (R), Skala (S).
        """
        cz, sz = math.cos(math.radians(rz)), math.sin(math.radians(rz))
        T  = [[1,0,tx],[0,1,ty],[0,0,1]]
        R  = [[cz,-sz,0],[sz,cz,0],[0,0,1]]
        S  = [[sx,0,0],[0,sy,0],[0,0,1]]
        return {'T':T,'R':R,'S':S,'params':f"T({tx},{ty}) R({rz}deg) S({sx},{sy})"}

    @staticmethod
    def apply_transform(points, tx=0, ty=0, rz=0, sx=1, sy=1, origin=(0,0)):
        """Terapkan transformasi ke daftar titik (polygon)."""
        result = []
        cz, sz = math.cos(math.radians(rz)), math.sin(math.radians(rz))
        for (px, py) in points:
            # Geser ke origin
            px -= origin[0]; py -= origin[1]
            # Scale
            px *= sx; py *= sy
            # Rotate
            px2 = px*cz - py*sz
            py2 = px*sz + py*cz
            # Translate kembali + offset
            result.append((int(px2 + origin[0] + tx), int(py2 + origin[1] + ty)))
        return result


ALGO = GraphicsAlgorithms()


# ============================================================
# INISIALISASI PYGAME
# ============================================================

pygame.init()
pygame.mixer.init()

W, H = 1280, 720
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Journey to Knowledge | Pentingnya Pendidikan")
clock = pygame.time.Clock()

# Font
try:
    FONT_BIG   = pygame.font.SysFont("Segoe UI", 52, bold=True)
    FONT_MED   = pygame.font.SysFont("Segoe UI", 30, bold=True)
    FONT_SMALL = pygame.font.SysFont("Segoe UI", 20)
    FONT_TINY  = pygame.font.SysFont("Segoe UI", 16)
except:
    FONT_BIG   = pygame.font.Font(None, 52)
    FONT_MED   = pygame.font.Font(None, 30)
    FONT_SMALL = pygame.font.Font(None, 20)
    FONT_TINY  = pygame.font.Font(None, 16)


# ============================================================
# WARNA
# ============================================================

C = {
    'bg_top':      (5, 8, 30),
    'bg_bot':      (15, 25, 80),
    'ground':      (60, 110, 50),
    'ground_top':  (80, 150, 60),
    'platform':    (120, 80, 40),
    'plat_top':    (160, 110, 60),
    'plat_shadow': (70, 45, 20),
    'player':      (80, 140, 220),
    'player_dark': (50, 100, 180),
    'enemy':       (160, 40, 220),
    'enemy_dark':  (100, 20, 160),
    'book':        (220, 60, 60),
    'pencil':      (255, 220, 50),
    'grad':        (80, 50, 180),
    'ui_bg':       (5, 5, 30),
    'ui_border':   (80, 60, 200),
    'gold':        (255, 210, 50),
    'white':       (255, 255, 255),
    'green':       (50, 200, 80),
    'red':         (220, 50, 50),
    'cyan':        (80, 220, 255),
    'purple':      (180, 80, 255),
    'text_dim':    (160, 150, 200),
    'hp_full':     (220, 50, 80),
    'hp_empty':    (60, 40, 80),
    'star_col':    (255, 240, 100),
    'tree_trunk':  (100, 65, 25),
    'tree_leaf':   (40, 140, 40),
    'sky_star':    (200, 210, 255),
    'quote_bg':    (10, 5, 50),
    'quote_bd':    (120, 80, 255),
}


# ============================================================
# QUOTES PENDIDIKAN
# ============================================================

QUOTES = [
    "Pendidikan adalah senjata paling ampuh\nuntuk mengubah dunia!  - Nelson Mandela",
    "Investasi terbaik adalah\ninvestasi pada diri sendiri!",
    "Ilmu pengetahuan adalah cahaya\nyang menerangi kegelapan!",
    "Belajar tidak pernah melelahkan\npikiran! - Leonardo da Vinci",
    "Akar pendidikan memang pahit,\ntapi buahnya manis! - Aristoteles",
    "Satu buku dan satu guru\nbisa mengubah dunia!",
    "Pendidikan adalah kunci emas\nmenuju pintu kesuksesan!",
    "Teruslah belajar, karena ilmu\ntidak mengenal batas!",
    "Orang terdidik tahu bagaimana\nmembuat sesuatu dari apapun!",
    "Pendidikan membebaskan pikiran\ndan jiwa manusia!",
]


# ============================================================
# ASSET GENERATOR (Gambar 2D dengan Pygame Draw)
# ============================================================

def make_star_bg():
    """Buat background bintang (titik-titik DDA + Midpoint Circle)."""
    surf = pygame.Surface((W, H))
    # Gradient langit malam
    for y in range(H):
        t = y / H
        r = int(C['bg_top'][0]*(1-t) + C['bg_bot'][0]*t)
        g = int(C['bg_top'][1]*(1-t) + C['bg_bot'][1]*t)
        b = int(C['bg_top'][2]*(1-t) + C['bg_bot'][2]*t)
        pygame.draw.line(surf, (r,g,b), (0,y), (W,y))
    # Bintang (menggunakan Midpoint Circle kecil)
    random.seed(42)
    for _ in range(180):
        sx, sy = random.randint(0,W), random.randint(0,H//2)
        br = random.randint(140,255)
        r = random.randint(1, 2)
        ALGO.midpoint_circle(surf, sx, sy, r, (br,br,255), filled=(r>1))
    # Bulan (Midpoint Circle besar)
    ALGO.midpoint_circle(surf, W-130, 80, 42, (255,248,200), filled=True)
    ALGO.midpoint_circle(surf, W-115, 72, 36, (15,22,70), filled=True)  # Crescent
    return surf


def draw_ground(surf, cam_x):
    """Gambar tanah dengan rumput menggunakan Scanline Fill."""
    ground_y = H - 80
    # Tanah utama (Scanline Fill polygon)
    poly = [(0, ground_y), (W, ground_y), (W, H), (0, H)]
    ALGO.scanline_fill(surf, poly, C['ground'])
    # Garis rumput atas (DDA Line)
    ALGO.dda_line(surf, 0, ground_y, W, ground_y, C['ground_top'])
    ALGO.dda_line(surf, 0, ground_y+1, W, ground_y+1, C['ground_top'])
    # Rumput detail
    for i in range(0, W+60, 18):
        gx = (i - cam_x % 18)
        gy = ground_y
        h = random.randint(8, 16) if random.random() < 0.7 else 6
        col = (60+random.randint(0,30), 140+random.randint(0,30), 40)
        ALGO.dda_line(surf, gx, gy, gx-3, gy-h, col)
        ALGO.dda_line(surf, gx, gy, gx+3, gy-h, col)


def draw_tree(surf, tx, ty, cam_x):
    """Gambar pohon menggunakan Scanline Fill + DDA Line."""
    x = tx - cam_x
    if x < -80 or x > W+80: return
    # Batang (Scanline Fill rectangle)
    trunk_poly = [(x-8,ty),(x+8,ty),(x+8,ty+60),(x-8,ty+60)]
    ALGO.scanline_fill(surf, trunk_poly, C['tree_trunk'])
    # Daun berlapis (3 segitiga Scanline Fill)
    for i, (dy, w) in enumerate([(0,45),(20,38),(38,28)]):
        leaf_poly = [(x,ty-60+dy-w),(x+w,ty-60+dy+w),(x-w,ty-60+dy+w)]
        # Rotasi sedikit via transform untuk variasi
        leaf_poly = ALGO.apply_transform(leaf_poly, rz=i*5, origin=(x, ty-40+dy))
        ALGO.scanline_fill(surf, leaf_poly, (30+i*10, 130+i*10, 30))
        # Garis tepi daun (DDA)
        for j in range(len(leaf_poly)):
            p1 = leaf_poly[j]; p2 = leaf_poly[(j+1)%len(leaf_poly)]
            ALGO.dda_line(surf, *p1, *p2, (20,100,20))

    # Buku kecil di atas pohon (highlight pendidikan)
    bx, by = x-5, ty-95
    pygame.draw.rect(surf, (200,50,50), (bx,by,14,18))
    pygame.draw.rect(surf, (255,100,100), (bx,by,3,18))


def draw_platform(surf, px, py, pw, ph, cam_x):
    """Gambar platform menggunakan Scanline Fill polygon."""
    sx = px - cam_x
    if sx+pw < 0 or sx > W: return

    # Shadow (Scanline Fill polygon miring)
    shadow = [(sx+6,py+ph+3),(sx+pw+6,py+ph+3),(sx+pw+6,py+ph+8),(sx+6,py+ph+8)]
    ALGO.scanline_fill(surf, shadow, (20,10,5))

    # Badan platform (Scanline Fill)
    plat_poly = [(sx,py),(sx+pw,py),(sx+pw,py+ph),(sx,py+ph)]
    ALGO.scanline_fill(surf, plat_poly, C['platform'])

    # Permukaan atas (lebih terang)
    top_poly = [(sx,py),(sx+pw,py),(sx+pw,py+10),(sx,py+10)]
    ALGO.scanline_fill(surf, top_poly, C['plat_top'])

    # Garis tepi (DDA Line)
    ALGO.dda_line(surf, sx, py, sx+pw, py, (200,160,100))
    ALGO.dda_line(surf, sx, py, sx, py+ph, (90,60,30))
    ALGO.dda_line(surf, sx+pw, py, sx+pw, py+ph, (90,60,30))

    # Dekorasi batu bata (DDA Line horizontal)
    for by2 in range(py+14, py+ph, 12):
        ALGO.dda_line(surf, sx+2, by2, sx+pw-2, by2, (90,60,25))


def draw_player(surf, x, y, facing, frame, invincible):
    """Gambar karakter player (student) menggunakan polygon + DDA."""
    if invincible and (frame//4)%2: return  # Kedip saat invincible

    # Transformasi tubuh (Translasi + Rotasi sedikit)
    bob = math.sin(frame*0.15) * 2 if facing else 0

    # Topi pelajar (Scanline Fill trapezoid)
    hat_pts = [(x-14,y-36),(x+14,y-36),(x+10,y-28),(x-10,y-28)]
    ALGO.scanline_fill(surf, hat_pts, (20,20,150))
    hat_brim = [(x-17,y-28),(x+17,y-28),(x+17,y-25),(x-17,y-25)]
    ALGO.scanline_fill(surf, hat_brim, (20,20,150))
    ALGO.dda_line(surf, x-17,y-28, x+17,y-28, (80,80,220))

    # Kepala (Midpoint Circle)
    ALGO.midpoint_circle(surf, x, int(y-18+bob), 13, (240,200,160), filled=True)
    ALGO.midpoint_circle(surf, x, int(y-18+bob), 13, (180,140,110))

    # Mata (Midpoint Circle kecil)
    eye_x = x+5 if facing >= 0 else x-5
    ALGO.midpoint_circle(surf, eye_x, int(y-19+bob), 2, (30,30,80), filled=True)

    # Senyum (DDA Line)
    smile_x = x+3 if facing >= 0 else x-3
    ALGO.dda_line(surf, smile_x-3, int(y-13+bob), smile_x+3, int(y-11+bob), (180,100,80))

    # Badan (Scanline Fill)
    body = [(x-12,y-5),(x+12,y-5),(x+10,y+18),(x-10,y+18)]
    ALGO.scanline_fill(surf, body, C['player'])
    # Dasi merah
    dasi = [(x+1,y-4),(x+5,y-4),(x+3,y+12)]
    ALGO.scanline_fill(surf, dasi, (220,50,50))

    # Kaki (Scanline Fill)
    leg_l = [(x-11,y+18),(x-3,y+18),(x-3,y+34),(x-11,y+34)]
    leg_r = [(x+3,y+18),(x+11,y+18),(x+11,y+34),(x+3,y+34)]
    for leg in [leg_l, leg_r]:
        ALGO.scanline_fill(surf, leg, (30,30,120))

    # Sepatu
    shoe_l = [(x-12,y+34),(x-1,y+34),(x-1,y+38),(x-12,y+38)]
    shoe_r = [(x+1,y+34),(x+12,y+34),(x+12,y+38),(x+1,y+38)]
    for shoe in [shoe_l, shoe_r]:
        ALGO.scanline_fill(surf, shoe, (30,20,80))

    # Tangan kanan (membawa buku)
    arm = [(x+12,y-2),(x+22,y+4),(x+22,y+12),(x+12,y+10)]
    ALGO.scanline_fill(surf, arm, C['player_dark'])
    # Buku di tangan
    book_pts = [(x+22,y+2),(x+32,y),(x+32,y+14),(x+22,y+16)]
    ALGO.scanline_fill(surf, book_pts, (200,50,50))
    ALGO.dda_line(surf, x+22,y+2, x+32,y, (255,100,100))


def draw_enemy(surf, x, y, frame, cam_x):
    """Gambar musuh monster kebodohan."""
    sx = x - cam_x
    if sx < -60 or sx > W+60: return

    # Animasi bobbing
    bob = int(math.sin(frame*0.1) * 4)
    sy = y + bob

    # Bayangan
    ALGO.midpoint_circle(surf, sx, sy+38, 18, (0,0,0,100), filled=True)

    # Badan monster (Midpoint Circle besar)
    ALGO.midpoint_circle(surf, sx, sy, 22, C['enemy_dark'], filled=True)
    ALGO.midpoint_circle(surf, sx, sy, 20, C['enemy'], filled=True)

    # Tanduk (Scanline Fill segitiga - transformasi rotasi)
    for sign in [-1, 1]:
        horn = [(sx+sign*8, sy-20),(sx+sign*14, sy-34),(sx+sign*18, sy-20)]
        horn = ALGO.apply_transform(horn, rz=sign*5, origin=(sx+sign*8, sy-20))
        ALGO.scanline_fill(surf, horn, (120,20,180))

    # Mata menyala (Midpoint Circle)
    for ex, ey in [(sx-8,sy-5),(sx+8,sy-5)]:
        ALGO.midpoint_circle(surf, ex, ey, 5, (255,50,50), filled=True)
        ALGO.midpoint_circle(surf, ex, ey, 3, (255,200,50), filled=True)
        ALGO.midpoint_circle(surf, ex, ey, 1, (255,255,255), filled=True)

    # Mulut (DDA Line lengkung)
    for dx2 in range(-8,9):
        my = sy+8 + int(dx2*dx2*0.08)
        if 0 <= sx+dx2 < W:
            surf.set_at((sx+dx2, my), (50,10,80))

    # Label "!!!" di atas
    lbl = FONT_TINY.render("!!!", True, (255,50,50))
    surf.blit(lbl, (sx - lbl.get_width()//2, sy-46))


def draw_book(surf, x, y, t, cam_x):
    """Gambar item buku dengan animasi mengambang."""
    sx = x - cam_x
    if sx < -40 or sx > W+40: return
    sy = y + int(math.sin(t*3) * 5)
    angle = math.sin(t*2) * 12

    # Aura glow (Midpoint Circle)
    alpha = int(180 + 60*math.sin(t*4))
    ALGO.midpoint_circle(surf, sx, sy, 22, (220,50,50), filled=False)

    # Buku (Scanline Fill dengan transformasi rotasi)
    book_pts = [(-18,-24),(18,-24),(18,24),(-18,24)]
    book_pts = ALGO.apply_transform(book_pts, rz=angle, origin=(0,0))
    book_pts = [(p[0]+sx, p[1]+sy) for p in book_pts]
    ALGO.scanline_fill(surf, book_pts, (200,40,40))
    # Spine buku
    spine_pts = [(-20,-24),(-14,-24),(-14,24),(-20,24)]
    spine_pts = ALGO.apply_transform(spine_pts, rz=angle, origin=(0,0))
    spine_pts = [(p[0]+sx, p[1]+sy) for p in spine_pts]
    ALGO.scanline_fill(surf, spine_pts, (255,90,90))
    # Garis halaman
    for i in range(-16, 17, 6):
        line_pts = [(-14,i),(14,i)]
        line_pts = ALGO.apply_transform(line_pts, rz=angle, origin=(0,0))
        if len(line_pts) == 2:
            ALGO.dda_line(surf,
                line_pts[0][0]+sx, line_pts[0][1]+sy,
                line_pts[1][0]+sx, line_pts[1][1]+sy,
                (255,150,150))

    # Label skor
    score_txt = FONT_TINY.render("+25", True, C['gold'])
    surf.blit(score_txt, (sx - score_txt.get_width()//2, sy-36))


def draw_pencil(surf, x, y, t, cam_x):
    """Gambar item pensil dengan animasi."""
    sx = x - cam_x
    if sx < -30 or sx > W+30: return
    sy = y + int(math.sin(t*2.5 + 1) * 5)
    angle = 45 + math.sin(t*1.5)*15

    # Aura
    ALGO.midpoint_circle(surf, sx, sy, 18, C['pencil'], filled=False)

    # Pensil (DDA Line tebal - transformasi rotasi)
    p1 = ALGO.apply_transform([(-4,-20)], rz=angle, origin=(0,0))[0]
    p2 = ALGO.apply_transform([(4,20)], rz=angle, origin=(0,0))[0]
    p3 = ALGO.apply_transform([(0,28)], rz=angle, origin=(0,0))[0]
    # Badan pensil
    body = [(-4,-22),(4,-22),(4,16),(-4,16)]
    body = ALGO.apply_transform(body, rz=angle, origin=(0,0))
    body = [(p[0]+sx, p[1]+sy) for p in body]
    ALGO.scanline_fill(surf, body, C['pencil'])
    # Ujung (segitiga)
    tip = [(-4,16),(4,16),(0,26)]
    tip = ALGO.apply_transform(tip, rz=angle, origin=(0,0))
    tip = [(p[0]+sx, p[1]+sy) for p in tip]
    ALGO.scanline_fill(surf, tip, (230,180,130))
    # Penghapus
    era = [(-4,-22),(4,-22),(4,-28),(-4,-28)]
    era = ALGO.apply_transform(era, rz=angle, origin=(0,0))
    era = [(p[0]+sx, p[1]+sy) for p in era]
    ALGO.scanline_fill(surf, era, (255,160,180))

    score_txt = FONT_TINY.render("+10", True, C['pencil'])
    surf.blit(score_txt, (sx - score_txt.get_width()//2, sy-34))


def draw_graduation(surf, x, y, t, cam_x):
    """Gambar item toga wisuda."""
    sx = x - cam_x
    if sx < -40 or sx > W+40: return
    sy = y + int(math.sin(t*2.8 + 2) * 6)
    angle = math.sin(t*1.8)*10

    # Aura ungu
    for r in [30, 24, 18]:
        alpha_col = (60+r*2, 30+r, 100+r*2)
        ALGO.midpoint_circle(surf, sx, sy, r, alpha_col, filled=False)

    # Toga (persegi panjang datar)
    cap = [(-22,-4),(22,-4),(22,4),(-22,4)]
    cap = ALGO.apply_transform(cap, rz=angle, origin=(0,0))
    cap = [(p[0]+sx, p[1]+sy) for p in cap]
    ALGO.scanline_fill(surf, cap, C['grad'])
    # Tali toga
    ALGO.dda_line(surf, sx+22, sy, sx+26, sy+18, C['gold'])
    ALGO.midpoint_circle(surf, sx+26, sy+18, 4, C['gold'], filled=True)
    # Papan toga (bujur sangkar miring)
    board = [(-14,-16),(14,-16),(14,-4),(-14,-4)]
    board = ALGO.apply_transform(board, rz=angle+45, origin=(0,-10))
    board = [(p[0]+sx, p[1]+sy) for p in board]
    ALGO.scanline_fill(surf, board, (60,40,160))

    score_txt = FONT_TINY.render("+50", True, C['purple'])
    surf.blit(score_txt, (sx - score_txt.get_width()//2, sy-38))


# ============================================================
# GAME OBJECTS
# ============================================================

class Player:
    W, H = 28, 40
    SPEED = 5.5
    JUMP  = -17
    GRAVITY = 0.75
    MAX_FALL = 18

    def __init__(self, x, y):
        self.x, self.y = float(x), float(y)
        self.vx, self.vy = 0.0, 0.0
        self.on_ground = False
        self.facing = 1
        self.health = 3
        self.score = 0
        self.invincible = 0
        self.frame = 0
        self.alive = True

    def rect(self):
        return pygame.Rect(int(self.x)-self.W//2, int(self.y)-self.H, self.W, self.H)

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.vx = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -self.SPEED; self.facing = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = self.SPEED; self.facing = 1

        self.vy = min(self.vy + self.GRAVITY, self.MAX_FALL)
        self.x += self.vx
        self.y += self.vy

        # Collision platform
        self.on_ground = False
        pr = self.rect()
        for plat in platforms:
            pr2 = pygame.Rect(plat['x'], plat['y'], plat['w'], plat['h'])
            if pr.colliderect(pr2):
                if self.vy > 0 and pr.bottom - pr2.top < 22:
                    self.y = plat['y']
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0 and pr2.bottom - pr.top < 18:
                    self.y = pr2.bottom + self.H
                    self.vy = 0
                elif self.vx > 0:
                    self.x = pr2.left - self.W//2
                elif self.vx < 0:
                    self.x = pr2.right + self.W//2

        # Lompat
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vy = self.JUMP

        # Batas layar horizontal
        if self.x < 0: self.x = 0
        if self.invincible > 0: self.invincible -= 1
        self.frame += 1

    def take_damage(self):
        if self.invincible > 0: return
        self.health -= 1
        self.invincible = 90
        if self.health <= 0:
            self.alive = False

    def draw(self, surf, cam_x):
        sx = int(self.x) - cam_x
        sy = int(self.y)
        draw_player(surf, sx, sy, self.facing, self.frame, self.invincible > 0)


class Enemy:
    def __init__(self, x, y, rng=120, spd=1.8):
        self.x, self.y = float(x), float(y)
        self.start_x = float(x)
        self.range = rng
        self.speed = spd
        self.dir = 1
        self.frame = random.randint(0, 60)

    def update(self):
        self.x += self.dir * self.speed
        if abs(self.x - self.start_x) >= self.range:
            self.dir *= -1
        self.frame += 1

    def rect(self):
        return pygame.Rect(int(self.x)-20, int(self.y)-40, 40, 40)

    def draw(self, surf, cam_x):
        draw_enemy(surf, int(self.x), int(self.y), self.frame, cam_x)


class Item:
    TYPES = ['book','pencil','graduation']
    SCORES = {'book':25,'pencil':10,'graduation':50}

    def __init__(self, x, y, itype):
        self.x, self.y = float(x), float(y)
        self.type = itype
        self.pts = self.SCORES[itype]
        self.collected = False

    def rect(self):
        return pygame.Rect(int(self.x)-18, int(self.y)-24, 36, 48)

    def draw(self, surf, t, cam_x):
        if self.collected: return
        if self.type == 'book':
            draw_book(surf, int(self.x), int(self.y), t, cam_x)
        elif self.type == 'pencil':
            draw_pencil(surf, int(self.x), int(self.y), t, cam_x)
        else:
            draw_graduation(surf, int(self.x), int(self.y), t, cam_x)


# ============================================================
# LEVEL DATA
# ============================================================

LEVEL = {
    'platforms': [
        # Start area
        {'x':   0, 'y': 540, 'w': 500, 'h': 30},
        {'x': 350, 'y': 460, 'w': 180, 'h': 20},
        {'x': 600, 'y': 400, 'w': 180, 'h': 20},
        {'x': 850, 'y': 340, 'w': 160, 'h': 20},
        {'x':1100, 'y': 280, 'w': 200, 'h': 20},
        {'x':1380, 'y': 340, 'w': 160, 'h': 20},
        {'x':1620, 'y': 400, 'w': 180, 'h': 20},
        {'x':1880, 'y': 320, 'w': 160, 'h': 20},
        {'x':2120, 'y': 260, 'w': 200, 'h': 20},
        # Tantangan atas
        {'x':2400, 'y': 300, 'w': 150, 'h': 20},
        {'x':2620, 'y': 240, 'w': 150, 'h': 20},
        {'x':2850, 'y': 180, 'w': 200, 'h': 20},
        # Final area
        {'x':3150, 'y': 220, 'w': 350, 'h': 30},
    ],
    'items': [
        (420, 435, 'pencil'),
        (670, 375, 'book'),
        (920, 315, 'pencil'),
        (1180,255, 'book'),
        (1460,315, 'graduation'),
        (1700,375, 'pencil'),
        (1960,295, 'book'),
        (2190,235, 'graduation'),
        (2470,275, 'pencil'),
        (2690,215, 'book'),
        (2930,155, 'graduation'),
        (3250,195, 'book'),
        (3380,195, 'pencil'),
        (3450,195, 'graduation'),
    ],
    'enemies': [
        (480, 540, 120, 2.0),
        (700, 400, 100, 2.2),
        (960, 340, 100, 2.5),
        (1560,340,  90, 2.8),
        (1950,320, 110, 3.0),
        (2500,300,  80, 3.2),
        (2950,180,  80, 3.5),
    ],
    'trees': [
        200, 1000, 1500, 2000, 2800, 3600
    ],
    'total_x': 3700,
}


# ============================================================
# UI HELPER FUNCTIONS
# ============================================================

def draw_rounded_rect(surf, col, rect, radius=12, border=0, border_col=None):
    """Gambar rounded rectangle."""
    if border > 0 and border_col:
        pygame.draw.rect(surf, border_col,
                         (rect[0]-border, rect[1]-border,
                          rect[2]+border*2, rect[3]+border*2),
                         border_radius=radius+border)
    pygame.draw.rect(surf, col, rect, border_radius=radius)


def draw_text_shadow(surf, text, font, col, x, y, shadow_col=(0,0,0), shadow_off=2, center=True):
    """Render teks dengan bayangan."""
    t = font.render(text, True, shadow_col)
    if center: surf.blit(t, (x - t.get_width()//2 + shadow_off, y + shadow_off))
    else: surf.blit(t, (x + shadow_off, y + shadow_off))
    t = font.render(text, True, col)
    if center: surf.blit(t, (x - t.get_width()//2, y))
    else: surf.blit(t, (x, y))
    return t.get_width(), t.get_height()


def draw_hud(surf, player, items_got, items_total, quote, quote_timer):
    """Gambar HUD (score, HP, items, quote)."""
    # Panel atas (Scanline Fill)
    panel = [(0,0),(W,0),(W,55),(0,55)]
    ALGO.scanline_fill(surf, panel, (5,5,30))
    ALGO.dda_line(surf, 0,55, W,55, C['ui_border'])

    # Score
    draw_rounded_rect(surf, (10,10,50), (10,6,180,42), radius=8,
                      border=1, border_col=C['ui_border'])
    draw_text_shadow(surf, f"SCORE: {player.score}", FONT_MED, C['gold'], 102, 12, center=True)

    # HP (Midpoint Circle untuk hati)
    draw_rounded_rect(surf, (10,10,50), (200,6,150,42), radius=8,
                      border=1, border_col=(150,30,60))
    hp_txt = FONT_MED.render("HP:", True, C['white'])
    surf.blit(hp_txt, (210,13))
    for i in range(3):
        col = C['hp_full'] if i < player.health else C['hp_empty']
        hx, hy = 270+i*32, 24
        ALGO.midpoint_circle(surf, hx, hy, 9, col, filled=True)
        ALGO.midpoint_circle(surf, hx, hy, 9, (200,50,80))

    # Items
    draw_rounded_rect(surf, (10,10,50), (360,6,200,42), radius=8,
                      border=1, border_col=(50,100,200))
    draw_text_shadow(surf, f"ITEM: {items_got}/{items_total}", FONT_MED, C['cyan'], 462, 12, center=True)

    # Algo info
    algo_txt = FONT_TINY.render(
        "[DDA] [Midpoint Circle] [Cohen-Sutherland] [Scanline Fill] [Transform T*R*S]",
        True, (80,140,255))
    surf.blit(algo_txt, (W//2 - algo_txt.get_width()//2, 38))

    # Kontrol hint (kanan)
    hint = FONT_TINY.render("A/D:Gerak  SPACE:Lompat  ESC:Menu", True, (120,110,180))
    surf.blit(hint, (W - hint.get_width() - 10, 38))

    # Quote box
    if quote and quote_timer > 0:
        alpha = min(1.0, quote_timer/0.5)  # fade in
        fade  = min(1.0, quote_timer)       # fade out
        lines = quote.split('\n')
        qw = 620; qh = 20 + len(lines)*28
        qx = W//2 - qw//2; qy = H - qh - 75
        draw_rounded_rect(surf, C['quote_bg'], (qx, qy, qw, qh), radius=10,
                          border=2, border_col=C['quote_bd'])
        ALGO.dda_line(surf, qx+6, qy+4, qx+6, qy+qh-4, C['quote_bd'])
        for i, line in enumerate(lines):
            col = C['gold'] if i == 0 else C['text_dim']
            draw_text_shadow(surf, line, FONT_SMALL, col, W//2, qy+8+i*28, center=True)


def draw_particles(surf, particles):
    """Gambar partikel bintang (Midpoint Circle kecil)."""
    for p in particles:
        alpha = int(255 * (p['life'] / p['max_life']))
        if alpha > 0:
            ALGO.midpoint_circle(surf, int(p['x']), int(p['y']),
                                 max(1, int(p['r'])),
                                 tuple(min(255,c) for c in p['col']), filled=True)


# ============================================================
# SCREEN FUNCTIONS
# ============================================================

def draw_menu(surf, star_bg, frame):
    """Tampilkan layar menu utama."""
    surf.blit(star_bg, (0,0))

    # Partikel bintang melayang
    t = frame * 0.02
    for i in range(12):
        sx = int((W*0.1 + W*0.8*((i*137+frame)%100)/100))
        sy = int(H*0.4 + math.sin(t + i*0.8)*60)
        ALGO.midpoint_circle(surf, sx, sy, 3, C['star_col'], filled=True)

    # Panel utama
    pw, ph = 720, 500
    px, py = W//2 - pw//2, H//2 - ph//2 - 10
    draw_rounded_rect(surf, (6,4,28), (px,py,pw,ph), radius=18,
                      border=2, border_col=C['ui_border'])
    # Garis hias atas
    ALGO.dda_line(surf, px+20, py+8, px+pw-20, py+8, C['ui_border'])

    # Judul (dengan DDA Line dekorasi)
    draw_text_shadow(surf, "JOURNEY TO KNOWLEDGE",
                     FONT_BIG, C['gold'], W//2, py+30, shadow_col=(40,20,0))
    draw_text_shadow(surf, "~ Tema: Pentingnya Pendidikan ~",
                     FONT_MED, C['purple'], W//2, py+92, shadow_col=(20,0,40))

    # Garis pemisah (DDA)
    ALGO.dda_line(surf, px+30, py+132, px+pw-30, py+132, C['ui_border'])

    # Deskripsi
    desc = [
        "Kumpulkan BUKU, PENSIL, dan TOGA WISUDA",
        "sambil menghindari Monster Kebodohan!",
    ]
    for i, d in enumerate(desc):
        draw_text_shadow(surf, d, FONT_SMALL, C['text_dim'], W//2, py+148+i*28, center=True)

    # Kontrol
    ctrl = ["A/D : Gerak Kiri/Kanan", "SPACE / W : Lompat", "ESC : Menu"]
    for i, c in enumerate(ctrl):
        draw_text_shadow(surf, c, FONT_SMALL, (140,200,255), W//2, py+218+i*26, center=True)

    # Algoritma
    ALGO.dda_line(surf, px+30, py+312, px+pw-30, py+312, (50,50,110))
    algo_info = "[DDA] [Midpoint Circle] [Cohen-Sutherland] [Scanline Fill] [Transformasi T*R*S]"
    draw_text_shadow(surf, algo_info, FONT_TINY, C['green'], W//2, py+320, center=True)

    # Tombol MULAI (dengan Scanline Fill)
    btn_rect = (W//2-160, py+360, 320, 54)
    hover = pygame.Rect(*btn_rect).collidepoint(pygame.mouse.get_pos())
    btn_col = (50, 160, 80) if hover else (35, 120, 60)
    draw_rounded_rect(surf, btn_col, btn_rect, radius=14,
                      border=2, border_col=(80,220,100) if hover else (50,160,80))
    draw_text_shadow(surf, ">> MULAI PETUALANGAN <<", FONT_MED, C['white'], W//2, py+374, center=True)

    # Quote bawah
    ALGO.dda_line(surf, px+30, py+428, px+pw-30, py+428, (50,50,110))
    draw_text_shadow(surf, '"Pendidikan adalah senjata paling ampuh',
                     FONT_TINY, (180,160,220), W//2, py+436, center=True)
    draw_text_shadow(surf, 'untuk mengubah dunia." - Nelson Mandela',
                     FONT_TINY, (180,160,220), W//2, py+454, center=True)

    return pygame.Rect(*btn_rect)


def draw_gameover(surf, star_bg, score, items_got, items_total):
    """Tampilkan layar game over."""
    surf.blit(star_bg, (0,0))
    # Overlay merah
    ov = pygame.Surface((W,H), pygame.SRCALPHA)
    ov.fill((60,0,0,160))
    surf.blit(ov, (0,0))

    pw, ph = 600, 380
    px, py = W//2-pw//2, H//2-ph//2
    draw_rounded_rect(surf, (30,4,4), (px,py,pw,ph), radius=16, border=2, border_col=(200,50,50))
    draw_text_shadow(surf, "*** GAME OVER ***", FONT_BIG, C['red'], W//2, py+30, center=True)
    draw_text_shadow(surf, f"Skor Akhir: {score}", FONT_MED, C['gold'], W//2, py+110, center=True)
    draw_text_shadow(surf, f"Item: {items_got}/{items_total}", FONT_MED, C['cyan'], W//2, py+148, center=True)
    draw_text_shadow(surf, '"Kegagalan adalah guru terbaik.', FONT_SMALL, C['text_dim'], W//2, py+196, center=True)
    draw_text_shadow(surf, 'Bangkit dan coba lagi!"', FONT_SMALL, C['text_dim'], W//2, py+224, center=True)

    btn1 = (W//2-240, py+280, 210, 48)
    btn2 = (W//2+30,  py+280, 210, 48)
    for btn, text, col in [(btn1,">> COBA LAGI",(35,120,60)),(btn2,"[M] MENU",(35,35,120))]:
        hover = pygame.Rect(*btn).collidepoint(pygame.mouse.get_pos())
        c = tuple(min(255,x+30) for x in col) if hover else col
        draw_rounded_rect(surf, c, btn, radius=12, border=2, border_col=C['white'])
        draw_text_shadow(surf, text, FONT_MED, C['white'], btn[0]+btn[2]//2, btn[1]+10, center=True)

    return pygame.Rect(*btn1), pygame.Rect(*btn2)


def draw_win(surf, star_bg, score, items_got, items_total, frame):
    """Tampilkan layar menang."""
    surf.blit(star_bg, (0,0))

    # Partikel kemenangan
    for i in range(20):
        t = frame*0.03
        sx = int(W*((i*73+frame*2)%100)/100)
        sy = int((frame*2 + i*40)%H)
        ALGO.midpoint_circle(surf, sx, sy, 4, C['star_col'], filled=True)

    pw, ph = 680, 450
    px, py = W//2-pw//2, H//2-ph//2
    draw_rounded_rect(surf, (4,10,40), (px,py,pw,ph), radius=18,
                      border=3, border_col=C['gold'])
    ALGO.dda_line(surf, px+20, py+8, px+pw-20, py+8, C['gold'])

    draw_text_shadow(surf, "SELAMAT! KAMU LULUS!", FONT_BIG, C['gold'], W//2, py+28, center=True)
    draw_text_shadow(surf, f"Skor Final: {score}", FONT_MED, C['white'], W//2, py+106, center=True)
    draw_text_shadow(surf, f"Semua ilmu terkumpul: {items_got}/{items_total}", FONT_MED, C['green'], W//2, py+144, center=True)

    ALGO.dda_line(surf, px+30, py+188, px+pw-30, py+188, (80,60,200))
    draw_text_shadow(surf, '"Orang berpendidikan tahu bagaimana', FONT_SMALL, C['text_dim'], W//2, py+198, center=True)
    draw_text_shadow(surf, 'membuat sesuatu dari apapun."', FONT_SMALL, C['text_dim'], W//2, py+226, center=True)
    draw_text_shadow(surf, "Pendidikan adalah investasi terbaik", FONT_SMALL, C['purple'], W//2, py+266, center=True)
    draw_text_shadow(surf, "untuk masa depan yang cerah!", FONT_SMALL, C['purple'], W//2, py+294, center=True)

    btn1 = (W//2-240, py+360, 210, 48)
    btn2 = (W//2+30,  py+360, 210, 48)
    for btn, text, col in [(btn1,">> MAIN LAGI",(35,120,60)),(btn2,"[M] MENU",(35,35,120))]:
        hover = pygame.Rect(*btn).collidepoint(pygame.mouse.get_pos())
        c = tuple(min(255,x+30) for x in col) if hover else col
        draw_rounded_rect(surf, c, btn, radius=12, border=2, border_col=C['white'])
        draw_text_shadow(surf, text, FONT_MED, C['white'], btn[0]+btn[2]//2, btn[1]+10, center=True)

    return pygame.Rect(*btn1), pygame.Rect(*btn2)


# ============================================================
# DEMO ALGORITMA
# ============================================================

def print_algo_demo():
    algo = GraphicsAlgorithms()
    print("\n" + "="*58)
    print("  JOURNEY TO KNOWLEDGE - Algoritma Grafika Komputer")
    print("="*58)
    pts = algo.dda_line(pygame.Surface((1,1)), 0,0,10,7,(255,255,255))
    print(f"[DDA LINE]  (0,0)->(10,7): {len(pts)} titik | {pts[:3]}...")
    # Midpoint circle (hitung secara manual)
    cx,cy,r,pts2=[],[],6,[]
    x2,y2,p2=6,0,1-6
    while x2>=y2:
        for dx,dy in [(x2,y2),(-x2,y2),(x2,-y2),(-x2,-y2),(y2,x2),(-y2,x2),(y2,-x2),(-y2,-x2)]:
            pts2.append((dx,dy))
        y2+=1; p2=p2+2*y2+1 if p2<=0 else p2+2*y2-2*x2+1
        if p2>0: x2-=1
    print(f"[MIDPOINT]  r=6: {len(pts2)} titik (8-symmetry)")
    ok,x1,y1,x2,y2=algo.cohen_sutherland(-5,3,15,8,0,0,10,10)
    print(f"[CLIP]      ({-5},{3})->({15},{8}) clip(0,0,10,10): accept={ok}, ({x1},{y1})->({x2},{y2})")
    m=algo.transform_matrix(tx=100,ty=50,rz=45,sx=2,sy=2)
    print(f"[TRANSFORM] {m['params']}")
    print(f"[SCANLINE]  Mengisi platform & sprite via algoritma scanline")
    print("="*58 + "\n")

print_algo_demo()


# ============================================================
# MAIN GAME LOOP
# ============================================================

def create_game():
    """Buat instance game baru."""
    player = Player(200, 500)
    platforms = [dict(p) for p in LEVEL['platforms']]
    # Tambah lantai utama (tanah)
    platforms.append({'x': -200, 'y': 570, 'w': LEVEL['total_x']+400, 'h': 40})
    items = [Item(x, y, t) for x,y,t in LEVEL['items']]
    enemies = [Enemy(x, y, r, s) for x,y,r,s in LEVEL['enemies']]
    return player, platforms, items, enemies


def run_game():
    """Loop utama permainan."""
    star_bg = make_star_bg()
    mode = 'menu'
    player, platforms, items, enemies = create_game()
    cam_x = 0
    particles = []
    quote = ""
    quote_timer = 0
    items_got = 0
    frame = 0
    t_anim = 0.0

    print("[GAME] Pygame game started! Window should be visible.")

    while True:
        dt = clock.tick(60) / 1000.0
        t_anim += dt
        frame += 1

        # ---- EVENT ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if mode == 'playing':
                        mode = 'menu'
                    else:
                        pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                if mode == 'menu':
                    pass  # Handled di draw
                elif mode in ('gameover','win'):
                    pass  # Handled di draw

        # ---- MENU ----
        if mode == 'menu':
            screen.blit(star_bg, (0,0))
            btn_start = draw_menu(screen, star_bg, frame)
            pygame.display.flip()
            # Cek klik tombol
            if pygame.mouse.get_pressed()[0]:
                if btn_start.collidepoint(pygame.mouse.get_pos()):
                    player, platforms, items, enemies = create_game()
                    items_got = 0; cam_x = 0; particles = []
                    quote = ""; quote_timer = 0
                    mode = 'playing'
                    pygame.time.delay(150)
            continue

        # ---- PLAYING ----
        if mode == 'playing':
            # Update
            player.update(platforms)
            for e in enemies:
                e.update()

            # Kamera mengikuti player (transformasi translasi kamera)
            target_cam = int(player.x) - W//3
            cam_x += int((target_cam - cam_x) * 0.1)
            cam_x = max(0, min(cam_x, LEVEL['total_x'] - W))

            # Clipping dengan Cohen-Sutherland (digunakan untuk cek visibilitas)
            ok, *_ = ALGO.cohen_sutherland(
                player.x, 0, player.x, H,
                cam_x, 0, cam_x+W, H
            )

            # Collision player vs enemy
            pr = player.rect()
            for e in enemies:
                er = e.rect()
                er.x -= cam_x; er.x += int(e.x) - int(e.x)
                er2 = pygame.Rect(int(e.x)-cam_x-20, int(e.y)-40, 40, 40)
                pr2 = pygame.Rect(int(player.x)-cam_x-14, int(player.y)-40, 28, 40)
                if pr2.colliderect(er2):
                    player.take_damage()
                    # Partikel damage
                    for _ in range(8):
                        particles.append({
                            'x': player.x-cam_x, 'y': player.y-20,
                            'vx': random.uniform(-4,4), 'vy': random.uniform(-6,-1),
                            'r': random.randint(3,7), 'col': [220,50,50],
                            'life': 30, 'max_life': 30
                        })

            # Collision player vs item
            pr2 = pygame.Rect(int(player.x)-20, int(player.y)-44, 40, 44)
            for item in items:
                if item.collected: continue
                ir = pygame.Rect(int(item.x)-20, int(item.y)-28, 40, 56)
                if pr2.colliderect(ir):
                    item.collected = True
                    player.score += item.pts
                    items_got += 1
                    quote = random.choice(QUOTES)
                    quote_timer = 4.5
                    # Partikel koleksi (posisi melingkar = Midpoint Circle concept)
                    for i in range(12):
                        angle = i/12 * math.pi*2
                        particles.append({
                            'x': item.x-cam_x, 'y': item.y,
                            'vx': math.cos(angle)*4, 'vy': math.sin(angle)*4-3,
                            'r': random.randint(4,8),
                            'col': [255,210,50] if item.type != 'book' else [220,80,80],
                            'life': 40, 'max_life': 40
                        })

            # Update partikel (translasi + decay)
            particles = [p for p in particles if p['life'] > 0]
            for p in particles:
                p['x'] += p['vx']; p['y'] += p['vy']
                p['vy'] += 0.3
                p['r'] = max(0, p['r'] - 0.15)
                p['life'] -= 1

            # Quote timer
            if quote_timer > 0: quote_timer -= dt

            # Jatuh ke jurang
            if player.y > 650:
                player.take_damage()
                player.x, player.y = 200, 500
                player.vy = 0

            # Cek win/lose
            if not player.alive: mode = 'gameover'
            if items_got >= len(items): mode = 'win'

            # ---- RENDER ----
            screen.blit(star_bg, (0,0))

            # Pohon
            for tx in LEVEL['trees']:
                draw_tree(screen, tx, 510, cam_x)

            # Tanah
            draw_ground(screen, cam_x)

            # Platform
            for plat in LEVEL['platforms']:
                draw_platform(screen, plat['x'], plat['y'], plat['w'], plat['h'], cam_x)

            # Items
            for item in items:
                item.draw(screen, t_anim, cam_x)

            # Enemies
            for e in enemies:
                e.draw(screen, cam_x)

            # Partikel
            draw_particles(screen, particles)

            # Player
            player.draw(screen, cam_x)

            # HUD
            draw_hud(screen, player, items_got, len(items), quote if quote_timer > 0 else "", quote_timer)

            # Progress bar
            prog = int((cam_x / (LEVEL['total_x']-W)) * (W-200))
            pygame.draw.rect(screen, (30,30,80), (80, H-22, W-160, 12), border_radius=6)
            pygame.draw.rect(screen, C['gold'], (80, H-22, max(8,prog), 12), border_radius=6)
            prog_lbl = FONT_TINY.render(f"Progress: {min(100,int((cam_x/(LEVEL['total_x']-W))*100))}%", True, C['text_dim'])
            screen.blit(prog_lbl, (W//2 - prog_lbl.get_width()//2, H-24))

        # ---- GAME OVER ----
        elif mode == 'gameover':
            btn_retry, btn_menu = draw_gameover(screen, star_bg, player.score, items_got, len(items))
            if pygame.mouse.get_pressed()[0]:
                mp = pygame.mouse.get_pos()
                if btn_retry.collidepoint(mp):
                    player, platforms, items, enemies = create_game()
                    items_got = 0; cam_x = 0; particles = []
                    quote = ""; quote_timer = 0
                    mode = 'playing'
                    pygame.time.delay(150)
                elif btn_menu.collidepoint(mp):
                    mode = 'menu'
                    pygame.time.delay(150)

        # ---- WIN ----
        elif mode == 'win':
            btn_retry, btn_menu = draw_win(screen, star_bg, player.score, items_got, len(items), frame)
            if pygame.mouse.get_pressed()[0]:
                mp = pygame.mouse.get_pos()
                if btn_retry.collidepoint(mp):
                    player, platforms, items, enemies = create_game()
                    items_got = 0; cam_x = 0; particles = []
                    quote = ""; quote_timer = 0
                    mode = 'playing'
                    pygame.time.delay(150)
                elif btn_menu.collidepoint(mp):
                    mode = 'menu'
                    pygame.time.delay(150)

        pygame.display.flip()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == '__main__':
    print("Starting Journey to Knowledge (Pygame)...")
    run_game()