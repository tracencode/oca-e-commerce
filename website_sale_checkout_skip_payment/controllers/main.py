# Copyright 2017 Sergio Teruel <sergio.teruel@tecnativa.com>
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.website_sale.controllers.main import WebsiteSale

from odoo import http, SUPERUSER_ID
from odoo.http import request


class CheckoutSkipPaymentWebsite(WebsiteSale):

    @http.route('/shop/payment/validate/skip', type='http', auth="public", website=True, sitemap=False)
    def shop_payment_skip(self, sale_order_id=None, **post):

        if not sale_order_id:
            return request.redirect('/shop')
        else:
            sale_order_ids = sale_order_id.split(',')
            vals = {}

            for order_id in sale_order_ids:
                order = request.env['sale.order'].sudo().browse(int(order_id))

                if not order.partner_id.skip_website_checkout_payment:
                    return request.redirect('/shop')

                if order.exists() and order.state not in ('sale', 'done', 'cancel'):
                    order.with_context(send_email=True).with_user(SUPERUSER_ID).action_quotation_send()
                    vals = {'order_name': order.name}
            request.session['skip_payment_vals'] = vals
            return request.redirect('/shop/confirmation')
