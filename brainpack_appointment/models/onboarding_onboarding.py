# coding: utf-8

from odoo import api, models


class Onboarding(models.Model):
    _inherit = 'onboarding.onboarding'

    # Appointment Onboarding
    @api.model
    def action_close_appointment_onboarding(self):
        onboarding = self.env.ref('brainpack_appointment.appointment_onboarding_panel', raise_if_not_found=False)
        if onboarding:
            onboarding.action_close()
