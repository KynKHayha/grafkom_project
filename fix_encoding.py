"""Fix encoding in generate_assets.py"""
content = open('generate_assets.py', 'r', encoding='utf-8').read()
content = content.replace('print("\u2713 ', 'print("[OK] ')
content = content.replace("print('\u2713 ", "print('[OK] ")
open('generate_assets.py', 'w', encoding='utf-8').write(content)
print('Fixed all checkmarks')
