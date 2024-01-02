odoo.define("sh_corpomate_theme.sh_website_quote", function (require) {


    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');


    publicWidget.registry.WebsiteQuoteForm = publicWidget.Widget.extend({
        selector: ".js_cls_website_quote_model_wrapper",
        events: {
            'submit #sh_wq_website_quote_form': '_onSubmitWebsiteQuoteForm',
            'show.bs.modal': '_onModalShow',
        },

        _onSubmitWebsiteQuoteForm: function (e) {
            console.log('\n\n CALLED FORM', e)

            var result = ajax.jsonRpc("/sh_website_quote/contact_us", "call", {
                contact_name: $('input[name="contact_name"]').val(),
                phone: $('input[name="phone"]').val(),
                email_from: $('input[name="email_from"]').val(),
                partner_name: $('input[name="partner_name"]').val(),
                name: $('input[name="name"]').val(),
                description: $('textarea[name="description"]').val(),
            }).then(function (result) {
                console.log('\n\n CALLED result', result)
                if (result) {
                    $("#sh_wq_website_quote_form").hide();
                    $("#sh_wq_website_quote_thankyou_msg").show();
                    $("#sh_wq_website_quote_thankyou_msg").html('<div class="alert alert-success" style="margin-bottom:0px;"><strong>Your message has been sent successfully. We will get back to you shortly.</strong></div>');
                } else {
                    $("#sh_wq_website_quote_thankyou_msg").show();
                    $("#sh_wq_website_quote_thankyou_msg").html('<div class="alert alert-danger" style="margin-bottom:0px;"><strong>Failure to request a quote.</strong></div>');
                }
            });
            return false;
        },

        _onModalShow: function (e) {
            $("#sh_wq_website_quote_form").show();
            $("#sh_wq_website_quote_thankyou_msg").hide();
            $("#sh_wq_website_quote_form")[0].reset();
        }

    });
});
