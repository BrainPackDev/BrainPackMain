from odoo import _, api, fields, models, modules, Command
import json
from odoo.osv import expression
from collections import defaultdict

class Channel(models.Model):

    _inherit = 'mail.channel'

    def channel_info_custom(self):
        """ Get the informations header for the current channels
            :returns a list of channels values
            :rtype : list(dict)
        """
        if not self:
            return []
        channel_infos = []
        rtc_sessions_by_channel = self.sudo().rtc_session_ids._mail_rtc_session_format_by_channel()
        channel_last_message_ids = dict((r['id'], r['message_id']) for r in self._channel_last_message_ids())
        current_partner = self.env['res.partner']
        current_guest = self.env['mail.guest']
        guest = self.env['mail.guest']._get_guest_from_context()
        if self.env.user._is_public and guest:
            current_guest = guest
        else:
            current_partner = self.env.user.partner_id
        all_needed_members_domain = expression.OR([
            [('channel_id.channel_type', '!=', 'channel')],
            [('rtc_inviting_session_id', '!=', False)],
            [('partner_id', '=', current_partner.id) if current_partner else expression.FALSE_LEAF],
            [('guest_id', '=', current_guest.id) if current_guest else expression.FALSE_LEAF],
        ])
        all_needed_members = self.env['mail.channel.member'].search \
            (expression.AND([[('channel_id', 'in', self.ids)], all_needed_members_domain]), order='id')
        all_needed_members.partner_id.sudo().mail_partner_format()  # prefetch in batch
        members_by_channel = defaultdict(lambda: self.env['mail.channel.member'])
        invited_members_by_channel = defaultdict(lambda: self.env['mail.channel.member'])
        member_of_current_user_by_channel = defaultdict(lambda: self.env['mail.channel.member'])
        for member in all_needed_members:
            members_by_channel[member.channel_id] |= member
            if member.rtc_inviting_session_id:
                invited_members_by_channel[member.channel_id] |= member
            if (current_partner and member.partner_id == current_partner) or \
                    (current_guest and member.guest_id == current_guest):
                member_of_current_user_by_channel[member.channel_id] = member
        for channel in self:
            channel_data = {
                'avatarCacheKey': channel._get_avatar_cache_key(),
                'channel_type': channel.channel_type,
                'id': channel.id,
                'memberCount': channel.member_count,
            }
            info = {
                'id': channel.id,
                'name': channel.name,
                'defaultDisplayMode': channel.default_display_mode,
                'description': channel.description,
                'uuid': channel.uuid,
                'state': 'open',
                'is_minimized': False,
                'group_based_subscription': bool(channel.group_ids),
                'create_uid': channel.create_uid.id,
                'authorizedGroupFullName': channel.group_public_id.full_name,
            }
            # add last message preview (only used in mobile)
            info['last_message_id'] = channel_last_message_ids.get(channel.id, False)
            # # find the channel member state
            # if current_partner or current_guest:
            #     info['message_needaction_counter'] = channel.message_needaction_counter
            #     member = member_of_current_user_by_channel.get(channel, self.env['mail.channel.member']).with_prefetch(
            #         [m.id for m in member_of_current_user_by_channel.values()])
            #     if member:
            #         channel_data['channelMembers'] = [('insert', list(member._mail_channel_member_format().values()))]
            #         info['state'] = member.fold_state or 'open'
            #         channel_data['serverMessageUnreadCounter'] = member.message_unread_counter
            #         info['is_minimized'] = member.is_minimized
            #         info['seen_message_id'] = member.seen_message_id.id
            #         channel_data['custom_channel_name'] = member.custom_channel_name
            #         info['is_pinned'] = member.is_pinned
            #         info['last_interest_dt'] = member.last_interest_dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            #         if member.rtc_inviting_session_id:
            #             info['rtc_inviting_session'] = {'id': member.rtc_inviting_session_id.id}
            # # add members info
            # if channel.channel_type != 'channel':
            #     # avoid sending potentially a lot of members for big channels
            #     # exclude chat and other small channels from this optimization because they are
            #     # assumed to be smaller and it's important to know the member list for them
            #     channel_data['channelMembers'] = [
            #         ('insert', list(members_by_channel[channel]._mail_channel_member_format().values()))]
            #     info['seen_partners_info'] = sorted([{
            #         'id': cp.id,
            #         'partner_id': cp.partner_id.id,
            #         'fetched_message_id': cp.fetched_message_id.id,
            #         'seen_message_id': cp.seen_message_id.id,
            #     } for cp in members_by_channel[channel] if cp.partner_id], key=lambda p: p['partner_id'])
            # # add RTC sessions info
            # info.update({
            #     'invitedMembers': [('insert', list(invited_members_by_channel[channel]._mail_channel_member_format(
            #         fields={'id': True, 'channel': {}, 'persona': {'partner': {'id', 'name', 'im_status'},
            #                                                        'guest': {'id', 'name', 'im_status'}}}).values()))],
            #     'rtcSessions': [('insert', rtc_sessions_by_channel.get(channel, []))],
            # })

            info['channel'] = channel_data

            channel_infos.append(info)
        return channel_infos