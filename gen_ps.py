#!/usr/bin/env python
from pyx import *
import sys, ast

invoice = ast.literal_eval(sys.argv[1])

invoice.update({'rif' : '',
    'invoice_footer1' : "Emitir cheques a nombre de Compania",
    'invoice_footer2' : "Cuenta Tipo Banco Nombre No. Cuenta",})

table_items = r""" 1 & 2 & 3 & 4 \\
"""

def generate_postscript(invoice_dict):
    text.set(mode="latex")
    text.preamble(r"\usepackage{color}")

    #Canvas
    c = canvas.canvas()

    #Factura
    c.text(18, 19, r"Factura N: \LARGE \textbf{\textcolor{red}{"+str(invoice_dict['invoice_number'])+"}}")

    #Fecha
    c.text(15.7, 18.5, r"\textbf{Fecha de Emision:} "+invoice_dict['date_invoice'])

    #Fecha
    c.text(12, 17.5, "Contribuyente No Sujeto.")

    #Cuadro partner_name o razon social
    c.text(1.1, 16.9, r"""\begin{tabular}{ | c | c | }
      \hline
      \textbf{NOMBRE O RAZON SOCIAL:} """+invoice_dict['partner_name']+r"""& \textbf{RIF:} """+invoice_dict['rif']+r""" \\
      \hline
    \end{tabular}""")

    c.text(1.1, 16.46, r"""\begin{tabular}{ | c | }
      \hline
      \textbf{FORMA DE PAGO:} CONTADO \\
      \hline
    \end{tabular}""")

    #Cuadro forma de pago
    #c.stroke(path.rect(1, 16.3, 19, 0.5))

    #Header tabla productos
    c.text(1, 15, r"""\begin{tabular}{ | c | c | c | c |}
      \hline
      \textbf{CANTIDAD} & \textbf{CONCEPTO O DESCRIPCION} & \textbf{PRECIO UNITARIO} & \textbf{VALOR TOTAL} \\
      \hline
      """+table_items+r"""
      \hline
    \end{tabular}""")

    #Total
    c.text(15.6, 13, r"\textbf{Subtotal Gravado Bs.F:} "+str(invoice_dict['invoice_amount_untaxed']))
    c.text(17, 12.5, r"\textbf{IVA 0\% Bs.F:} 0.00")
    c.text(16.2, 12, r"\textbf{Total a Pagar Bs.F:} "+str(invoice_dict['invoice_amount_total']))

    #Cuadro invoice_footer (cuenta corriente)
    c.text(1, 1.2, r"""\begin{tabular}{ | c |}
      \hline
      """+invoice_dict['invoice_footer1']+r""" \\
      """+invoice_dict['invoice_footer2']+r""" \\
      \hline
    \end{tabular}""")

    #page = document.paperformat(8.5 inch, 11 inch, name=A0)
    page = document.page(c, paperformat="Letter", centered=0)
    doc = document.document(pages=[page])
    doc.writePSfile("invoice", writebbox=True)

generate_postscript(invoice)
