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
        "postscript" : fields.binary('Postscript File', readonly=True),
        "postscript_name" : fields.char('Invoice Postscript', 40, readonly=True),
    }
    
    def invoice_print_ps(self, cr, uid, ids, context=None):
        inv = {}
        path_module = modules.get_module_path('openerp-postscript-reports')
        invoices = self.browse(cr, uid, ids)
        for invoice in invoices:
            inv.update({'partner_name': invoice.partner_id.name,
                'partner_name' : invoice.partner_id.name,
                'date_invoice' : invoice.date_invoice,
                'fiscal_position_name' : invoice.fiscal_position.name,
                'invoice_amount_untaxed' : invoice.amount_untaxed,
                'invoice_amount_total' : invoice.amount_total,
                'invoice_number' : invoice.number,
                'path': path_module,
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


        subprocess.call(['python', path_module + '/gen_ps.py', str(inv)])

        file = open(path_module +
                    "/" +
                    "invoice" +
                    ".ps", "rb")

        fileContent = file.read()
        out = base64.encodestring(fileContent)

        self.write(cr, uid, ids, {'postscript_name': 'invoice.ps', 'postscript' : out}, context=context)
        file.close()

        #Busco ID de la vista
        obj_model = self.pool.get('ir.model.data')
        model_data_ids = obj_model.search(cr,uid,[('model','=','ir.ui.view'),('name','=','postscript_download')])
        view_id = obj_model.read(cr, uid, model_data_ids, fields=['res_id'])[0]['res_id']

        return {
            'type': 'ir.actions.act_window',
            'title': 'Downloadme',
            'res_model': 'account.invoice',
            'view_id': view_id,
            'view_mode': 'form',
            'res_id': ids[0],
            'target': 'new',
        }


account_invoice()
