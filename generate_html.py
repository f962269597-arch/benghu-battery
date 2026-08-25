# -*- coding: utf-8 -*-
"""奔虎锂电 · 产品展示 + 车型电池智能匹配系统 生成器 v3
读取 vehicles.json + batteries.json，生成 index.html（GitHub Pages 主页）。
更新流程：修改 JSON → 运行 python generate_html.py → 提交推送。
新增产品图时：把图片放进 assets/img/，然后在下方 ASSET_MAP 里加一行。
"""
import json, os

BASE = r'F:\Claude项目\电车数据'

with open(os.path.join(BASE, 'vehicles.json'), 'r', encoding='utf-8') as f:
    vehicles = json.load(f)
with open(os.path.join(BASE, 'batteries.json'), 'r', encoding='utf-8') as f:
    bat_data = json.load(f)

batteries = bat_data.get('电池列表', [])

# ============================================================
# 产品素材映射：型号 + 尺寸 → 产品图 / 参数图 / 规格书 / 认证报告
# 新产品有图后：文件放到 assets/img/ 和 assets/files/，在这里加一行即可
# ============================================================
ASSET_MAP = {
    ("6435LFP", "185×165×340"): ("assets/img/6435LFP.png", "assets/img/6435LFP-参数.png",
                                "assets/files/6435LFP-规格书.pdf", "assets/files/6435LFP-认证报告.pdf"),
    ("6440LFP", "240×170×350"): ("assets/img/6440.png", "", "", ""),
    ("6450LFP", "240×170×350"): ("assets/img/6450LFP.png", "assets/img/6450LFP-参数.png",
                                "assets/files/6450LFP-规格书.pdf", "assets/files/6450LFP-认证报告.pdf"),
    ("6460LFP", "400×259×185"): ("assets/img/6460LFP.png", "assets/img/6460LFP-参数.png",
                                "assets/files/6460LFP-规格书.pdf", "assets/files/6460LFP-认证报告.pdf"),
    ("6460LFP", "462×267×170"): ("assets/img/6460（PC+ABS）.png", "", "", ""),
    ("6480LFP", "400×259×210"): ("assets/img/6480.png", "", "", ""),
    ("64120LFP（沈）", "570×300×200"): ("assets/img/64120（沈）.png", "", "", ""),
    ("64120LFP（石）", "500×460×200"): ("assets/img/64120（石）.jpg", "", "", ""),
    ("7635LFP", "220×165×340"): ("assets/img/7635（立）.png", "", "", ""),
    ("7635LFP（卧）", "400×185×168"): ("assets/img/7635LFP.png", "assets/img/7635LFP-参数.png",
                                "assets/files/7635LFP-规格书.pdf", "assets/files/7635LFP-认证报告.pdf"),
    ("7650LFP", "460×220×168"): ("assets/img/7650LFP.png", "assets/img/7650LFP-参数.png",
                                "assets/files/7650LFP-规格书.pdf", "assets/files/7650LFP-认证报告.pdf"),
    ("7660LFP", "462×267×170"): ("assets/img/7660.png", "", "", ""),
    ("7670LFP", "560×230×170"): ("assets/img/7670.png", "", "", ""),
    ("7680LFP", "462×267×200"): ("assets/img/7680.png", "", "", ""),
    ("76120LFP", "500×460×200"): ("assets/img/76120.png", "", "", ""),
}

# 给电池附加展示字段：展示名（同名加壳体材质区分）、图片、PDF
name_count = {}
for b in batteries:
    short = b['型号'].replace('奔虎', '')
    name_count[short] = name_count.get(short, 0) + 1

for b in batteries:
    short = b['型号'].replace('奔虎', '')
    if name_count[short] > 1:
        b['展示名'] = short + '（' + (b.get('壳体材质') or '款') + '）'
    else:
        b['展示名'] = short
    dims = f"{b['长_mm']}×{b['宽_mm']}×{b['高_mm']}"
    asset = ASSET_MAP.get((short, dims)) or ASSET_MAP.get((b['型号'], dims))
    if asset:
        b['展示图'] = asset[0]
        b['参数图'] = asset[1]
        b['规格书'] = asset[2]
        b['认证报告'] = asset[3]
    else:
        b['展示图'] = ''
        b['参数图'] = ''
        b['规格书'] = ''
        b['认证报告'] = ''

total_v = sum(len(v) for v in vehicles.values() if isinstance(v, list))
total_b = len(batteries)
brand_count = len([k for k in vehicles if isinstance(vehicles[k], list) and len(vehicles[k]) > 0])

v_json = json.dumps(vehicles, ensure_ascii=False)
b_json = json.dumps(batteries, ensure_ascii=False)

# ============================================================
# 页面模板（__VJSON__ / __BJSON__ 在生成时替换为数据）
# ============================================================
TEMPLATE = open(os.path.join(BASE, 'page_template.html'), 'r', encoding='utf-8').read()

html = TEMPLATE.replace('__VJSON__', v_json).replace('__BJSON__', b_json)

out = os.path.join(BASE, 'index.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Vehicles: {total_v} | Batteries: {total_b} | Brands: {brand_count}')
print(f'Generated: {out} ({len(html)} bytes)')
