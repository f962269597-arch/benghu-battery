# -*- coding: utf-8 -*-
"""把 assets/img 下的产品图/参数图批量转成 WebP，不删原图。
用法：python optimize_images.py
输出：assets/img/webp/<原名>.webp（宽 ≤800，等比；原图更窄则不放大）
"""
import os, sys, io, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, 'assets', 'img')
DST = os.path.join(SRC, 'webp')
MAXW = 800
QUALITY = 80

os.makedirs(DST, exist_ok=True)

files = []
for ext in ('*.png', '*.jpg', '*.jpeg', '*.PNG', '*.JPG'):
    files += glob.glob(os.path.join(SRC, ext))
files = sorted(set(files))

before = sum(os.path.getsize(f) for f in files)
after = 0
done = 0
for f in files:
    name = os.path.splitext(os.path.basename(f))[0]
    out = os.path.join(DST, name + '.webp')
    src_mtime = os.path.getmtime(f)
    if os.path.exists(out) and os.path.getmtime(out) >= src_mtime:
        after += os.path.getsize(out)
        done += 1
        continue
    im = Image.open(f)
    has_alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
    im = im.convert('RGBA' if has_alpha else 'RGB')
    w, h = im.size
    if w > MAXW:
        h = round(h * MAXW / w)
        w = MAXW
        im = im.resize((w, h), Image.LANCZOS)
    im.save(out, 'WEBP', quality=QUALITY, method=6)
    after += os.path.getsize(out)
    done += 1

print(f'图片 {done} 张：{before/1048576:.1f} MB -> {after/1048576:.2f} MB '
      f'（压缩到 {after/before*100:.1f}%）')
