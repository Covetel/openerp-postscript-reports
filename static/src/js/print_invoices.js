openerp.plan_cuentas_cooperativas = function (instance) {
    instance.web.client_actions.add('printer.action', 'instance.plan_cuentas_cooperativas.action');
    instance.plan_cuentas_cooperativas.action = function (parent, action) {
        id = [parent.inner_widget.dataset.index];
        //console.log(self.$(".oe_form_field_date").text());
        model_invoice = new instance.web.Model('account.invoice');
        result_invoice = model_invoice.call('dic_invoice', [id]);
        result_invoice.done(function (records) {
            invoice = records;
            console.log(invoice);
        });    
        //model_invoice.query().filter([['id', '=', id]]).all().done(function (records) {
        //    console.log(_(records));
        //});
    };
};
