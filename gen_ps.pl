#!/usr/bin/env perl
use Template;
use strict;
use warnings;
use lib qw(lib);
use Number::Format;
use Data::Dumper;
use JSON qw( decode_json );

my $invoice_from_python = shift;

$invoice_from_python =~ s/u'/'/g;
$invoice_from_python =~ s/'/"/g;

my $invoice = decode_json($invoice_from_python);

print Dumper($invoice->{"path"}.'/report/');

my $tt = Template->new({
		       INCLUDE_PATH => $invoice->{"path"}.'/report/',
		       INTERPOLATE => 1,
}) || die "$Template::ERROR\n";

my @items;

foreach my $item (@{$invoice->{"invoice_lines"}}) {
    push  @items,{
        qty => $item->{"invoice_line_quantity"},
        desc => $item->{"invoice_line_name"},
        unit_price => &number_format($item->{"invoice_line_price_unit"}),
        total_price => &number_format($item->{"invoice_line_price_subtotal"}),
    };
}

my $vars = {
   invoice => {
       id => $invoice->{"invoice_number"},
       date => &date_format($invoice->{"date_invoice"}),
       client => {
            name => $invoice->{"partner_name"},
            id => "",
       },
       paymentform => "CONTADO",
       sub_total => &number_format($invoice->{"invoice_amount_untaxed"}),
       iva => 0.00,
       total => &number_format($invoice->{"invoice_amount_total"}),
   },
};

$vars->{'invoice'}->{'items'} = \@items;

$tt->process('invoice.tt2', $vars, $invoice->{"path"}.'/invoice.ps') || die $tt->error(), "\n";

sub number_format {
    my $n = shift;
    my $format = new Number::Format(
        THOUSANDS_SEP   => '.',
        DECIMAL_POINT   => ',',
    );

    return$format->format_number($n);
}

sub date_format {
    my $d = shift;
    my $year = substr($d, 0, 4);
    my $month = substr($d, 5, 2);
    my $day = substr($d, 8, 2);

    return $day."-".$month."-".$year;
}
