ckan.module("search-tweaks-reflect-range-in-label", function($){
    "use strict";

    return {
	options: {
	    format: "%d",
	},
	initialize: function() {
	    this.el.on("input", this._onChange.bind(this));
	    this.label = $('[for="' + this.el.prop("id") + '"]');

	    this.el.trigger("input");
	},
	_onChange: function(e) {
	    var value = e.target.value;
	    var formatted = this.options.format.replace(/%d/g, value);
	    this.label.attr("data-value", formatted);
	}
    };
});
