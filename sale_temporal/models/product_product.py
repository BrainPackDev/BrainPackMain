# -*- coding: utf-8 -*-


from odoo import models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _get_best_pricing_rule(self, **kwargs):
        """Return the best pricing rule for the given duration.

        :return: least expensive pricing rule for given duration
        :rtype: product.pricing
        """
        return self.product_tmpl_id._get_best_pricing_rule(product=self, **kwargs)
