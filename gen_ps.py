#!/usr/bin/env python
from pyx import *

factura = 000
fecha = "16-02-2014"
nombre = "Nombre Cliente"
rif = "X-00000000-0"
cant = 1
desc = "asdadad"
pu = 970
vt = pu * cant
footer1="Emitir cheques a nombre de Compania"
footer2="Cuenta Tipo Banco Nombre No. Cuenta"

table_items = r""" 1 & 2 & 3 & 4 \\
"""

text.set(mode="latex")
text.preamble(r"\usepackage{color}")

#Canvas
c = canvas.canvas()

#Factura
c.text(18, 19, r"Factura N: \LARGE \textbf{\textcolor{red}{"+str(factura)+"}}")

#Fecha
c.text(15.7, 18.5, r"\textbf{Fecha de Emision:} "+fecha)

#Fecha
c.text(12, 17.5, "Contribuyente No Sujeto.")

#Cuadro nombre o razon social
c.text(1.1, 16.9, r"""\begin{tabular}{ | c | c | }
  \hline
  \textbf{NOMBRE O RAZON SOCIAL:} """+nombre+r"""& \textbf{RIF:} """+rif+r""" \\
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
c.text(15.6, 13, r"\textbf{Subtotal Gravado Bs.F:} "+str(vt))
c.text(17, 12.5, r"\textbf{IVA 0\% Bs.F:} 0.00")
c.text(16.2, 12, r"\textbf{Total a Pagar Bs.F:} "+str(vt))

#Cuadro footer (cuenta corriente)
c.text(1, 1.2, r"""\begin{tabular}{ | c |}
  \hline
  """+footer1+r""" \\
  """+footer2+r""" \\
  \hline
\end{tabular}""")

#page = document.paperformat(8.5 inch, 11 inch, name=A0)
page = document.page(c, paperformat="Letter", centered=0)
doc = document.document(pages=[page])
doc.writePSfile("test", writebbox=True)
