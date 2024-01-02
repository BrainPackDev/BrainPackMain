odoo.define("sh_corpomate_theme.sh_corpomate_bottom_navbar", function (require) {
    "use strict";

    var publicWidget = require("web.public.widget");
    var animations = require('website.content.snippets.animation');


    publicWidget.registry.sh_corpomate_zoom_toggle = animations.Animation.extend({
        selector: "#wrapwrap",
        events: {
            'click .js_cls_zoom_toggle_btn.zoom_in': '_click_expand_button',
            'click .js_cls_zoom_toggle_btn.zoom_out': '_click_compress_button',
        },

        _click_expand_button: function (ev) {
            ev.preventDefault();
            var self = this;
            $('.js_cls_zoom_toggle_btn.zoom_in').addClass('d-none');
            $('.js_cls_zoom_toggle_btn.zoom_out').removeClass('d-none');
            var elem = document.querySelector('body');
            if (elem.requestFullscreen) {
                elem.requestFullscreen();
            } else if (elem.mozRequestFullScreen) { /* Firefox */
                elem.mozRequestFullScreen();
            } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
                elem.webkitRequestFullscreen();
            } else if (elem.msRequestFullscreen) { /* IE/Edge */
                elem.msRequestFullscreen();
            }
        },
        _click_compress_button: function (ev) {
            ev.preventDefault();
            var self = this;
            $('.js_cls_zoom_toggle_btn.zoom_in').removeClass('d-none');
            $('.js_cls_zoom_toggle_btn.zoom_out').addClass('d-none');
            var elem = document.querySelector('body');
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.mozCancelFullScreen) { /* Firefox */
                document.mozCancelFullScreen();
            } else if (document.webkitExitFullscreen) { /* Chrome, Safari and Opera */
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) { /* IE/Edge */
                document.msExitFullscreen();
            }
        },

    });


    publicWidget.registry.sh_corpomate_bottom_navbar = animations.Animation.extend({
        selector: "#wrapwrap",
        disabledInEditableMode: true,

        effects: [{
            startEvents: 'scroll',
            update: '_add_remove_top_to_bottom_navbar',
        }],



        /**
         * @constructor
         */
        init: function () {
            this._super(...arguments);
            var self = this;
            this.amount_scrolled = 300;


        },



        //--------------------------------------------------------------------------
        /**
         * Called when the window is scrolled
         *
         * @private
         * @param {integer} scroll
         */
        _add_remove_top_to_bottom_navbar: function (scroll) {
            var self = this;

            var navbar = $(document).find('.js_cls_bottom_nav_bar_wrapper');
            if (navbar.length > 0 && scroll + $("#wrapwrap").innerHeight() >= $("#wrapwrap")[0].scrollHeight - 100) {
                navbar.fadeOut('slow');

            } else if (navbar.length > 0) {
                navbar.fadeIn('slow');
            }

            // $(document).find('.js_cls_sh_corpomate_theme_flag_btn').click(function (event) {

            // })
        },


    });




    publicWidget.registry.sh_corpomate_bottom_navbar_sh_corpomate_theme_section_536 = animations.Animation.extend({
        selector: "#sh_corpomate_theme_section_536",
        disabledInEditableMode: true,

        effects: [{
            startEvents: 'scroll',
            update: '_on_scroll_animation',
        }],


        //--------------------------------------------------------------------------
        /**
         * Called when the window is scrolled
         *
         * @private
         * @param {integer} scroll
         */
        _on_scroll_animation: function (scroll) {
            var self = this;

            var scrollValue = self.$el.find('.js_cls_scroll_animation').scrollTop();
            var winWdith = $(window).width();
            // console.log('\n\n CALLED  1 ====>>',scrollValue)
            // console.log('\n\n CALLED  2 ====>>',winWdith)
            // console.log('\n\n CALLED  3 ====>>',scroll)
        },


    });

    // sh_corpomate_theme_crypto_7 start//
    $(document).ready(function () {


        // new Typed('#typed',{
        //   strings : ["Developments","styles","Designes"],
        //   typeSpeed : 200,
        //   delaySpeed : 1,
        //   loop : true,
        //   backSpeed: 200,
        //   backDelay: 200,
        //   startDelay: 200,
        // });


        $('[data-bs-toggle="popover"]').popover();
    });
    $(document).find('.js_cls_sh_corpomate_theme_flag_btn').click(function () {
        $(document).find(".sh_bottom_nav  #sh_corpomate_lang_dropdown_area").slideToggle('slow')

    })





    $("#sh_corpomate_theme_crypto_7 .testimonial .indicators li").click(function () {
        var i = $(this).index();
        var targetElement = $(".testimonial .tabs li");
        targetElement.eq(i).addClass('active');
        targetElement.not(targetElement[i]).removeClass('active');
    });
    $("#sh_corpomate_theme_crypto_7 .testimonial .tabs li").click(function () {
        var targetElement = $(".testimonial .tabs li");
        targetElement.addClass('active');
        targetElement.not($(this)).removeClass('active');
    });
    $("#sh_corpomate_theme_crypto_7 .slider .swiper-pagination span").each(function (i) {
        $(this).text(i + 1).prepend("0");
    });
    // sh_corpomate_theme_crypto_7 end//

    $(document).find(".sh_header_custom_1 .header_1 > a").click(function (ev) {
        var $shareBtn = $(ev.currentTarget)
        $shareBtn.toggleClass('header_1_links');
        $shareBtn.next('.header_link_share').slideToggle('slow', function () {
            if ($('.header_link_share').is(':hidden')) {
                $('.header_link_share').addClass('arrow_animation')
            }
            else {
                $('.header_link_share').removeClass('arrow_animation')
            }
        })
    });


    // sh_corpomate_theme_accounting_6 start//

    $('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img#link_1').click(function (ev) {
        $('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img').removeClass('active')

        var $img = $(ev.currentTarget);
        $img.addClass('active');
        $('#sh_corpomate_theme_accounting_6 .sh_testimonial_custom #link_1').click()
    })

    $('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img#link_2').click(function (ev) {
        $('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img').removeClass('active')

        var $img = $(ev.currentTarget);
        $img.addClass('active');
        $('#sh_corpomate_theme_accounting_6 .sh_testimonial_custom #link_2').click()
    })

    $('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img#link_3').click(function (ev) {
        $('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img').removeClass('active')

        var $img = $(ev.currentTarget);
        $img.addClass('active');
        $('#sh_corpomate_theme_accounting_6 .sh_testimonial_custom #link_3').click()
    })

    $('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img#link_4').click(function (ev) {
        $('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img').removeClass('active')

        var $img = $(ev.currentTarget);
        $img.addClass('active');
        $('#sh_corpomate_theme_accounting_6 .sh_testimonial_custom #link_4').click()
    })

    $('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img#link_5').click(function (ev) {
        $('#sh_corpomate_theme_accounting_6 .sh_testimonial_links img').removeClass('active')

        var $img = $(ev.currentTarget);
        $img.addClass('active');
        $('#sh_corpomate_theme_accounting_6 .sh_testimonial_custom #link_5').click()
    })


    // sh_corpomate_theme_accounting_6 end//

    $('#sh_corpomate_theme_section_561 .sh_box .js_cls_carousel_link_content').click(function (ev) {
        var $link = $(ev.currentTarget);
        var content = $link.find('img').attr('class');
        if (content) {
            $('#sh_corpomate_theme_section_561 .sh_testimonial_custom .carousel-item').removeClass('active');
            $('#sh_corpomate_theme_section_561 .carousel-indicators li').removeClass('active');
            $('#sh_corpomate_theme_section_561 .carousel-indicators').find('.' + content).addClass('active');
            $('#sh_corpomate_theme_section_561 .sh_testimonial_custom').find('.' + content).addClass('active');
        }
    });

    //hide admin authentication
    $($('.nav-item.dropdown.o_no_autohide_item')[0]).addClass('sh-show-auth-mobile')
    // $($('.nav-item.dropdown.o_no_autohide_item')[0]).click(function (event) {
    //    console.log('HASCAL',$('.sh_social_text').hasClass('ABC'))

    //     $('.sh_social_text').removeClass('ABC')


    // })


});






