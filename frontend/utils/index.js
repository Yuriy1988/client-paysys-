/**
 * Created by gasya on 30.03.16.
 * DigitalOutlooks corporation.
 */

export { Validator as Validator } from './validator'
export { CreditCard as CreditCard } from './creditCard'
export { Payment as Payment } from './payment'

const possibleChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

export default class Utils {

    static createPaymentUrl(invoiceId) {
        return `${XOPAY_CLIENT_HOST}/api/client/${XOPAY_CLIENT_API_VERSION}/invoices/${invoiceId}/payments`;
    }

    static getPublicKeyUrl() {
        return `${XOPAY_CLIENT_HOST}/api/client/${XOPAY_CLIENT_API_VERSION}/security/public_key`;
    }

    static getAllowedPasystems(id) {
        return `${XOPAY_CLIENT_HOST}/api/client/${XOPAY_CLIENT_API_VERSION}/invoices/${id}/invoice_paysys`;
    }

    static getStatusUrl(paymentId) {
        return `${XOPAY_CLIENT_HOST}/api/client/${XOPAY_CLIENT_API_VERSION}/payment/${paymentId}`;
    }

    static generateSalt(size) {
        var arr = [];
        for (var i = 0; i < size; i++) {
            arr.push(possibleChars[Math.floor(Math.random() * possibleChars.length)]);
        }
        return arr.join("");
    }
}
