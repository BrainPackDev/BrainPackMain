from odoo import api, fields, models


class Translation(models.Model):
    _name = 'formio.translation'
    _description = 'formio.js Base Translation'
    _order = 'lang_id ASC'

    lang_id = fields.Many2one('res.lang', string='Language', required=True)
    source_id = fields.Many2one('formio.translation.source', string='Source Term', required=True)
    property = fields.Text(related='source_id.property', string='Property', readonly=True)
    value = fields.Text(string='Translation Value', required=True)

    @api.depends('lang_id', 'source_id', 'value')
    def name_get(self):
        res = []
        for r in self:
            name = '{lang}: {source} => {value}'.format(
                lang=r.lang_id.code, source=r.source_id.source, value=r.value
            )
            res.append((r.id, name))
        return res