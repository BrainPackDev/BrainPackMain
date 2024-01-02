odoo.define('sh_onemate_theme.s_counter_frontend', function (require) {
    'use strict';
    
    var publicWidget = require('web.public.widget');
    var registry = publicWidget.registry;
    var animations = require('website.content.snippets.animation');
    
    registry.shOnemateCounterWidget = animations.Animation.extend({
        selector: '.js_cls_sh_onemate_s_counter',	
        disabledInEditableMode: true,
        effects: [{
            startEvents: 'scroll',
            update: '_updateCounterOnScroll',
        }],
    
        /**
         * @constructor
         */
        init: function () {
            this._super(...arguments);
            this.HasCounted = false;
        },
    
        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
        /**
         * Called when the window is scrolled
         *
         * @private
         * @param {integer} scroll
         */
        _updateCounterOnScroll: function (scroll) {    	
          
            var oTop = this.$el.offset().top - window.innerHeight;
              if (this.HasCounted == false && $(window).scrollTop() > oTop) {
                  //counter part start here
                  var looping = true;
                  console.log('\n\n 123',this.$el)
                  console.log('\n\n 123',this.$el.find('.js_cls_s_counter_number'))
                  this.$el.find('.js_cls_s_counter_number').each(function () {
                       var $this = $(this);
                       looping = true;
                       jQuery({ Counter: 0 }).animate({ Counter: $this.text() }, {
                         duration: 8000,
                         easing: 'swing',
                         step: function () {
                           $this.text(Math.ceil(this.Counter));
                         }
                       });
                     }).promise().done( function(){
                         
                         looping = false;
                     });	  
                  //counter part ends here
                  this.HasCounted = true;
              }        
        },
    
    });
    
    
    
    });
    