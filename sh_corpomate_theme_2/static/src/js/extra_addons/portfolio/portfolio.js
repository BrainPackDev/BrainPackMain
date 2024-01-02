odoo.define('sh_onemate_theme.s_portfolio_frontend', function (require) {

	
    var concurrency = require('web.concurrency');
    var core = require('web.core');
    var publicWidget = require('web.public.widget');
    
    var qweb = core.qweb;
    
    
    
    publicWidget.registry.shOnematePortfolio = publicWidget.Widget.extend({
        selector: '.js_cls_get_sh_onemate_s_portfolio',
        disabledInEditableMode: true,
        read_events: {
            'click .js_cls_s_portfolio_filter_button': '_onClickFilterButton',
        },
        
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
            this.item_template = this.$el.attr('data-item_template') || false;
    
            this.initialize_lc_lightbox();
    
            this._dp.add(this._fetch()).then(this._render.bind(this));
            return this._super.apply(this, arguments);
            
        },
        
        /**
         * Initialize LC Lightbox plugin.
         * @private
         */
        initialize_lc_lightbox: function () {
            
            lc_lightbox('.js_cls_s_portfolio_lcl', {
                wrap_class: 'lcl_fade_oc',
                gallery : true,	
                thumb_attr: 'data-lcl-thumb',
                skin: 'dark',
                radius: 0,
                padding	: 0,
                border_w: 0,
            });
        },
        
        
        /**
         * @override
         */
        destroy: function () {
            this._super(...arguments);
            this.$el.find('.js_cls_render_dynamic_portfolio_area').html('');
        },
    
        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------
    
        /**
         * @private
         */
        _fetch: function () {    	
            return this._rpc({
                route: '/sh_onemate_theme/get_portfolio',
                params: {
                    'item_template': this.item_template,
                },            
            }).then(res => {
                return res;
            });
        },
        /**
         * @private
         */
        _render: function (res) {
            // Add dynamic content
            this.$('.js_cls_render_dynamic_portfolio_area').html(res);
        },
        
        
        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
    
        /**
         * Add product to cart and reload the carousel.
         * @private
         * @param {Event} ev
         */
        _onClickFilterButton: function (ev) {
            var self = this;  
            var $button = $(ev.currentTarget);
            var value = $button.attr('data-filter');        
            self.$el.find(".js_cls_s_portfolio_filter_button").removeClass("active");
            $button.addClass("active");
            
            if(value == "all")
            {
                self.$el.find('.js_cls_s_portfolio_filter_el').show('1000');
            }
            else
            {
                self.$el.find(".js_cls_s_portfolio_filter_el").not('.'+ value).hide('3000');
                self.$el.find('.js_cls_s_portfolio_filter_el').filter('.'+ value).show('3000');   
            }
        },
        
        
        
            
    });
    
    
    });
    
    