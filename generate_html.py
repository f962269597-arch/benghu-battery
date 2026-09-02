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
    ("GX4820", "157×182×265"): ("assets/img/4820.png", "", "assets/files/4820-规格书.pdf", ""),
    ("GX4824", "157×182×265"): ("assets/img/4824.png", "", "assets/files/4824-规格书.pdf", ""),
    ("6428LFP", "185×165×340"): ("assets/img/6428.png", "", "", ""),
    ("6435LFP", "180×156×334"): ("assets/img/6435LFP.png", "assets/img/6435LFP-参数.png",
                                "assets/files/6435LFP-规格书.pdf", "assets/files/6435LFP-认证报告.pdf"),
    ("6450LFP", "232×161×344"): ("assets/img/6450LFP.png", "assets/img/6450LFP-参数.png",
                                "assets/files/6450LFP-规格书.pdf", "assets/files/6450LFP-认证报告.pdf"),
    ("6460LFP", "400×260×185"): ("assets/img/6460LFP.png", "assets/img/6460LFP-参数.png",
                                "assets/files/6460LFP-规格书.pdf", "assets/files/6460LFP-认证报告.pdf"),
    ("6460LFP塑壳", "462×267×170"): ("assets/img/6460（PC+ABS）.png", "", "", ""),
    ("6480LFP钣金", "400×260×210"): ("", "", "", ""),
    ("64120LFP*S款", "570×330×180"): ("assets/img/64120S款.png", "", "", ""),
    ("64120LFP-4G智能钣金", "570×300×200"): ("assets/img/64120-4G智能钣金.png", "", "", ""),
    ("64120LFP-4G智能电池", "500×460×200"): ("assets/img/64120-4G智能电池.jpg", "", "", ""),
    ("7635LFP", "214×156×334"): ("", "", "", ""),
    ("7635LFP（卧款）", "400×185×168"): ("assets/img/7635LFP.png", "assets/img/7635LFP-参数.png",
                                "assets/files/7635LFP-规格书.pdf", "assets/files/7635LFP-认证报告.pdf"),
    ("7650LFP（卧款）", "460×214×168"): ("assets/img/7650LFP.png", "assets/img/7650LFP-参数.png",
                                "assets/files/7650LFP-规格书.pdf", "assets/files/7650LFP-认证报告.pdf"),
    ("7660LFP", "464×260×185"): ("assets/img/7660（钣金）.png", "", "", ""),
    ("7660LFP塑壳", "462×267×170"): ("assets/img/7660.png", "", "", ""),
    ("7670LFP 4G钣金款", "560×230×170"): ("assets/img/7670-4G钣金款.png", "", "", ""),
    ("7680LFP塑壳", "462×267×200"): ("assets/img/7680.png", "", "", ""),
    ("76120LFP-4G智能电池", "500×460×200"): ("assets/img/76120-4G智能电池.png", "", "", ""),
    ("72100LFP", "595×230×175"): ("", "", "", ""),
    ("76120LFP", "670×330×180"): ("assets/img/76120.png", "", "", ""),
    ("LY24V12Ah", "245×195×102"): ("assets/img/24V12Ah.png", "", "assets/files/轮椅-BA012L-AS21A-规格书.pdf", ""),
    ("LY36V8Ah", "308×134×75"): ("assets/img/36V8Ah.png", "", "assets/files/轮椅-ADCF120292237-规格书.pdf", ""),
    ("LY25.6V7Ah", "192×169×48.5"): ("assets/img/25.6V7Ah.png", "", "assets/files/轮椅-ACF83AV060-规格书.pdf", ""),
    ("LY25.6V12Ah", "367×158×116.8"): ("assets/img/25.6V12Ah.png", "", "assets/files/轮椅-ADCF080379238-规格书.pdf", ""),
    ("LY25.2V10.4Ah", "212.4×190×50"): ("assets/img/25.2V10.4Ah.png", "", "assets/files/轮椅-ADCN07040F32D-规格书.pdf", ""),
}

# 展示排序：48V → 64V → 76.8V → 轮椅
def series_key(b):
    if b.get('系列') == '轮椅':
        return 3
    v = b.get('电压_V', 0)
    if v == 48:
        return 0
    if v == 64:
        return 1
    return 2

batteries.sort(key=series_key)

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
