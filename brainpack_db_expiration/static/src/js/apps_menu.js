/** @odoo-module **/
var { NavBar } = require("@web/webclient/navbar/navbar");
var { patch } = require("web.utils");
const { useListener } = require("@web/core/utils/hooks");
const {useRef, useState ,onMounted} = owl;
import { session } from "@web/session";

patch(NavBar.prototype, "brainpack_db_expiration.appsMenuJs", {
    setup() {
        this._super();
        
        var self = this;
        onMounted(() => {
            if (session.database_block_message) {
                $(".database_block_message").html(
                    session.database_block_message
                );

                if (!session.database_block_is_warning) {
                    $(".o_action_manager").block({
                        message: $(".block_ui.database_block_message").html(
                            session.database_block_message
                        ),
                    });
//                    $("header").css("z-index", $.blockUI.defaults.baseZ + 20);
                }

                if (session.database_block_show_message_in_apps_menu) {
                    $(".database_block_message").show();
                }
            }
        });
    },
});