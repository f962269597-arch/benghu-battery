# -*- coding: utf-8 -*-
"""奔虎锂电 · 电池匹配系统 HTML 生成器 v2 - 纯读JSON生成"""
import json, os

BASE = r'F:\Claude项目\电车数据'

with open(os.path.join(BASE, 'vehicles.json'), 'r', encoding='utf-8') as f:
    vehicles = json.load(f)
with open(os.path.join(BASE, 'batteries.json'), 'r', encoding='utf-8') as f:
    bat_data = json.load(f)

batteries = bat_data.get('电池列表', [])
total_v = sum(len(v) for v in vehicles.values() if isinstance(v, list))
total_b = len(batteries)
brand_count = len([b for b in vehicles if isinstance(vehicles[b], list) and len(vehicles[b]) > 0])

print(f'Vehicles: {total_v} | Batteries: {total_b} | Brands: {brand_count}')

# ===== Generate HTML =====
v_json = json.dumps(vehicles, ensure_ascii=False, indent=4)
b_json = json.dumps(batteries, ensure_ascii=False, indent=4)

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="奔虎电池匹配">
<meta name="theme-color" content="#1a1a2e">
<link rel="manifest" href="manifest.json">
<title>奔虎锂电 · 车型电池智能匹配系统</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Microsoft YaHei','PingFang SC',sans-serif;background:#f0f2f5;color:#333;min-height:100vh}}
.header{{background:linear-gradient(135deg,#1a1a2e,#e2720c);color:#fff;padding:20px 0;text-align:center}}
.header h1{{font-size:clamp(20px,5vw,28px);font-weight:700;letter-spacing:2px}}
.header p{{font-size:14px;opacity:.85;margin-top:6px}}
.container{{max-width:1200px;margin:0 auto;padding:12px}}
.search-box{{background:#fff;border-radius:12px;padding:20px;margin-bottom:16px;box-shadow:0 2px 12px rgba(0,0,0,.08)}}
.search-row{{display:flex;gap:10px;flex-wrap:wrap;align-items:center}}
.search-row input{{flex:1;min-width:200px;padding:12px 16px;border:2px solid #e0e0e0;border-radius:8px;font-size:16px}}
.search-row input:focus{{border-color:#e2720c;outline:none}}
.search-row select{{padding:12px 16px;border:2px solid #e0e0e0;border-radius:8px;font-size:16px;background:#fff;min-width:120px}}
.search-row button{{padding:12px 24px;background:#e2720c;color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer;white-space:nowrap}}
.search-row button:hover{{background:#c9600a}}
.search-row button.secondary{{background:#fff;color:#e2720c;border:2px solid #e2720c}}
.search-row button.secondary:hover{{background:#fff8f3}}
.mode-tabs{{display:flex;gap:4px;margin-bottom:14px;background:#f5f5f5;border-radius:8px;padding:4px}}
.mode-tab{{flex:1;padding:10px 16px;border:none;background:transparent;border-radius:6px;cursor:pointer;font-size:14px;font-weight:500}}
.mode-tab.active{{background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.1);color:#e2720c;font-weight:700}}
.result-summary{{margin-bottom:12px;font-size:14px;color:#666}}
.result-summary strong{{color:#e2720c}}
.card-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px}}
.card{{background:#fff;border-radius:12px;padding:18px;box-shadow:0 2px 8px rgba(0,0,0,.06);border-left:4px solid transparent;cursor:pointer;transition:all .2s}}
.card.match{{border-left-color:#22c55e}}
.card.no-match{{border-left-color:#ef4444;opacity:.7}}
.card:hover{{box-shadow:0 4px 16px rgba(0,0,0,.12);transform:translateY(-2px)}}
.card h3{{font-size:17px;margin-bottom:2px;color:#1a1a2e}}
.card .brand{{font-size:11px;color:#999;margin-bottom:8px}}
.card .specs{{display:grid;grid-template-columns:1fr 1fr;gap:4px 14px;font-size:13px}}
.card .specs .label{{color:#888}}
.card .specs .value{{font-weight:600;color:#333}}
.power-tag{{display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px}}
.power-tag.high{{background:#fee2e2;color:#dc2626}}
.power-tag.mid{{background:#fef3c7;color:#d97706}}
.power-tag.low{{background:#dbeafe;color:#2563eb}}
.src-badge{{display:inline-block;padding:1px 6px;border-radius:8px;font-size:10px}}
.src-badge.src-high{{background:#dcfce7;color:#16a34a}}
.src-badge.src-mid{{background:#fef3c7;color:#d97706}}
.src-badge.src-low{{background:#fee2e2;color:#dc2626}}
.match-badge{{display:inline-block;padding:4px 12px;border-radius:12px;font-size:12px;font-weight:600}}
.match-badge.fit{{background:#dcfce7;color:#16a34a}}
.match-badge.nofit{{background:#fee2e2;color:#dc2626}}
.battery-info{{margin-top:10px;padding-top:10px;border-top:1px solid #f0f0f0}}
.battery-info .batt-name{{font-weight:700;color:#e2720c}}
.stats{{display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap}}
.stat-card{{background:#fff;padding:14px 18px;border-radius:10px;box-shadow:0 1px 4px rgba(0,0,0,.06);text-align:center;min-width:80px;flex:1}}
.stat-card .num{{font-size:26px;font-weight:700;color:#e2720c}}
.stat-card .label{{font-size:11px;color:#888;margin-top:2px}}
.modal-overlay{{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.5);z-index:100;justify-content:center;align-items:center}}
.modal-overlay.show{{display:flex}}
.modal{{background:#fff;border-radius:16px;padding:28px;max-width:500px;width:95%;max-height:85vh;overflow-y:auto}}
.modal h2{{margin-bottom:14px}}
.modal .close{{float:right;background:none;border:none;font-size:24px;cursor:pointer;color:#999}}
.empty{{text-align:center;padding:50px 20px;color:#999}}
.empty .icon{{font-size:56px;margin-bottom:12px}}
.footer{{text-align:center;padding:20px;color:#999;font-size:12px}}
@media (max-width:640px){{.card-grid{{grid-template-columns:1fr}}.search-row input,.search-row select,.search-row button{{width:100%}}.stats{{gap:6px}}.stat-card{{padding:10px 12px}}.stat-card .num{{font-size:20px}}}}
</style>
</head>
<body>
<div class="header"><h1>🔋 奔虎锂电 · 车型电池智能匹配</h1><p>输入车型 → 秒出可装电池 | {total_v}款车型 · {total_b}款电池 · {brand_count}品牌</p></div>
<div class="container">
<div class="stats" id="stats"></div>
<div class="search-box">
<div class="mode-tabs">
<button class="mode-tab active" data-mode="vehicle">🚗 按车型查电池</button>
<button class="mode-tab" data-mode="battery">🔋 按电池查车型</button>
</div>
<div class="search-row" id="searchVehicleRow">
<input type="text" id="vehicleSearch" placeholder="输入车型搜索，如：M95C、FXT、AE5、F0...">
<select id="brandFilter"><option value="">全部品牌</option></select>
<button onclick="searchVehicles()">🔍 搜索</button>
<button class="secondary" onclick="resetSearch()">↺ 重置</button>
</div>
<div class="search-row" id="searchBatteryRow" style="display:none">
<input type="text" id="batterySearch" placeholder="输入电池型号搜索...">
<button onclick="searchBatteries()">🔍 搜索</button>
<button class="secondary" onclick="resetSearch()">↺ 重置</button>
</div>
</div>
<div class="result-summary" id="resultSummary"></div>
<div class="card-grid" id="cardGrid"></div>
<div class="empty" id="emptyState"><div class="icon">🔍</div><p>上方搜索车型，即刻匹配可安装的奔虎电池</p></div>
</div>
<div class="modal-overlay" id="modalOverlay"><div class="modal" id="modalContent"></div></div>
<div class="footer">奔虎锂电 · 智能匹配系统 v2.0 | 数据持续更新 | <a href="javascript:void(0)" onclick="alert('数据来源说明：\\n高可信=多源验证/官方数据 | 中可信=单源实测/经销商 | 低可信=估算值需实测确认\\n数据来源：品牌官方参数+车友实测+经销商+网络收集\\n更新时间：2025-07-17\\n来电咨询：奔虎锂电')">📋 数据来源说明</a></div>
<script>
var EMBEDDED_VEHICLES = {v_json};
var EMBEDDED_BATTERIES = {b_json};
var vehicles = EMBEDDED_VEHICLES;
var allBatteriesFlat = EMBEDDED_BATTERIES;
var currentMode = 'vehicle';
var allVehiclesFlat = [];

function init(){{
allVehiclesFlat=[];
for(var brand in vehicles){{if(Array.isArray(vehicles[brand])){{vehicles[brand].forEach(function(v){{allVehiclesFlat.push(Object.assign({{}},v,{{_brand:brand}}));}});}}}}
if('serviceWorker' in navigator && location.protocol === 'https:'){{navigator.serviceWorker.register('sw.js').catch(function(){{}});}}
var sel=document.getElementById('brandFilter');
for(var b in vehicles){{if(Array.isArray(vehicles[b])&&vehicles[b].length>0){{var n=b.replace('_',' ');sel.innerHTML+='<option value="'+b.split('_')[0]+'">'+n+'</option>';}}}}
updateStats();renderAllVehicles();setupListeners();
}}

function updateStats(){{
var brands=0;for(var b in vehicles){{if(Array.isArray(vehicles[b])&&vehicles[b].length>0)brands++;}}
document.getElementById('stats').innerHTML='<div class="stat-card"><div class="num">'+allVehiclesFlat.length+'</div><div class="label">收录车型</div></div><div class="stat-card"><div class="num">'+brands+'</div><div class="label">覆盖品牌</div></div><div class="stat-card"><div class="num">'+allBatteriesFlat.length+'</div><div class="label">电池型号</div></div><div class="stat-card"><div class="num" id="matchCount">-</div><div class="label">匹配结果</div></div>';
}}

function setupListeners(){{
document.querySelectorAll('.mode-tab').forEach(function(t){{t.addEventListener('click',function(){{document.querySelectorAll('.mode-tab').forEach(function(x){{x.classList.remove('active');}});this.classList.add('active');currentMode=this.dataset.mode;document.getElementById('searchVehicleRow').style.display=currentMode==='vehicle'?'flex':'none';document.getElementById('searchBatteryRow').style.display=currentMode==='battery'?'flex':'none';resetSearch();}});}});
document.getElementById('brandFilter').addEventListener('change',function(){{renderAllVehicles();}});
document.getElementById('vehicleSearch').addEventListener('keypress',function(e){{if(e.key==='Enter')searchVehicles();}});
document.getElementById('vehicleSearch').addEventListener('input',function(){{if(!this.value.trim())renderAllVehicles();}});
document.getElementById('batterySearch').addEventListener('keypress',function(e){{if(e.key==='Enter')searchBatteries();}});
document.getElementById('modalOverlay').addEventListener('click',function(e){{if(e.target===this)closeModal();}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape')closeModal();if(e.ctrlKey&&e.key==='k'){{e.preventDefault();document.getElementById('vehicleSearch').focus();}}}});
}}

function checkFit(battery,vehicle){{
var bl=battery.长_mm||0,bw=battery.宽_mm||0,bh=battery.高_mm||0;
var vl=vehicle.电池仓_长_mm||0,vw=vehicle.电池仓_宽_mm||0,vh=vehicle.电池仓_高_mm||0;
var lOk=bl<=vl,wOk=bw<=vw,hOk=bh<=vh,reasons=[];
if(!lOk)reasons.push('长度超限('+bl+'>'+vl+'mm)');
if(!wOk)reasons.push('宽度超限('+bw+'>'+vw+'mm)');
if(!hOk)reasons.push('高度超限('+bh+'>'+vh+'mm)');
if(vehicle.电池仓_宽窄处_mm&&bw>vehicle.电池仓_宽窄处_mm)reasons.push('宽度超窄处限制');
var sizeFit=lOk&&wOk&&hOk;
var battMaxPwr=battery.适用电机功率_最大_W||99999;
var vehPwr=vehicle.电机_额定功率_W||0;
var powerFit=vehPwr<=battMaxPwr;
var level=sizeFit?(powerFit?'完美匹配':'尺寸合适(功率需确认)'):'尺寸不匹配';
return{{fits:sizeFit,powerFit:powerFit,fitLevel:level,reasons:reasons}};
}}

function matchVehicleToBatteries(vehicle){{return allBatteriesFlat.map(function(b){{var r=checkFit(b,vehicle);r.battery=b;return r;}}).sort(function(a,b){{var o={{'完美匹配':0,'尺寸合适(功率需确认)':1,'尺寸不匹配':2}};return(o[a.fitLevel]||3)-(o[b.fitLevel]||3);}});}}

function matchBatteryToVehicles(battery){{return allVehiclesFlat.map(function(v){{var r=checkFit(battery,v);r.vehicle=v;return r;}}).sort(function(a,b){{var o={{'完美匹配':0,'尺寸合适(功率需确认)':1,'尺寸不匹配':2}};return(o[a.fitLevel]||3)-(o[b.fitLevel]||3);}});}}

function searchVehicles(){{
var q=document.getElementById('vehicleSearch').value.trim().toLowerCase();
if(!q){{renderAllVehicles();return;}}
var brand=document.getElementById('brandFilter').value;
var results=allVehiclesFlat.filter(function(v){{if(brand&&!v._brand.includes(brand))return false;return(v._brand+' '+v.型号+' '+(v.类型||'')+' '+(v.备注||'')).toLowerCase().includes(q);}});
renderResults(results);
}}

function searchBatteries(){{
var q=document.getElementById('batterySearch').value.trim().toLowerCase();
if(!q){{renderAllVehicles();return;}}
var matched=allBatteriesFlat.filter(function(b){{return(b.型号+' '+b.电压_V+'V '+b.容量_Ah+'Ah').toLowerCase().includes(q);}});
if(!matched.length){{document.getElementById('resultSummary').innerHTML='<strong>未找到匹配的电池</strong>';document.getElementById('cardGrid').innerHTML='';document.getElementById('emptyState').style.display='block';return;}}
var allRes=[];matched.forEach(function(batt){{var vm=matchBatteryToVehicles(batt).filter(function(r){{return r.fits;}});allRes.push({{battery:batt,vehicleMatches:vm}});}});
renderBatteryResults(allRes);
}}

function renderResults(list){{
var grid=document.getElementById('cardGrid'),summary=document.getElementById('resultSummary'),empty=document.getElementById('emptyState');
if(!list.length){{summary.innerHTML='<strong>未找到匹配车型</strong>，试试其他关键词';grid.innerHTML='';empty.style.display='block';document.getElementById('matchCount').textContent='0';return;}}
summary.innerHTML='找到 <strong>'+list.length+'</strong> 款车型';document.getElementById('matchCount').textContent=list.length;empty.style.display='none';
grid.innerHTML=list.map(function(v){{
var brandShort=(v._brand||'').split('_')[0],pwr=v.电机_额定功率_W||0;
var pwrLevel=pwr>=3000?'high':(pwr>=1200?'mid':'low'),pwrLabel=pwr>=3000?'高功率':(pwr>=1200?'中功率':'低功率');
var src=v.数据来源||'网络收集',conf=v.可信度||'中',confClass=conf==='高'?'high':(conf==='低'?'low':'mid');
var br=matchVehicleToBatteries(v),fitBatt=br.filter(function(r){{return r.fits;}}),perfect=br.filter(function(r){{return r.fitLevel==='完美匹配';}});
return '<div class="card" onclick="showDetail(\\''+v._brand.replace(/'/g,'\\\\\\'')+'\\',\\''+v.型号.replace(/'/g,'\\\\\\'')+'\\')"><div style="display:flex;justify-content:space-between;align-items:start"><div><h3>'+v.型号+'</h3><div class="brand">'+brandShort+' · '+(v.类型||'')+' <span class="src-badge src-'+confClass+'">'+conf+'可信 · '+src+'</span></div></div><span class="power-tag '+pwrLevel+'">'+pwrLabel+'</span></div><div class="specs"><div><span class="label">电池仓：</span><span class="value">'+(v.电池仓_长_mm||'-')+'×'+(v.电池仓_宽_mm||'-')+'×'+(v.电池仓_高_mm||'-')+' mm</span></div><div><span class="label">电机功率：</span><span class="value">'+(v.电机_额定功率_W||'-')+'W'+(v.电机_峰值功率_W?' / 峰值'+v.电机_峰值功率_W+'W':'')+'</span></div><div><span class="label">原厂电池：</span><span class="value">'+(v.原厂电池规格||'-')+'</span></div><div><span class="label">可匹配：</span><span class="value" style="color:#e2720c">'+fitBatt.length+'款'+(perfect.length?' ('+perfect.length+'款完美)':'')+'</span></div></div>'+(v.备注?'<div style="margin-top:6px;font-size:12px;color:#888;">💡 '+v.备注+'</div>':'')+(fitBatt.length?'<div class="battery-info"><div style="font-size:11px;color:#888;margin-bottom:2px;">🔋 可装奔虎电池：</div>'+fitBatt.slice(0,3).map(function(r){{return '<div style="font-size:12px;margin:1px 0;"><span class="batt-name">'+r.battery.型号+'</span> '+r.battery.电压_V+'V'+r.battery.容量_Ah+'Ah '+r.battery.长_mm+'×'+r.battery.宽_mm+'×'+r.battery.高_mm+'mm <span class="match-badge fit">'+r.fitLevel+'</span></div>';}}).join('')+(fitBatt.length>3?'<div style="font-size:11px;color:#e2720c;">+ '+(fitBatt.length-3)+' 款更多...</div>':'')+'</div>':'<div class="battery-info" style="color:#ef4444;">⚠️ 暂无匹配电池</div>')+'</div>';
}}).join('');
}}

function renderBatteryResults(allRes){{
var grid=document.getElementById('cardGrid'),summary=document.getElementById('resultSummary');
var total=allRes.reduce(function(s,r){{return s+r.vehicleMatches.length;}},0);
summary.innerHTML='可匹配 <strong>'+total+'</strong> 款车型';document.getElementById('matchCount').textContent=total;
document.getElementById('emptyState').style.display=total?'none':'block';
grid.innerHTML=allRes.map(function(item){{return item.vehicleMatches.map(function(r){{return '<div class="card match"><div style="display:flex;justify-content:space-between;align-items:start"><div><h3>'+r.vehicle.型号+'</h3><div class="brand">'+(r.vehicle._brand||'').split('_')[0]+' · '+(r.vehicle.类型||'')+'</div></div><span class="match-badge fit">✅ '+r.fitLevel+'</span></div><div class="specs"><div><span class="label">电池仓：</span><span class="value">'+(r.vehicle.电池仓_长_mm||'-')+'×'+(r.vehicle.电池仓_宽_mm||'-')+'×'+(r.vehicle.电池仓_高_mm||'-')+' mm</span></div><div><span class="label">电池：</span><span class="value">'+item.battery.型号+' ('+item.battery.长_mm+'×'+item.battery.宽_mm+'×'+item.battery.高_mm+'mm)</span></div><div><span class="label">电机：</span><span class="value">'+(r.vehicle.电机_额定功率_W||'-')+'W / 电池'+item.battery.电压_V+'V</span></div><div><span class="label">原厂规格：</span><span class="value">'+(r.vehicle.原厂电池规格||'-')+'</span></div></div>'+(r.reasons.length&&r.fitLevel!=='完美匹配'?'<div style="margin-top:6px;font-size:11px;color:#ef4444;">⚠️ '+r.reasons.join('；')+'</div>':'')+'</div>';}}).join('');}}).join('');
}}

function renderAllVehicles(){{var brand=document.getElementById('brandFilter').value,list=allVehiclesFlat;if(brand)list=list.filter(function(v){{return v._brand.includes(brand);}});renderResults(list);}}

function resetSearch(){{document.getElementById('vehicleSearch').value='';document.getElementById('batterySearch').value='';document.getElementById('brandFilter').value='';renderAllVehicles();updateStats();}}

function showDetail(brand,model){{
var v=allVehiclesFlat.find(function(x){{return x._brand===brand&&x.型号===model;}});if(!v)return;
var br=matchVehicleToBatteries(v),fitBatt=br.filter(function(r){{return r.fits;}}),perfect=br.filter(function(r){{return r.fitLevel==='完美匹配';}});
var src=v.数据来源||'网络收集',conf=v.可信度||'中',confClass=conf==='高'?'high':(conf==='低'?'low':'mid');
document.getElementById('modalContent').innerHTML='<button class="close" onclick="closeModal()">✕</button><h2>'+v.型号+'</h2><p style="color:#888;margin-bottom:12px;">'+(brand||'').replace('_',' ')+' · '+(v.类型||'')+' <span class="src-badge src-'+confClass+'">'+conf+'可信 · '+src+'</span></p><div style="display:grid;grid-template-columns:1fr 1fr;gap:6px 12px;margin-bottom:12px"><div><strong>电池仓：</strong>'+(v.电池仓_长_mm||'-')+' × '+(v.电池仓_宽_mm||'-')+' × '+(v.电池仓_高_mm||'-')+' mm</div>'+(v.电池仓_宽窄处_mm?'<div><strong>窄处宽：</strong>'+v.电池仓_宽窄处_mm+' mm</div>':'')+'<div><strong>额定功率：</strong>'+(v.电机_额定功率_W||'-')+'W</div><div><strong>峰值功率：</strong>'+(v.电机_峰值功率_W||'-')+'W</div><div><strong>原厂电池：</strong>'+(v.原厂电池规格||'-')+'</div></div>'+(v.备注?'<p style="background:#fff8f3;padding:8px 12px;border-radius:6px;font-size:13px;">💡 '+v.备注+'</p>':'')+'<hr style="margin:14px 0;border-color:#f0f0f0"><h4 style="margin-bottom:8px;">🔋 匹配的奔虎电池 ('+fitBatt.length+'款)</h4>'+(fitBatt.length===0?'<p style="color:#ef4444;">暂无匹配电池</p>':fitBatt.map(function(r){{return '<div style="padding:10px;margin:5px 0;background:#f8fdf8;border-radius:8px;border-left:3px solid #22c55e"><strong style="color:#e2720c;">'+r.battery.型号+'</strong><span class="match-badge fit" style="margin-left:8px">'+r.fitLevel+'</span><div style="font-size:12px;color:#666;margin-top:3px">'+r.battery.电压_V+'V '+r.battery.容量_Ah+'Ah | '+r.battery.长_mm+'×'+r.battery.宽_mm+'×'+r.battery.高_mm+'mm | '+(r.battery.持续放电电流_A||'-')+'A/'+(r.battery.峰值放电电流_A||'-')+'A'+(r.battery.重量_kg?' | '+r.battery.重量_kg+'kg':'')+'</div><div style="font-size:11px;color:#888">适配电机：'+(r.battery.适用电机功率_最小_W||0)+'-'+(r.battery.适用电机功率_最大_W||'不限')+'W | '+r.battery.电芯类型+' | '+r.battery.壳体材质+'</div></div>';}}).join(''))+(perfect.length===0&&fitBatt.length>0?'<p style="font-size:11px;color:#d97706;margin-top:6px">⚠️ 功率范围需进一步确认</p>':'');document.getElementById('modalOverlay').classList.add('show');
}}

function closeModal(){{document.getElementById('modalOverlay').classList.remove('show');}}
init();
</script>
</body>
</html>'''

out = os.path.join(BASE, '电池匹配系统.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Generated: {out} ({len(html)} bytes)')
print('Done!')
