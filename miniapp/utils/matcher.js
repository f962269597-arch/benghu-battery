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
  var bl = battery.长_mm || 0, bw = battery.宽_mm || 0, bh = battery.高_mm || 0;
  var vl = vehicle.电池仓_长_mm || 0, vw = vehicle.电池仓_宽_mm || 0, vh = vehicle.电池仓_高_mm || 0;
  var lOk = bl <= vl, wOk = bw <= vw, hOk = bh <= vh, reasons = [];
  if (!lOk) reasons.push('长度超限(' + bl + '>' + vl + 'mm)');
  if (!wOk) reasons.push('宽度超限(' + bw + '>' + vw + 'mm)');
  if (!hOk) reasons.push('高度超限(' + bh + '>' + vh + 'mm)');
  if (vehicle.电池仓_宽窄处_mm && bw > vehicle.电池仓_宽窄处_mm) reasons.push('宽度超窄处限制');
  var sizeFit = lOk && wOk && hOk;
  // Voltage matching
  var vSpec = (vehicle.原厂电池规格 || '').toLowerCase();
  var vMatch = vSpec.match(/(\d+)\s*v/i);
  var vVolt = vMatch ? parseInt(vMatch[1]) : 0;
  var battVolt = battery.电压_V || 0;
  var voltOk = true;
  if (vVolt === 60 && battVolt !== 48) { voltOk = false; reasons.push('电压不匹配：60V原厂需用64V锂电'); }
  if (vVolt === 72 && battVolt !== 72) { voltOk = false; reasons.push('电压不匹配：72V原厂需用76V锂电'); }
  if (vVolt === 48 && battVolt !== 48) { voltOk = false; reasons.push('电压不匹配：48V原厂需用64V锂电'); }
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
