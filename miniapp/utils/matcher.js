var vehiclesData = require('./vehicles.js');
var batteriesData = require('./batteries.js');

// Flatten vehicles
var allVehicles = [];
for (var brand in vehiclesData) {
  if (Array.isArray(vehiclesData[brand])) {
    vehiclesData[brand].forEach(function(v) {
      allVehicles.push(Object.assign({}, v, { _brand: brand }));
    });
  }
}

function checkFit(battery, vehicle) {
  // 电池可任意姿态安装：立装 / 平放 / 侧放，6 种旋转逐一尝试
  var D = [battery.长_mm || 0, battery.宽_mm || 0, battery.高_mm || 0];
  var V = [vehicle.电池仓_长_mm || 0, vehicle.电池仓_宽_mm || 0, vehicle.电池仓_高_mm || 0];
  var narrow = vehicle.电池仓_宽窄处_mm || 0;
  var perms = [];
  [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]].forEach(function (p) {
    var d = [D[p[0]], D[p[1]], D[p[2]]];
    var key = d.join('x');
    if (!perms.some(function (x) { return x.key === key; })) perms.push({ d: d, laid: p[2] !== 2, key: key });
  });
  perms.sort(function (a, b) { return (a.laid ? 1 : 0) - (b.laid ? 1 : 0); });
  var fitPerm = null, reasons = [], bestOver = Infinity;
  for (var i = 0; i < perms.length; i++) {
    var d = perms[i].d;
    if (d[0] <= V[0] && d[1] <= V[1] && d[2] <= V[2] && (!narrow || d[1] <= narrow)) { fitPerm = perms[i]; break; }
    var over = [d[0] - V[0], d[1] - V[1], d[2] - V[2]].map(function (x) { return x > 0 ? x : 0; });
    var total = over[0] + over[1] + over[2] + (narrow && d[1] > narrow ? 10000 : 0);
    if (total < bestOver) {
      bestOver = total;
      reasons = [];
      if (over[0]) reasons.push('长度超限(' + d[0] + '>' + V[0] + 'mm)');
      if (over[1]) reasons.push('宽度超限(' + d[1] + '>' + V[1] + 'mm)');
      if (over[2]) reasons.push('高度超限(' + d[2] + '>' + V[2] + 'mm)');
      if (narrow && d[1] > narrow) reasons.push('宽度超窄处限制');
    }
  }
  var sizeFit = !!fitPerm;
  // Voltage matching
  var vSpec = (vehicle.原厂电池规格 || '').toLowerCase();
  var vMatch = vSpec.match(/(\d+)\s*v/i);
  var vVolt = vMatch ? parseInt(vMatch[1]) : 0;
  var battVolt = battery.电压_V || 0;
  var voltOk = true;
  if (vVolt === 60 && battVolt !== 64) { voltOk = false; reasons.push('电压不匹配：60V原厂需用64V锂电'); }
  if (vVolt === 72 && battVolt !== 76.8) { voltOk = false; reasons.push('电压不匹配：72V原厂需用76.8V锂电'); }
  if (vVolt === 48 && battVolt !== 64) { voltOk = false; reasons.push('电压不匹配：48V原厂需用64V锂电'); }
  // Power matching
  var battMaxPwr = battery.适用电机功率_最大_W || 99999;
  var vehPwr = vehicle.电机_额定功率_W || 0;
  var powerFit = vehPwr <= battMaxPwr;
  var level = (sizeFit && voltOk) ? (powerFit ? '完美匹配' : '尺寸合适(功率需确认)') : (sizeFit && !voltOk ? '电压不匹配' : '尺寸不匹配');
  return {
    fits: sizeFit && voltOk,
    powerFit: powerFit,
    voltOk: voltOk,
    fitLevel: level,
    reasons: reasons,
    laid: fitPerm ? fitPerm.laid : false,
    installDims: fitPerm ? fitPerm.d.join('×') : '',
    battery: battery,
    vehicle: vehicle
  };
}

function matchVehicleToBatteries(vehicle) {
  return batteriesData.map(function(b) {
    var r = checkFit(b, vehicle);
    r.battery = b;
    return r;
  }).sort(function(a, b) {
    var o = { '完美匹配': 0, '尺寸合适(功率需确认)': 1, '尺寸不匹配': 2, '电压不匹配': 2 };
    return (o[a.fitLevel] || 3) - (o[b.fitLevel] || 3);
  });
}

function matchBatteryToVehicles(battery) {
  return allVehicles.map(function(v) {
    var r = checkFit(battery, v);
    r.vehicle = v;
    return r;
  }).sort(function(a, b) {
    var o = { '完美匹配': 0, '尺寸合适(功率需确认)': 1, '尺寸不匹配': 2, '电压不匹配': 2 };
    return (o[a.fitLevel] || 3) - (o[b.fitLevel] || 3);
  });
}

function searchVehicles(keyword, brand) {
  var q = (keyword || '').toLowerCase();
  return allVehicles.filter(function(v) {
    if (brand && !v._brand.includes(brand)) return false;
    if (!q) return !brand || v._brand.includes(brand);
    return (v._brand + ' ' + v.型号 + ' ' + (v.类型 || '') + ' ' + (v.备注 || '')).toLowerCase().includes(q);
  });
}

function searchBatteries(keyword) {
  var q = (keyword || '').toLowerCase();
  return batteriesData.filter(function(b) {
    return (b.型号 + ' ' + b.电压_V + 'V ' + b.容量_Ah + 'Ah').toLowerCase().includes(q);
  });
}

function getBrands() {
  var brands = [];
  for (var b in vehiclesData) {
    if (Array.isArray(vehiclesData[b]) && vehiclesData[b].length > 0) {
      brands.push({ key: b, name: b.replace('_', ' '), short: b.split('_')[0] });
    }
  }
  return brands;
}

function getStats() {
  var bc = 0;
  for (var b in vehiclesData) {
    if (Array.isArray(vehiclesData[b]) && vehiclesData[b].length > 0) bc++;
  }
  return { vehicles: allVehicles.length, batteries: batteriesData.length, brands: bc };
}

module.exports = {
  allVehicles: allVehicles,
  allBatteries: batteriesData,
  checkFit: checkFit,
  matchVehicleToBatteries: matchVehicleToBatteries,
  matchBatteryToVehicles: matchBatteryToVehicles,
  searchVehicles: searchVehicles,
  searchBatteries: searchBatteries,
  getBrands: getBrands,
  getStats: getStats
};
