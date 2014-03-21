function impresora_fiscal(line1,line2){
    try{
        if (window.XMLHttpRequest)
          {// code for IE7+, Firefox, Chrome, Opera, Safari
          xmlhttp=new XMLHttpRequest();
          }
        else
          {// code for IE6, IE5
          xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
          }
          xmlhttp.open("GET","http://127.0.0.1:8200/"+String(line1)+"___"+String(line2),false);
          xmlhttp.send();
        }catch(err){
    }
}

openerp.plan_cuentas_cooperativas = function (instance) {
    instance.web.client_actions.add('printer.action', 'instance.plan_cuentas_cooperativas.action');
    instance.plan_cuentas_cooperativas.action = function (parent, action) {
        index = [parent.inner_widget.dataset.index];
        id = [parent.inner_widget.dataset.ids[index]];
        //console.log(self.$(".oe_form_field_date").text());
        model_invoice = new instance.web.Model('account.invoice');
        result_invoice = model_invoice.call('dic_invoice', [id]);
        result_invoice.done(function (records) {
            invoice = records;
            impresora_fiscal('ABRIR1',"ABRIR1");
            impresora_fiscal('ESCRIBIR',invoice.invoice_number);
            impresora_fiscal('ESCRIBIR',invoice.date_invoice);
            impresora_fiscal('ESCRIBIR',invoice.partner_name);
            for (var i=0; i< invoice.invoice_lines.length;i++) {
                impresora_fiscal('PRODUCTO',invoice.invoice_lines[i].invoice_line_quantity+"___"+invoice.invoice_lines[i].invoice_line_name+"___"+invoice.invoice_lines[i].invoice_line_price_unit+"___"+invoice.invoice_lines[i].invoice_line_price_subtotal+"_");
            }
            impresora_fiscal("SUBTOTAL",invoice.invoice_amount_untaxed);
            impresora_fiscal("SUBTOTAL",invoice.invoice_amount_tax);
            impresora_fiscal("SUBTOTAL",invoice.invoice_amount_total);
            impresora_fiscal("CERRAR1","CERRAR1");
        });
        //model_invoice.query().filter([['id', '=', id]]).all().done(function (records) {
        //    console.log(_(records));
        //});
    };
};
