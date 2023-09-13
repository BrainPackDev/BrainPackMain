/** @odoo-module **/
import { registerPatch } from '@mail/model/model_core';
import { attr, many, one } from '@mail/model/model_field';

registerPatch({
    name: 'Thread',
    fields: {
        fetchMessagesParams: {
            compute() {
                let stringifiedDomain = "[]";
                for (const threadView of this.threadViews) {
                  if (threadView.stringifiedDomain && threadView.stringifiedDomain != "[]") {
                    stringifiedDomain = threadView.stringifiedDomain;
                  }
                }
                if (stringifiedDomain != "[]") {
                  stringifiedDomain = JSON.parse(stringifiedDomain);
                }
                if (this.model === 'mail.channel') {
                    if(stringifiedDomain == "[]"){
                        return { 'channel_id': this.id };
                    }
                    return { 'channel_id': this.id ,'stringifiedDomain':stringifiedDomain};
                }
                if (this.mailbox) {
                    if(stringifiedDomain != "[]"){
                        return {
                            'stringifiedDomain':stringifiedDomain,
                        };
                    }
                    return {}
                }
                if(stringifiedDomain != "[]"){
                    return {
                        'thread_id': this.id,
                        'thread_model': this.model,
                        'stringifiedDomain':stringifiedDomain,
                    };
                }
                return {
                    'thread_id': this.id,
                    'thread_model': this.model,
                };
            },
        },
    },
});