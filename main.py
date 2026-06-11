# -*- coding: utf-8 -*-
"""
================================================
 JOURNEY TO KNOWLEDGE - 3D Raycasting Game
 Tema  : Pentingnya Pendidikan
 Engine: Pygame (Pure Software 3D Rendering)

 Algoritma Grafika Komputer:
  1. DDA Line  → Raycasting (inti engine 3D)
  2. Midpoint Circle → Minimap & UI elements
  3. Cohen-Sutherland → Wall segment clipping
  4. Scanline Fill    → Floor & ceiling render
  5. Transformasi T,R,S → Sprite projection 3D
================================================
"""

import sys, math, random
import pygame
from pygame import gfxdraw
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ── SETUP ──────────────────────────────────────
W, H = 1280, 720
HALF_H = H // 2
FOV = math.pi / 3          # 60° field of view
HALF_FOV = FOV / 2
NUM_RAYS = W // 2           # 1 ray per 2 px (performance)
STEP = FOV / NUM_RAYS
MAX_DEPTH = 16.0
MINI_S = 8                  # minimap cell size
MOVE_SPD = 3.5
ROT_SPD  = 2.2
TILE = 1.0

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Journey to Knowledge | 3D Raycasting")
clock = pygame.time.Clock()
try:
    F_BIG  = pygame.font.SysFont("Segoe UI", 54, bold=True)
    F_MED  = pygame.font.SysFont("Segoe UI", 30, bold=True)
    F_SM   = pygame.font.SysFont("Segoe UI", 20)
    F_TINY = pygame.font.SysFont("Segoe UI", 15)
except:
    F_BIG=pygame.font.Font(None,54); F_MED=pygame.font.Font(None,30)
    F_SM=pygame.font.Font(None,20);  F_TINY=pygame.font.Font(None,15)

# ── PETA LEVEL ─────────────────────────────────
# '#'=Dinding  '.'=Lantai  'B'=Buku  'P'=Pensil  'G'=Toga  'E'=Musuh
MAP_STR = [
    "####################",
    "#.........#........#",
    "#.B.###.#.#.E.####.#",
    "#...#...#.....#....#",
    "#.###.#.#####.#.##.#",
    "#.#...#.....#.#.P..#",
    "#.#.###.###.#.#.##.#",
    "#...#.......#......#",
    "###.#.#####.######.#",
    "#G..#.....#....B...#",
    "#.#######.#.######.#",
    "#.......#...#..E...#",
    "#.#####.#####.####.#",
    "#.#.P...#.....#....#",
    "#.#.#####.###.#.#..#",
    "#...........G......#",
    "#.#.###.#.##########",
    "#.#...#.#.........##",
    "#.B...E.....###.#.##",
    "####################",
]
MAP_W = len(MAP_STR[0])
MAP_H = len(MAP_STR)


def map_get(mx, my):
    if 0 <= int(my) < MAP_H and 0 <= int(mx) < MAP_W:
        return MAP_STR[int(my)][int(mx)]
    return '#'

# ── GENERATE WALL TEXTURES ─────────────────────
def make_wall_tex(w=64, h=64):
    """Buat tekstur dinding bata secara prosedural."""
    s = pygame.Surface((w, h)); s.fill((60,35,20))
    for row in range(0, h, 16):
        offset = 20 if (row//16)%2 else 0
        pygame.draw.line(s,(90,55,30),(0,row),(w,row),2)
        for col in range(-offset, w+32, 32):
            pygame.draw.line(s,(90,55,30),(col,row),(col,row+16),2)
            pygame.draw.rect(s,(75,45,22),(col+2,row+2,28,12))
    return s

def make_floor_tex(w=64, h=64):
    s = pygame.Surface((w, h)); s.fill((40,55,35))
    for i in range(0,w,8):
        pygame.draw.line(s,(50,65,42),(i,0),(i,h),1)
        pygame.draw.line(s,(50,65,42),(0,i),(w,i),1)
    return s

def make_ceil_tex(w=64, h=64):
    s = pygame.Surface((w, h)); s.fill((10,12,35))
    for _ in range(30):
        x,y=random.randint(0,w),random.randint(0,h)
        pygame.draw.circle(s,(180,190,255),( x,y),random.randint(1,2))
    return s

WALL_TEX  = make_wall_tex()
FLOOR_TEX = make_floor_tex()
CEIL_TEX  = make_ceil_tex()

# ── SPRITE TEXTURES ────────────────────────────
def make_book_sprite(sz=48):
    s = pygame.Surface((sz,sz), pygame.SRCALPHA)
    pygame.draw.rect(s,(200,40,40),(4,0,sz-8,sz)); pygame.draw.rect(s,(240,80,80),(4,0,6,sz))
    for y in range(10,sz,8): pygame.draw.line(s,(255,160,160),(10,y),(sz-6,y),1)
    pygame.draw.rect(s,(180,30,30),(4,0,sz-8,sz),2); return s

def make_pencil_sprite(sz=48):
    s = pygame.Surface((sz,sz), pygame.SRCALPHA)
    pts = [(sz//2-5,4),(sz//2+5,4),(sz//2+5,sz-10),(sz//2,sz),(sz//2-5,sz-10)]
    pygame.draw.polygon(s,(255,220,50),pts); pygame.draw.polygon(s,(220,180,30),pts,2)
    pygame.draw.polygon(s,(255,180,150),[(sz//2-5,sz-10),(sz//2+5,sz-10),(sz//2,sz)])
    return s

def make_grad_sprite(sz=48):
    s = pygame.Surface((sz,sz), pygame.SRCALPHA)
    pygame.draw.rect(s,(60,40,180),(2,sz//2-4,sz-4,10))
    pygame.draw.rect(s,(80,60,200),(sz//2-10,sz//2-12,20,12))
    pygame.draw.line(s,(255,200,50),(sz-8,sz//2),(sz-8,sz-8),2)
    pygame.draw.circle(s,(255,200,50),(sz-8,sz-8),5); return s

def make_enemy_sprite(sz=48):
    s = pygame.Surface((sz,sz), pygame.SRCALPHA)
    pygame.draw.circle(s,(140,30,200),(sz//2,sz//2+4),sz//2-4)
    for i,ex in enumerate([sz//2-8,sz//2+8]):
        pygame.draw.circle(s,(255,50,50),(ex,sz//2),6)
        pygame.draw.circle(s,(255,200,50),(ex,sz//2),3)
    for x in range(sz//2-8,sz//2+8):
        pygame.draw.circle(s,(50,10,80),(x,sz//2+12),2)
    pygame.draw.polygon(s,(120,20,180),[(sz//2-6,4),(sz//2-10,16),(sz//2-2,16)])
    pygame.draw.polygon(s,(120,20,180),[(sz//2+6,4),(sz//2+2,16),(sz//2+10,16)])
    return s

SPRITES = {
    'B': {'tex': make_book_sprite(),     'pts':25, 'col':(220,60,60),  'name':'Buku'},
    'P': {'tex': make_pencil_sprite(),   'pts':10, 'col':(255,220,50), 'name':'Pensil'},
    'G': {'tex': make_grad_sprite(),     'pts':50, 'col':(120,80,255), 'name':'Toga'},
    'E': {'tex': make_enemy_sprite(),    'pts': 0, 'col':(180,40,220), 'name':'Musuh'},
}

# ── ALGORITMA GRAFIKA ──────────────────────────
class Algo:

    # 1. DDA LINE → digunakan untuk RAYCASTING
    @staticmethod
    def dda_raycast(px, py, angle):
        """DDA Algorithm - inti dari mesin 3D raycasting."""
        cos_a = math.cos(angle); sin_a = math.sin(angle)
        # Step ke arah x
        if cos_a != 0:
            step_x = abs(1/cos_a); dx = 1 if cos_a>0 else -1
            map_x  = int(px) + (1 if cos_a>0 else 0)
            side_x = (map_x - px)/cos_a if cos_a>0 else (px-int(px))/abs(cos_a)
        else:
            step_x=1e9; side_x=1e9; dx=0
        # Step ke arah y
        if sin_a != 0:
            step_y = abs(1/sin_a); dy = 1 if sin_a>0 else -1
            map_y  = int(py) + (1 if sin_a>0 else 0)
            side_y = (map_y - py)/sin_a if sin_a>0 else (py-int(py))/abs(sin_a)
        else:
            step_y=1e9; side_y=1e9; dy=0

        mx, my, side = int(px), int(py), 0
        dist = 0.0
        hit_x = px; hit_y = py
        cell = '.'
        for _ in range(int(MAX_DEPTH*4)):
            if side_x < side_y:
                dist=side_x; side_x+=step_x; mx+=dx; side=0
            else:
                dist=side_y; side_y+=step_y; my+=dy; side=1
            if dist > MAX_DEPTH: break
            cell = map_get(mx, my)
            if cell == '#':
                hit_x = px + dist*cos_a; hit_y = py + dist*sin_a
                break
        return dist, side, cell, hit_x, hit_y

    # 2. MIDPOINT CIRCLE → Minimap & UI
    @staticmethod
    def draw_circle(surf, cx, cy, r, col, filled=False):
        if filled: pygame.draw.circle(surf, col, (cx,cy), r)
        else:
            x,y,p = r,0,1-r
            while x>=y:
                for dx,dy in [(x,y),(-x,y),(x,-y),(-x,-y),(y,x),(-y,x),(y,-x),(-y,-x)]:
                    gfxdraw.pixel(surf, cx+dx, cy+dy, col)
                y+=1; p=p+2*y+1 if p<=0 else p+2*y-2*x+1
                if p>0: x-=1

    # 3. COHEN-SUTHERLAND → Kliping segmen dinding
    @staticmethod
    def clip_segment(x1,y1,x2,y2, xn,yn,xx,yx):
        INSIDE,L,R,B,T=0,1,2,4,8
        def c(x,y):
            r=INSIDE
            if x<xn:r|=L
            elif x>xx:r|=R
            if y<yn:r|=B
            elif y>yx:r|=T
            return r
        c1,c2,ok=c(x1,y1),c(x2,y2),False
        for _ in range(10):
            if not(c1|c2): ok=True; break
            elif c1&c2: break
            co=c1 if c1 else c2
            if co&T: x=x1+(x2-x1)*(yx-y1)/(y2-y1) if y2!=y1 else x1; y=yx
            elif co&B: x=x1+(x2-x1)*(yn-y1)/(y2-y1) if y2!=y1 else x1; y=yn
            elif co&R: y=y1+(y2-y1)*(xx-x1)/(x2-x1) if x2!=x1 else y1; x=xx
            else: y=y1+(y2-y1)*(xn-x1)/(x2-x1) if x2!=x1 else y1; x=xn
            if co==c1: x1,y1,c1=x,y,c(x,y)
            else: x2,y2,c2=x,y,c(x,y)
        return ok,int(x1),int(y1),int(x2),int(y2)

    # 4. SCANLINE FILL → Lantai & Langit-langit
    @staticmethod
    def draw_floor_ceil(surf, col_floor, col_ceil):
        """Scanline fill - isi lantai dan langit-langit per baris."""
        for y in range(HALF_H+1, H):       # Lantai - scanline dari tengah ke bawah
            pygame.draw.line(surf, col_floor, (0,y), (W,y))
        for y in range(0, HALF_H):          # Langit - scanline dari atas ke tengah
            shade = int(20 + (y/HALF_H)*30)
            pygame.draw.line(surf, (shade, shade+5, shade+20), (0,y),(W,y))

    # 5. TRANSFORMASI → Proyeksi sprite ke layar
    @staticmethod
    def project_sprite(px,py,pangle, sx,sy):
        """Matriks Transformasi: Translasi+Rotasi untuk proyeksi sprite 3D."""
        # Translasi: vektor dari player ke sprite
        dx = sx - px; dy = sy - py
        # Rotasi: transform ke ruang kamera player
        inv = 1.0/(math.cos(pangle)*math.cos(pangle) + math.sin(pangle)*math.sin(pangle))
        cam_x = inv*(math.cos(pangle)*dx  + math.sin(pangle)*dy)
        cam_y = inv*(-math.sin(pangle)*dx + math.cos(pangle)*dy)
        # Skala + proyeksi perspektif
        if cam_y <= 0.1: return None
        screen_x = int((W//2)*(1 + cam_x/cam_y))
        sprite_h  = min(H, int(H/cam_y))
        sprite_w  = sprite_h
        return screen_x, sprite_h, sprite_w, cam_y

A = Algo()

# ── GAME STATE ─────────────────────────────────
class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.px, self.py = 1.5, 1.5   # Posisi player
        self.angle = 0.0
        self.score = 0; self.health = 3; self.inv_t = 0; self.frame = 0
        self.items = {}  # (mx,my): cell_char
        self.enemies = []  # [{x,y,dir,speed}]
        self.collected = set()
        self.quote = ""; self.q_timer = 0
        self._load_map()

    def _load_map(self):
        for my in range(MAP_H):
            for mx in range(MAP_W):
                c = MAP_STR[my][mx]
                if c in ('B','P','G'):
                    self.items[(mx,my)] = c
                elif c == 'E':
                    self.enemies.append({'x':mx+.5,'y':my+.5,'dir':random.uniform(0,math.pi*2),'spd':.025})
        self.total = len(self.items)
        # Cari spawn bersih
        for my in range(1,MAP_H-1):
            for mx in range(1,MAP_W-1):
                if MAP_STR[my][mx]=='.': self.px,self.py=mx+.5,my+.5; return

    def update(self, dt):
        keys = pygame.key.get_pressed()
        spd = MOVE_SPD*dt; rot = ROT_SPD*dt
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: self.angle -= rot
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.angle += rot
        nx,ny = self.px,self.py
        if keys[pygame.K_UP]   or keys[pygame.K_w]:
            nx += math.cos(self.angle)*spd; ny += math.sin(self.angle)*spd
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            nx -= math.cos(self.angle)*spd; ny -= math.sin(self.angle)*spd
        if map_get(nx, self.py) != '#': self.px = nx
        if map_get(self.px, ny) != '#': self.py = ny
        # Kumpulkan item
        cell = (int(self.px), int(self.py))
        if cell in self.items and cell not in self.collected:
            self.collected.add(cell); c = self.items[cell]
            self.score += SPRITES[c]['pts']
            self.quote = random.choice(QUOTES); self.q_timer = 4.0
        # Update musuh
        for e in self.enemies:
            e['x'] += math.cos(e['dir'])*e['spd']
            e['y'] += math.sin(e['dir'])*e['spd']
            if map_get(e['x'],e['y'])=='#':
                e['dir'] = random.uniform(0,math.pi*2)
                e['x'] -= math.cos(e['dir'])*e['spd']
                e['y'] -= math.sin(e['dir'])*e['spd']
            # Damage
            if self.inv_t <= 0 and math.hypot(e['x']-self.px,e['y']-self.py)<.8:
                self.health -= 1; self.inv_t = 90
        if self.inv_t>0: self.inv_t -= 1
        if self.q_timer>0: self.q_timer -= dt
        self.frame += 1

QUOTES = [
    "Pendidikan: senjata paling\nampuh mengubah dunia! -Mandela",
    "Investasi terbaik adalah\npada diri sendiri!",
    "Ilmu adalah cahaya yang\nmenerangi kegelapan!",
    "Belajar tak pernah\nmelelahkan pikiran! -Da Vinci",
    "Pendidikan adalah kunci\nemas kesuksesan!",
    "Teruslah belajar, ilmu\ntidak mengenal batas!",
    "Satu buku bisa mengubah\nperjalanan hidupmu!",
]

# ── RENDER ─────────────────────────────────────
def render(surf, game, z_buf):
    # 4. Scanline fill lantai & langit
    A.draw_floor_ceil(surf, (55,75,45), None)

    # Raycasting dinding (DDA per kolom)
    angle = game.angle - HALF_FOV
    for col in range(NUM_RAYS):
        dist, side, cell, hx, hy = A.dda_raycast(game.px, game.py, angle)
        dist = max(0.01, dist * math.cos(angle - game.angle))  # fish-eye fix
        z_buf[col] = dist

        # Tinggi kolom dinding
        wall_h = min(H, int(H / (dist + 0.0001)))
        y0 = HALF_H - wall_h//2; y1 = HALF_H + wall_h//2

        # Shade berdasarkan jarak + side (Cohen-Sutherland clip ke viewport)
        ok, cx0, _, cx1, _ = A.clip_segment(col*2, y0, col*2, y1, 0, 0, W, H)
        if ok:
            shade = max(40, int(220 - dist*14))
            if side == 1: shade = int(shade*0.7)
            # Tekstur dinding (ambil kolom dari texture)
            tex_x = int((hx if side==1 else hy) * 64) % 64
            col_surf = pygame.transform.scale(
                WALL_TEX.subsurface((tex_x,0,1,64)), (2, wall_h))
            col_surf.set_alpha(shade)
            surf.blit(col_surf, (col*2, y0))

        angle += STEP

    # 5. Sprite projection (Transformasi T+R+S)
    sprites = []
    # Items
    for (mx,my),c in game.items.items():
        if (mx,my) in game.collected: continue
        res = A.project_sprite(game.px,game.py,game.angle, mx+.5,my+.5)
        if res: sprites.append((*res, SPRITES[c]['tex'], SPRITES[c]['col']))
    # Enemies
    for e in game.enemies:
        res = A.project_sprite(game.px,game.py,game.angle, e['x'],e['y'])
        if res: sprites.append((*res, SPRITES['E']['tex'], SPRITES['E']['col']))
    # Sort by distance (painter's algorithm)
    sprites.sort(key=lambda s: -s[3])
    for (sx,sh,sw,sd,tex,col) in sprites:
        if sd > MAX_DEPTH or sd < 0.3: continue
        col_idx = (sx - sw//2) // 2
        if col_idx < 0 or col_idx >= NUM_RAYS: continue
        if z_buf[max(0,min(NUM_RAYS-1,col_idx))] < sd: continue
        shade = max(60, int(220-sd*14))
        scaled = pygame.transform.scale(tex, (sw, sh))
        scaled.set_alpha(shade)
        surf.blit(scaled, (sx-sw//2, HALF_H-sh//2))


def render_hud(surf, game):
    # Panel atas
    pygame.draw.rect(surf,(5,5,28),(0,0,W,52))
    pygame.draw.line(surf,(80,60,200),(0,52),(W,52),2)
    # Score
    t=F_MED.render(f"SCORE: {game.score}",True,(255,210,50))
    surf.blit(t,(12,10))
    # HP (Midpoint Circle)
    for i in range(3):
        col=(210,40,60) if i<game.health else (50,30,70)
        A.draw_circle(surf,200+i*30,26,10,col,filled=True)
        A.draw_circle(surf,200+i*30,26,10,(255,100,130) if i<game.health else (80,50,100))
    # Items
    got=len(game.collected); tot=game.total
    t=F_MED.render(f"ITEM: {got}/{tot}",True,(80,220,255))
    surf.blit(t,(280,10))
    # Algoritma bar
    t=F_TINY.render("[DDA Raycast] [Midpoint Circle] [Cohen-Sutherland] [Scanline Fill] [Transform T*R*S]",True,(70,130,255))
    surf.blit(t,(W//2-t.get_width()//2,36))
    # Kontrol
    t=F_TINY.render("W/S:Maju/Mundur  A/D:Putar  ESC:Menu",True,(120,110,180))
    surf.blit(t,(W-t.get_width()-10,36))
    # Crosshair
    pygame.draw.line(surf,(255,255,255,180),(W//2-10,H//2),(W//2+10,H//2),2)
    pygame.draw.line(surf,(255,255,255,180),(W//2,H//2-10),(W//2,H//2+10),2)
    # Quote
    if game.q_timer>0:
        lines=game.quote.split('\n')
        bw,bh=520,16+len(lines)*26
        bx,by=W//2-bw//2, H-bh-70
        pygame.draw.rect(surf,(8,3,40),(bx,by,bw,bh),border_radius=10)
        pygame.draw.rect(surf,(100,70,220),(bx,by,bw,bh),2,border_radius=10)
        for i,ln in enumerate(lines):
            c=(255,210,50) if i==0 else (180,160,220)
            t=F_SM.render(ln,True,c)
            surf.blit(t,(W//2-t.get_width()//2,by+6+i*26))
    # Minimap (pojok kanan bawah)
    mx0=W-MAP_W*MINI_S-10; my0=H-MAP_H*MINI_S-62
    for my in range(MAP_H):
        for mx in range(MAP_W):
            c=MAP_STR[my][mx]
            col=(50,35,15) if c=='#' else (20,30,15)
            if (mx,my) in game.items and (mx,my) not in game.collected:
                col=SPRITES[game.items[(mx,my)]]['col']
            pygame.draw.rect(surf,col,(mx0+mx*MINI_S,my0+my*MINI_S,MINI_S-1,MINI_S-1))
    # Player di minimap (Midpoint Circle)
    ppx=mx0+int(game.px*MINI_S); ppy=my0+int(game.py*MINI_S)
    A.draw_circle(surf,ppx,ppy,4,(80,200,255),filled=True)
    # Arah pandang player (DDA Line)
    dx2=int(math.cos(game.angle)*12); dy2=int(math.sin(game.angle)*12)
    pygame.draw.line(surf,(255,255,100),(ppx,ppy),(ppx+dx2,ppy+dy2),2)


def draw_menu(surf,frame):
    surf.fill((5,8,28))
    # Bintang (Midpoint Circle)
    random.seed(99)
    for _ in range(120):
        x,y=random.randint(0,W),random.randint(0,H//2+50)
        r=random.randint(1,2)
        A.draw_circle(surf,x,y,r,(random.randint(150,255),random.randint(150,255),255),True)
    pw,ph=700,480; px=W//2-pw//2; py=H//2-ph//2-20
    pygame.draw.rect(surf,(6,4,26),(px,py,pw,ph),border_radius=18)
    pygame.draw.rect(surf,(80,60,200),(px,py,pw,ph),2,border_radius=18)
    # Judul
    t=F_BIG.render("JOURNEY TO KNOWLEDGE",True,(255,210,50))
    surf.blit(t,(W//2-t.get_width()//2,py+24))
    t=F_MED.render("~ Pentingnya Pendidikan | 3D Raycasting ~",True,(160,120,255))
    surf.blit(t,(W//2-t.get_width()//2,py+90))
    pygame.draw.line(surf,(80,60,180),(px+30,py+130),(px+pw-30,py+130),2)
    for i,ln in enumerate([
        "Jelajahi gedung SEKOLAH ILMU PENGETAHUAN!",
        "Kumpulkan Buku (+25), Pensil (+10), Toga (+50)",
        "Hindari Monster Kebodohan yang mengintai!",
    ]):
        t=F_SM.render(ln,True,(160,155,210))
        surf.blit(t,(W//2-t.get_width()//2,py+150+i*30))
    pygame.draw.line(surf,(60,50,140),(px+30,py+246),(px+pw-30,py+246),1)
    for i,ln in enumerate(["W/S : Maju / Mundur","A/D : Putar Kamera","ESC : Kembali ke Menu"]):
        t=F_SM.render(ln,True,(100,180,255))
        surf.blit(t,(W//2-t.get_width()//2,py+260+i*26))
    t=F_TINY.render("[ALGO] DDA Raycast | Midpoint Circle | Cohen-Sutherland | Scanline Fill | Transform T*R*S",True,(60,200,100))
    surf.blit(t,(W//2-t.get_width()//2,py+360))
    btn=(W//2-160,py+395,320,52)
    hov=pygame.Rect(*btn).collidepoint(pygame.mouse.get_pos())
    pygame.draw.rect(surf,(45,145,70) if hov else (30,110,55),btn,border_radius=14)
    pygame.draw.rect(surf,(80,220,100),btn,2,border_radius=14)
    t=F_MED.render(">> MULAI JELAJAH <<",True,(255,255,255))
    surf.blit(t,(W//2-t.get_width()//2,btn[1]+12))
    t=F_TINY.render('"Pendidikan adalah senjata paling ampuh untuk mengubah dunia." - Nelson Mandela',True,(150,130,200))
    surf.blit(t,(W//2-t.get_width()//2,py+460))
    return pygame.Rect(*btn)


def draw_overlay(surf,title,lines,btn1_txt,btn2_txt,col_top):
    ov=pygame.Surface((W,H),pygame.SRCALPHA); ov.fill((0,0,0,180)); surf.blit(ov,(0,0))
    pw,ph=620,380; px=W//2-pw//2; py=H//2-ph//2
    pygame.draw.rect(surf,(6,4,26),(px,py,pw,ph),border_radius=16)
    pygame.draw.rect(surf,col_top,(px,py,pw,ph),3,border_radius=16)
    t=F_BIG.render(title,True,col_top)
    surf.blit(t,(W//2-t.get_width()//2,py+22))
    for i,ln in enumerate(lines):
        t=F_MED.render(ln,True,(200,190,230))
        surf.blit(t,(W//2-t.get_width()//2,py+100+i*36))
    b1=(W//2-240,py+300,210,48); b2=(W//2+30,py+300,210,48)
    for btn,txt,c in [(b1,btn1_txt,(35,120,55)),(b2,btn2_txt,(35,35,120))]:
        hov=pygame.Rect(*btn).collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(surf,tuple(min(255,x+30) for x in c) if hov else c,btn,border_radius=12)
        pygame.draw.rect(surf,(200,200,255),btn,2,border_radius=12)
        t=F_MED.render(txt,True,(255,255,255))
        surf.blit(t,(btn[0]+btn[2]//2-t.get_width()//2,btn[1]+10))
    return pygame.Rect(*b1),pygame.Rect(*b2)


# ── MAIN ───────────────────────────────────────
def main():
    print("\n"+"="*55)
    print("  JOURNEY TO KNOWLEDGE - 3D Raycasting")
    print("  Algoritma: DDA | Midpoint | CS-Clip | Scanline | Transform")
    print("="*55+"\n")
    game = Game()
    z_buf = [MAX_DEPTH]*NUM_RAYS
    mode = 'menu'
    frame = 0

    while True:
        dt = min(clock.tick(60)/1000.0, 0.05)
        frame += 1

        for event in pygame.event.get():
            if event.type==pygame.QUIT: pygame.quit(); sys.exit()
            if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                if mode=='playing': mode='menu'
                else: pygame.quit(); sys.exit()

        if mode=='menu':
            btn=draw_menu(screen,frame)
            if pygame.mouse.get_pressed()[0] and btn.collidepoint(pygame.mouse.get_pos()):
                game.reset(); mode='playing'; pygame.time.delay(150)

        elif mode=='playing':
            game.update(dt)
            render(screen,game,z_buf)
            render_hud(screen,game)
            if game.health<=0: mode='gameover'
            if len(game.collected)>=game.total: mode='win'

        elif mode=='gameover':
            b1,b2=draw_overlay(screen,"GAME OVER",
                [f"Skor: {game.score}",f"Item: {len(game.collected)}/{game.total}",
                 '"Bangkit & coba lagi!"'],">> COBA LAGI","[M] MENU",(220,40,40))
            if pygame.mouse.get_pressed()[0]:
                mp=pygame.mouse.get_pos()
                if b1.collidepoint(mp): game.reset();mode='playing';pygame.time.delay(150)
                if b2.collidepoint(mp): mode='menu';pygame.time.delay(150)

        elif mode=='win':
            b1,b2=draw_overlay(screen,"SELAMAT LULUS!",
                [f"Skor Final: {game.score}",f"Semua ilmu: {len(game.collected)}/{game.total}",
                 '"Pendidikan = kunci emas kesuksesan!"'],">> MAIN LAGI","[M] MENU",(255,210,50))
            if pygame.mouse.get_pressed()[0]:
                mp=pygame.mouse.get_pos()
                if b1.collidepoint(mp): game.reset();mode='playing';pygame.time.delay(150)
                if b2.collidepoint(mp): mode='menu';pygame.time.delay(150)

        pygame.display.flip()

if __name__=='__main__':
    main()