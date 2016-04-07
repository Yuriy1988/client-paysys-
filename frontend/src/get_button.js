/**
 * Created by gasya on 22.03.16. DigitalOutlooks corporation.
 */

import ajax from 'axios'

var targetUrl = `${XOPAY_CLIENT_HOST}/api/client/${XOPAY_CLIENT_API_VERSION}/invoices`;

function sendInvoice(invoice) {
    console.log("Request");
    return ajax({
        url: targetUrl,
        data: JSON.stringify(invoice),
        method: "POST",
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
        var invoice = dataPrepare(el.dataset);
        if (validateInvoice(invoice)) {
            sendInvoice(invoice)
                .then(function (response) {
                    switch (response.status) {
                        case 200:
                            location.href = `${XOPAY_CLIENT_HOST}/payment/${response.data.id}`;
                            break;
                        default:
                            alert(response); // TODO CATCH ERROR
                    }
                })
                .catch(function (response) {
                    alert(response); //TODO CATCH ERROR
                });
        } else {
            alert("Invoice is invalid");
        }
    }
};

window.addEventListener("load", function () {
    "use strict";
    document.body.appendChild(render());
});
