odoo.define('brainpack_invoice_sale_portal_sign.name_and_signature', function (require) {
'use strict';

var core = require('web.core');
var config = require('web.config');
var utils = require('web.utils');
var Widget = require('web.Widget');
var NameAndSignature = require('web.name_and_signature');

NameAndSignature.NameAndSignature.include({
     getCompanyName: function () {
        return this.$('.o_web_sign_company_name_input').val();
    },
     getCompanyNumber: function () {
        return this.$('.o_web_sign_company_number_input').val();
    },
    getBehalfOfCompany: function () {
        return this.$('.o_web_sign_behalf_of_company_input').is(':checked')
    },
});


});