# HARUS dijalankan SEBELUM import apapun dari panda3d/ursina
# Tulis config ke memori dulu
import sys

# Set env variable agar panda3d baca config kita
from panda3d.core import loadPrcFileData

# KRITIS: disable alpha bits - ini yang bikin layar "transparan" (terlihat putih)
loadPrcFileData('', 'alpha-bits 0')
loadPrcFileData('', 'framebuffer-object #f')
loadPrcFileData('', 'color-bits 8 8 8 0')
loadPrcFileData('', 'depth-bits 24')
loadPrcFileData('', 'multisamples 0')
loadPrcFileData('', 'background-color 0.05 0.05 0.2 1')

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina(title="BG FIX TEST", size=(800, 500))

# Paksa clear color via Panda3D
from panda3d.core import LVecBase4f
base.win.setClearColor(LVecBase4f(0.05, 0.05, 0.2, 1.0))
base.win.setClearColorActive(True)
# Paksa juga di semua display regions
for dr in base.win.getDisplayRegions():
    dr.setClearColorActive(True)
    dr.setClearColor(LVecBase4f(0.05, 0.05, 0.2, 1.0))
    print(f"  DisplayRegion cleared: {dr.getClearColor()}")

# UI quad merah besar
Entity(parent=camera.ui, model='quad', color=color.rgba(255,0,0,255), scale=(0.8, 0.4), z=0)
Text(parent=camera.ui, text="MUNCUL? WARNA MERAH", color=color.yellow, scale=2.5, y=0.25, z=0)

# 3D cube hijau
e3d = Entity(model='cube', color=color.rgb(0,200,0), scale=3, position=(0,0,5))
camera.position = (0, 0, -5)

print("Setup done. Window should show dark blue background with red quad.")
app.run()
