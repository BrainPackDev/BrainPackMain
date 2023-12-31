/** @odoo-module **/

import { registerPatch } from '@mail/model/model_core';
import { attr, many, one } from '@mail/model/model_field';

registerPatch({
    name: 'Chatter',
        fields: {
            isMessageFailedBoxVisible: attr({
                default: true,
            }),
        },
        recordMethods: {
            async refresh() {
                this._super(...arguments);
                if(this.thread){
                    this.thread.refreshMessagefailed();
                }
            },
            toggleMessageFailedBoxVisibility() {
                this.update({
                    isMessageFailedBoxVisible: !this.isMessageFailedBoxVisible,
                });
            },
            _onThreadIdOrThreadModelChanged() {
                this._super(...arguments);
                if(this.thread){
                    this.thread.refreshMessagefailed();
                }
            },
        },
});
