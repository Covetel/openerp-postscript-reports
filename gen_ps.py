#!/usr/bin/env python
from pyx import *
import sys, ast

invoice = ast.literal_eval(sys.argv[1])

invoice.update({'rif' : '',
    'invoice_footer1' : "Emitir cheques a nombre de Compania",
    'invoice_footer2' : "Cuenta Tipo Banco Nombre No. Cuenta",})

table_items = ""

table_products_y_pos = 15
tables_x_pos = 2.1

print str(1.72-(tables_x_pos/10))

for line in invoice['invoice_lines']:
    table_items += r"""\centering"""+str(line['invoice_line_quantity'])+r"""&"""+line['invoice_line_name']+r"""& \centering"""+str(line['invoice_line_price_unit'])+r"""&"""+str(line['invoice_line_price_subtotal'])+r"""\\"""

def generate_postscript(invoice_dict):
    text.set(mode="latex")
    text.preamble(r"\usepackage{color}")

    #Canvas
    c = canvas.canvas()

    #Factura
    c.text(13, 19, r"\textbf{Factura N:} \LARGE \textbf{\textcolor{red}{"+str(invoice_dict['invoice_number'])+"}}")

    #Fecha
    c.text(13, 18.5, r"\textbf{Fecha de Emision:} "+str(invoice_dict['date_invoice']))

    #Fecha
    c.text(11, 17.5, "Contribuyente No Sujeto.")

    #Cuadro partner_name o razon social
    c.text(tables_x_pos, 16.9, r"""\begin{tabular*}{"""+str(1.65-(tables_x_pos/10))+r"""\columnwidth}{|p{13cm}|p{3.65cm}|}
      \hline
      \textbf{NOMBRE O RAZON SOCIAL:} """+invoice_dict['partner_name']+r"""& \textbf{RIF:} """+invoice_dict['rif']+r""" \\
      \hline
    \end{tabular*}""")

    c.text(tables_x_pos, 16.46, r"""\begin{tabular*}{"""+str(1.65-(tables_x_pos/10))+r"""\columnwidth}{|p{17.07cm}|}
      \hline
      \textbf{FORMA DE PAGO:} CONTADO \\
      \hline
    \end{tabular*}""")

    #Header tabla productos
    c.text(tables_x_pos, table_products_y_pos, r"""\begin{tabular*}{"""+str(1.65-(tables_x_pos/10))+r"""\columnwidth}{|p{2.3cm}|p{9cm}|p{2.3cm}|p{2.22cm}|}
      \hline
      \centering\textbf{CANTIDAD} & \centering\textbf{CONCEPTO O DESCRIPCION} & \centering\textbf{PRECIO UNITARIO} & \textbf{VALOR TOTAL} \\
      \hline
      """+table_items+r"""
      \hline
    \end{tabular*}""")

    #Total
    c.text(14.3, (table_products_y_pos - 2), r"""\begin{tabular}{r}
    \textbf{Subtotal Gravado Bs.F:} """+str(invoice_dict['invoice_amount_untaxed'])+r""" \\ """+
    r"""\textbf{IVA 0\% Bs.F:} 0.00 \\"""+
    r"""\textbf{Total a Pagar Bs.F:} """+str(invoice_dict['invoice_amount_total'])+r"""\\"""+
    r"""\end{tabular}""")

    #Cuadro invoice_footer (cuenta corriente)
    c.text(tables_x_pos, 1.2, r"""\begin{tabular*}{"""+str(17.7-(tables_x_pos/10))+r"""cm}{|p{"""+str(19.2-tables_x_pos)+r"""cm}|}
      \hline
      """+invoice_dict['invoice_footer1']+r""" \\
      """+invoice_dict['invoice_footer2']+r""" \\
      \hline
    \end{tabular*}""")

    #page = document.paperformat(8.5 inch, 11 inch, name=A0)
    page = document.page(c, paperformat="Letter", centered=0)
    doc = document.document(pages=[page])
    doc.writePSfile(invoice_dict['path']+"/invoice", writebbox=True)

generate_postscript(invoice)
