/**
 * Created by gasya on 22.03.16. DigitalOutlooks corporation.
 */
(function (d, w) {
    var targetUrl = "{{create_invoice_url}}"; // TODO put invoice_url
    targetUrl = "http://192.168.1.111:5000/api/client/dev/invoices";
    function createRequest() {
        var xmlhttp;
        try {
            xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
        } catch (e) {
            try {
                xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
            } catch (E) {
                xmlhttp = false;
            }
        }
        if (!xmlhttp && typeof XMLHttpRequest != 'undefined') {
            xmlhttp = new XMLHttpRequest();
        }
        return xmlhttp;
    }

    function sendInvoice(invoice, cb) {
        window.console.log("Request");
        var request = createRequest();

        window.console.log("Request created", request);
        request.onreadystatechange = function () {
            window.console.log("STATUSC", request);
            if (request.readyState == 4) { // Ответ пришёл
                if (request.status == 200) {
                    cb(request, null); //OK
                } else {
                    cb(null, request); // Error
                }
            }
        };
        request.open('POST', targetUrl, true);
        request.setRequestHeader('Content-Type', 'application/json');
        request.send(JSON.stringify(invoice));
    }

    function validateInvoice(invoice) {
        return true; //TODO write validation
    }

    function render() {
        var root = d.createElement("div");
        //var button = d.createElement("button");
        var styles = d.createElement("link");
        styles.rel = "stylesheet";
        styles.href = "{{ROOT}}{{ url_for('static', filename='css/get-button.css') }}";
        root.appendChild(styles);
        //root.appendChild(button);
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

    d.onclick = function (event) {
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
                sendInvoice(invoice, function (result, err) {
                    if (err) {
                        window.console.log("ERRORRESP", err)
                    } else {
                        var serverInvoice = JSON.parse(result.responseText);
                        window.console.log(serverInvoice);
                        window.console.log("redirection");
                        // window.location.href = "http://localhost:5000/payment/" + serverInvoice.id;
                    }

                    window.console.log("Res", result);
                    window.console.log("Err", err);
                })
            } else {
                window.alert("Invoice is invalid");
            }
        }
    };

    d.body.appendChild(render());
})(document, window);
