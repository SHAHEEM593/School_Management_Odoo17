/** @odoo-module */

import PublicWidget from '@web/legacy/js/public/public_widget';
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";


    PublicWidget.registry.NewEvents = PublicWidget.Widget.extend({
        selector:'.event_snippet',
        start: function(){
        var self = this
        jsonrpc('/latest_event').then(function(data){
        if (data.length > 0){
            data[0].is_active = true
            self.$el.find('#event_snip').html(renderToElement("school_management.event_snipped_carousel", {data: data}))
        }
        })
        return this._super(...arguments)
    },
})