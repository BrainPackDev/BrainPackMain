/** @odoo-module **/

import { isMobileOS } from "@web/core/browser/feature_detection";
import { _lt } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { url } from "@web/core/utils/urls";
import { isBinarySize } from "@web/core/utils/binary";

const { Component, useState, onWillUpdateProps, onWillStart, onMounted } = owl;


export class reviewUrlIframe extends Component {
    setup() {
        super.setup();
        onMounted(() => {
        });
    }
}

reviewUrlIframe.template = "brainpack_affinda_integration.reviewUrlIframe";

registry.category("fields").add("review_url_iframe", reviewUrlIframe);