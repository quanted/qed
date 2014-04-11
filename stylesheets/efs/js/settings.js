var Settings = {
  // localStorage object
  ls: {},

  init: function() {
    Settings.loadSettings();
    Settings.attachEvents();
  },

  loadSettings: function() {
    Settings.load.domain();
  },

  saveSettings: function() {
      Settings.save.domain();
  },

  attachEvents: function() {
      jQuery('#settingsSave').on('click', Settings.saveSettings);
  },

  getDomain: function() {
    return Settings.ls.domain;
  },

  load: {
    domain: function() {
      var defaultDomain = "http://pnnl.cloudapp.net";

      if (Settings.util.lsTest()) {
        Settings.ls = localStorage;

        if (Settings.ls.domain == undefined) {
          Settings.ls.domain = defaultDomain;
        }

        jQuery('#settingsDomain').val(Settings.getDomain());
      }
    }
  },

  save: {
    domain: function() {
      var uiDomain = jQuery('#settingsDomain').val();

      if (uiDomain != Settings.ls.domain) Settings.ls.domain = uiDomain;
    }
  },

  util: {
    lsTest: function() {
      var test = 'test';
      try {
          localStorage.setItem(test, test);
          localStorage.removeItem(test);
          return true;
      } catch(e) {
          return false;
      }
    }
  }
};
