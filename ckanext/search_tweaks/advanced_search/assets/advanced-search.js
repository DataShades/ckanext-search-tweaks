ckan.module("search-tweaks-advanced-search", function ($) {
  "use strict";
  var EVENT_TOGGLE_SEARCH = "composite-search:toggle";
  return {
    options: {
      enableAdvanced: false,
      enableSolr: false,
    },
    initialize: function () {
      $.proxyAll(this, /_on/);
      this.toggles = this.$(".advanced-toggles");
      this.fieldQ = this.$('input[name="q"]');
      this.fieldSolr = this.$('input[name="ext_solr_q"]');

      this.toggles
        .find(".enable-advanced")
        .on("change", this._onEnableAdvanced);
      this.toggles.find(".enable-solr").on("change", this._onEnableSolr);
      this.el.on("keyup", this._onKeyUp);

      if (this.options.enableAdvanced) {
        this.enableAdvanced();
      }
      if (this.options.enableSolr) {
        this.enableAdvanced();
        this.enableSolr();
      }
    },
    teadown: function () {},
    _onKeyUp: function (e) {
      if (e.key !== "Enter") {
        return;
      }
      if (e.target.name != "ext_composite_value") {
        return;
      }
      this.$('[type="submit"]').first().click();
    },
    _onEnableAdvanced: function (e) {
      if (e.target.checked) {
        this.enableAdvanced();
      } else {
        this.disableAdvanced();
      }
    },
    _onEnableSolr: function (e) {
      if (e.target.checked) {
        this.enableSolr();
      } else {
        this.disableSolr();
      }
    },

    enableAdvanced: function () {
      this.el.addClass("enabled");
      this.toggles.addClass("advanced-active");
      this.sandbox.publish(EVENT_TOGGLE_SEARCH, true);
      this.fieldQ.prop("disabled", true);
    },

    disableAdvanced: function () {
      this.el.removeClass("enabled");
      this.toggles
        .removeClass("advanced-active")
        .find(".enable-solr input")
        .prop("checked", false);
      this.disableSolr();
      this.sandbox.publish(EVENT_TOGGLE_SEARCH, false);
      this.fieldQ.prop("disabled", false);
    },

    enableSolr: function () {
      this.el.addClass("use-solr-query");
      this.sandbox.publish(EVENT_TOGGLE_SEARCH, false);
      this.fieldSolr.prop("disabled", false);
    },
    disableSolr: function () {
      this.el.removeClass("use-solr-query");
      this.sandbox.publish(EVENT_TOGGLE_SEARCH, true);
      this.fieldSolr.prop("disabled", true);
    },
  };
});
