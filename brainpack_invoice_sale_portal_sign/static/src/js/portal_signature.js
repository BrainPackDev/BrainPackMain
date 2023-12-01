odoo.define('brainpack_invoice_sale_portal_sign.signature_form', function (require) {
'use strict';

    var SignatureForm = require('portal.signature_form');

    SignatureForm.SignatureForm.include({
        start: function () {
            var self = this
            debugger;
            return this._super.apply(this, arguments).then(function () {
                self.quotation = false
                if($('.o_portal_signature_form').data('quotation') && $('.o_portal_signature_form').data('quotation') == 'True'){
                    self.quotation = true
                }
                if(!self.quotation){
                    $('.o_portal_signature_form').find('.o_web_sign_company_name_group').remove();
                    $('.o_portal_signature_form').find('.o_web_sign_company_number_group').remove();
                    $('.o_portal_signature_form').find('.o_web_sign_behalf_of_company_group').remove();
                }
            });


        },
        _onClickSignSubmit: function (ev) {
        var self = this;
        ev.preventDefault();

        if (!this.nameAndSignature.validateSignature()) {
            return;
        }

        var name = this.nameAndSignature.getName();
        var signature = this.nameAndSignature.getSignatureImage()[1];
        var company_name = this.nameAndSignature.getCompanyName();
        var company_number = this.nameAndSignature.getCompanyNumber();
        var behalf_of_company = this.nameAndSignature.getBehalfOfCompany();

        return this._rpc({
            route: this.callUrl,
            params: _.extend(this.rpcParams, {
                'name': name,
                'signature': signature,
                'company_name': company_name,
                'company_number': company_number,
                'behalf_of_company': behalf_of_company,
            }),
        }).then(function (data) {
            if (data.error) {
                self.$('.o_portal_sign_error_msg').remove();
                self.$controls.prepend(qweb.render('portal.portal_signature_error', {widget: data}));
            } else if (data.success) {
                var $success = qweb.render('portal.portal_signature_success', {widget: data});
                self.$el.empty().append($success);
            }
            if (data.force_refresh) {
                if (data.redirect_url) {
                    window.location = data.redirect_url;
                } else {
                    window.location.reload();
                }
                // no resolve if we reload the page
                return new Promise(function () { });
            }
        });
    },
    });

});
