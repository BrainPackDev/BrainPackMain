odoo.define('sh_corpomate_theme.sh_snippet_builder', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var options = require('web_editor.snippets.options');
    var wUtils = require('website.utils');
    var _t = core._t;
    const QWeb = core.qweb;



    // SNIPPET OPTION.
    options.registry.js_editor_sh_snippet_builder = options.Class.extend({
        start: function () {
            // loadXML('/sh_snippet_builder/static/src/xml/sh_snippet_builder_popup.xml', core.qweb);
            var self = this;
            var def = this._super.apply(this, arguments);
            return def;
        },

        sh_snippet_builder_configure: function (previewMode, value) {
            var self = this;
            if (previewMode === false || previewMode === "click") {

                // MAKE MODEL
                self.$modal = $(QWeb.render('sh_corpomate_theme.sh_popup_snippt_builder'));

                // REMOVE PREVIOUS APPENDED MODEL
                $('body > #js_id_model_sh_snippet_builder_config').remove();

                // ADD MODEL TO BODY IN ORDER TO OPEN IT.
                self.$modal.appendTo('body');

                // CLICK ON SAVE CHANGES BUTTON ADD CODE TO PAGE.
                self.$modal.on('click', ".js_cls_btn_apply_sh_snippet_builder_config", function () {

                    self.$modal.css('display-block;')
                    // JS
                    var js_arch = self.$modal.find('#js_id_sh_snippet_builder_js_code').val() || '   ';
                    var js = js_arch;
                    // STYLE
                    var style = "<style>" + self.$modal.find('#js_id_sh_snippet_builder_css_code').val() + "</style>";

                    // HTML
                    var html = self.$modal.find('#js_id_sh_snippet_builder_html_code').val();

                    // PUT/ADD CODE IN ODOO PAGE.
                    self.$target.empty().append(style + html);
                    var name = self.$modal.find('#js_id_sh_snippet_builder_name').val()
                    self._rpc({
                        model: 'sh.snippet.builder',
                        method: 'create',
                        args: [{ 'html': html, 'js': js, 'css': style, 'name': name }],
                    }).then(function (data) {
                        if (data && data['error']) {
                            alert("Please check Syntax !");
                        } else {
                            // CLOSE THE MODEL         
                            $("#js_id_model_sh_snippet_builder_config").css({ 'display': '' });
                        }
                    });
                });

                // CLOSE THE MODEL 
                self.$modal.on('click', ".js_cls_btn_close_button", function () {
                    $("#js_id_model_sh_snippet_builder_config").css({ 'display': '' });
                });

                // REMOVE MODEL
                self.$modal.modal();
            }
            return self;
        },
        onBuilt: function () {
            var self = this;
            this._super();
            this.sh_snippet_builder_configure('click');
        }
    });

});
