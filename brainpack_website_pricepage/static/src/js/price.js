odoo.define('brainpack_website_pricepage.price', function (require) {
"use strict";

    $(document).ready(function(){
        $('.bp-pricing .bp-model .bp-toggle').click(function() {
            $(this).toggleClass('bp-monthly bp-yearly');

            $('.bp-plan:not(.bp-plan-static)').toggleClass('d-none');
        });
    })
});