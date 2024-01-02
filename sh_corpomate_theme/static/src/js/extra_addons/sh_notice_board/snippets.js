odoo.define("sh_corpomate_theme.sh_notice_board", function (require) {
    "use strict";

    require("web.dom_ready");
    var concurrency = require("web.concurrency");
    var core = require("web.core");
    var publicWidget = require("web.public.widget");

    publicWidget.registry.sh_nb_notice_board_horizontal_tmpl_1 = publicWidget.Widget.extend({
        selector: ".sh_nb_notice_board_main_horizontal_marquee_cls_1 , .sh_nb_notice_board_main_vertical_marquee_cls_1, .js_cls_sh_nb_notice_board_vertical_tmpl_4_render_dynamic_area",
        disabledInEditableMode: true,
        /**
         * @constructor
         */
        init: function () {
            this._super.apply(this, arguments);
            this._dp = new concurrency.DropPrevious();
        },
        /**
         * @override
         */
        start: function () {
            var self = this;
            var tempalte = this.$el.attr("data-item_template") || false;
            var section_classes = false;
            var rows = false;
            if (this.$el.parents("section").attr("class")) {
                section_classes = this.$el.parents("section").attr("class");
            }

            if (section_classes) {
                var pos = section_classes.search("newscount_");
                if (pos != -1) {
                    var newscount_cls = section_classes.substring(pos, pos + 12);
                    var rows = newscount_cls.replace("newscount_", "");
                }
            }
            this.$el.find("span").remove();
            this.$el.find("div").remove();

            if (self.$el.hasClass('js_cls_sh_nb_notice_board_vertical_tmpl_4_render_dynamic_area')) {
                self.$el.empty();
            }
            this._rpc({
                route: "/get_latest_news",
                params: { limit: rows },
            }).then((data) => {
                _.each(data, function (news) {

                    if (self.$el.hasClass('js_cls_sh_nb_notice_board_vertical_tmpl_4_render_dynamic_area')) {
                        self.$el.append("<li><a href='#'>" + news.desc + "</a></li>");
                    }
                    else if (self.$el.parents('div').attr('class') == 'sh_vertical_main row') {
                        self.$el.append("<div class='sh_news'><h4>" + news.name + "</h4><p>" + news.desc + "</p></div>");
                    }
                    else if (self.$el.parents('div').attr('class') == 'sh_vertical_div_js_cls container-fluid row') {
                        self.$el.append("<div class='sh_news_box'><h4>" + news.name + "</h4><p>" + news.desc + "</p></div>");
                    }
                    else {
                        self.$el.append("<span>" + news.desc + "</span>");
                    }
                });
            });

            return this._super.apply(this, arguments);

        },
    });
});
