# Panda3D Config - FORCE software renderer (TinyDisplay)
# Ini bypass semua masalah OpenGL/GPU driver

# Paksa pakai software renderer
load-display tinydisplay

# Window
win-size 1280 720

# Background biru tua (wajib set di sini untuk tinydisplay)
background-color 0.03 0.05 0.15 1

# Nonaktifkan shadow (tidak supported tinydisplay)
shadow-depth-bits 0
framebuffer-object #f
