# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (c) 2010-2013 Elico Corp. All Rights Reserved.
#    Author: Yannick Gouin <yannick.gouin@elico-corp.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime
import time, subprocess, base64
from osv import fields, osv
from openerp import modules, tools

class account_invoice(osv.osv):
    _name = "account.invoice"
    _inherit = "account.invoice"

    _columns = {
        "postscript" : fields.binary("File", readonly=True),
    }
    
    def invoice_print_ps(self, cr, uid, ids, context=None):
        inv = {}
        invoices = self.browse(cr, uid, ids)
        for invoice in invoices:
            inv.update({'partner_name': invoice.partner_id.name,
                'partner_name' : invoice.partner_id.name,
                'date_invoice' : invoice.date_invoice,
                'fiscal_position_name' : invoice.fiscal_position.name,
                'invoice_amount_untaxed' : invoice.amount_untaxed,
                'invoice_amount_total' : invoice.amount_total,
                'invoice_number' : invoice.number,
            })

            invoice_lines = invoice.invoice_line
            inv_lines  = []
            inv_line = {}

            for invoice_line in invoice_lines:
                inv_line.update({'invoice_line_name' : invoice_line.name,
                    'invoice_line_price_subtotal' : invoice_line.price_subtotal,
                    'invoice_line_price_unit' : invoice_line.price_unit,
                    'invoice_line_quantity' : invoice_line.quantity,})

                inv_lines.append(inv_line)

                inv.update({'invoice_lines' : inv_lines})

        path_module = modules.get_module_path('openerp-postscript-reports')

        subprocess.call(['python', path_module + '/gen_ps.py', str(inv)])

        file = open(path_module +
                    "/" +
                    "invoice" +
                    ".ps", "rb")

        fileContent = file.read()
        out = base64.encodestring(fileContent)

        self.write(cr, uid, ids, {'postscript' : out}, context=context)
        file.close()

        url =  self.browse(cr, uid, ids)[0].postscript

account_invoice()
