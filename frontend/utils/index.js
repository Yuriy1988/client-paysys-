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
        return "http://192.168.1.118:5000/api/client/dev/public_key"; //TODO delete
        //return `${XOPAY_CLIENT_HOST}/api/client/${XOPAY_CLIENT_API_VERSION}/public_key`;
    }

    static generateSalt(size) {
        var arr = [];
        for (var i = 0; i < size; i++) {
            arr.push(possibleChars[Math.floor(Math.random() * possibleChars.length)]);
        }
        return arr.join("");
    }
}