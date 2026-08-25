var matcher = require('../../utils/matcher.js');

Page({
  data: {
    mode: 'vehicle',
    keyword: '',
    brandIndex: 0,
    brandNames: ['全部品牌'],
    brandKeys: [''],
    stats: { vehicles: 0, batteries: 0, brands: 0 },
    results: [],
    resultCount: '-',
    batteryResults: [],
    showModal: false,
    detail: {},
    loading: false
  },

  onLoad: function () {
    var stats = matcher.getStats();
    var brands = matcher.getBrands();
    var brandNames = ['全部品牌'];
    var brandKeys = [''];
    brands.forEach(function (b) {
      brandNames.push(b.short);
      brandKeys.push(b.short);
    });
    this.setData({
      stats: stats,
      brandNames: brandNames,
      brandKeys: brandKeys
    });
    this.showAll();
  },

  switchMode: function (e) {
    var mode = e.currentTarget.dataset.mode;
    this.setData({ mode: mode, keyword: '', results: [], batteryResults: [], resultCount: '-' });
    if (mode === 'vehicle') this.showAll();
  },

  onKeywordInput: function (e) {
    this.setData({ keyword: e.detail.value });
    if (!e.detail.value.trim() && this.data.mode === 'vehicle') this.showAll();
  },

  onBrandChange: function (e) {
    var idx = parseInt(e.detail.value);
    this.setData({ brandIndex: idx });
    this.showAll();
  },

  doSearch: function () {
    var self = this;
    if (this.data.mode === 'vehicle') {
      var brand = this.data.brandKeys[this.data.brandIndex];
      var list = matcher.searchVehicles(this.data.keyword, brand);
      self.renderVehicleResults(list);
    } else {
      var batteries = matcher.searchBatteries(this.data.keyword);
      if (batteries.length === 0) {
        self.setData({ batteryResults: [], resultCount: 0, results: [] });
        return;
      }
      var allRes = [];
      batteries.forEach(function (batt) {
        var vm = matcher.matchBatteryToVehicles(batt).filter(function (r) { return r.fits; });
        allRes.push({ battery: batt, matches: vm });
      });
      self.renderBatteryResults(allRes);
    }
  },

  resetSearch: function () {
    this.setData({ keyword: '', brandIndex: 0, results: [], batteryResults: [], resultCount: '-' });
    this.showAll();
  },

  showAll: function () {
    var brand = this.data.brandKeys[this.data.brandIndex];
    var list = matcher.searchVehicles('', brand);
    this.renderVehicleResults(list);
  },

  renderVehicleResults: function (list) {
    var enriched = list.map(function (v) {
      var br = matcher.matchVehicleToBatteries(v);
      var fitBatt = br.filter(function (r) { return r.fits; });
      var perfect = br.filter(function (r) { return r.fitLevel === '完美匹配'; });
      var pwr = v.电机_额定功率_W || 0;
      return Object.assign({}, v, {
        _brandShort: (v._brand || '').split('_')[0],
        _powerLevel: pwr >= 3000 ? 'high' : (pwr >= 1200 ? 'mid' : 'low'),
        _powerLabel: pwr >= 3000 ? '高功率' : (pwr >= 1200 ? '中功率' : '低功率'),
        _confClass: v.可信度 === '高' ? 'high' : (v.可信度 === '低' ? 'low' : 'mid'),
        _fitBatteries: fitBatt.slice(0, 3).map(function (r) { return { battery: r.battery, fitLevel: r.fitLevel, laid: r.laid, installDims: r.installDims }; }),
        _fitCount: fitBatt.length,
        _perfectCount: perfect.length,
        _allFitResults: br
      });
    });
    this.setData({ results: enriched, resultCount: enriched.length, batteryResults: [] });
  },

  renderBatteryResults: function (allRes) {
    var flat = [];
    allRes.forEach(function (item) {
      item.matches.forEach(function (r) {
        flat.push({
          _key: item.battery.型号 + '_' + r.vehicle.型号,
          battery: item.battery,
          vehicle: Object.assign({}, r.vehicle, { _brandShort: (r.vehicle._brand || '').split('_')[0] }),
          fitLevel: r.fitLevel,
          fits: r.fits,
          reasons: r.reasons,
          laid: r.laid,
          installDims: r.installDims
        });
      });
    });
    this.setData({ batteryResults: flat, resultCount: flat.length, results: [] });
  },

  showDetail: function (e) {
    var idx = e.currentTarget.dataset.id;
    var v = this.data.results[idx];
    if (!v) return;
    var br = matcher.matchVehicleToBatteries(v);
    var fitBatt = br.filter(function (r) { return r.fits; });
    var perfect = br.filter(function (r) { return r.fitLevel === '完美匹配'; });
    var detail = Object.assign({}, v, {
      _brandName: (v._brand || '').replace('_', ' '),
      _confClass: v.可信度 === '高' ? 'high' : (v.可信度 === '低' ? 'low' : 'mid'),
      _fitBatteries: fitBatt.map(function (r) { return { battery: r.battery, fitLevel: r.fitLevel, laid: r.laid, installDims: r.installDims }; }),
      _perfectCount: perfect.length
    });
    this.setData({ showModal: true, detail: detail });
  },

  closeModal: function () {
    this.setData({ showModal: false });
  },

  noop: function () { }
});
