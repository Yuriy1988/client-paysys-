/**
 * Created by gasya on 22.03.16. DigitalOutlooks corporation.
 */

import { ajax } from 'jquery'

var targetUrl = `${XOPAY_CLIENT_HOST}/api/client/${XOPAY_CLIENT_API_VERSION}/invoices`;
//targetUrl = "http://192.168.1.160:7128/api/admin/version";

function sendInvoice(invoice) {
    console.log("Request");
    return ajax({
        url: targetUrl,
        data: JSON.stringify(invoice),
        method: "POST", //TODO POST
        dataType: "json",
        headers: {
            "Content-Type": "application/json"
        }
    });
}

function validateInvoice(invoice) {
    return true; //TODO write validation
}

function render() {
    var root = document.createElement("link");
    root.rel = "stylesheet";
    root.href = `${XOPAY_CLIENT_HOST}/static/client/css/get-button.css`;
    return root;
}


function dataPrepare(invoice) {
    var newInvoice = {};
    newInvoice.order_id = invoice.order_id;
    newInvoice.store_id = invoice.store_id;
    newInvoice.currency = invoice.currency;
    newInvoice.items = JSON.parse(invoice.items);
    return newInvoice;
}

document.onclick = function (event) {
    var el = event.target;
    if (el.dataset.xopay) {

        /*
         order_id: string,			// {required}
         store_id: string,			// {required}, from $Store
         currency: enum,			// {required}, one of Currency Enum
         items: [
         ____{
         ________store_item_id: string,		// {required}
         ________quantity: integer,	    // {required}
         ________unit_price: decimal,	// {required}
         ________item_name: string
         ____},
         ...
         ]
         */

        var invoice = dataPrepare(el.dataset);
        if (validateInvoice(invoice)) {
            sendInvoice(invoice)
                .done(function (data) {
                    location.href = `${XOPAY_CLIENT_HOST}/payment/${data.id}`;
                })
                .fail(function (jqXHR, textStatus, errorThrown) {
                    console.log(textStatus);
                });
        } else {
            alert("Invoice is invalid");
        }
    }
};

document.body.appendChild(render());
