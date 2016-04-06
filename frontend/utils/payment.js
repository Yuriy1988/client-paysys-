/**
 * Created by gasya on 30.03.16.
 * DigitalOutlooks corporation.
 */
import ajax from 'axios'
import Utils, {CreditCard} from '../utils'
import RSA from 'node-rsa'

export class Payment {
    static create(data, paySysId, publicKey) {
        return ajax({
            url: Utils.createPaymentUrl(invoice.id),
            data: Payment.prepareData(data, paySysId, publicKey),
            method: "POST",
            dataType: "json",
            headers: {
                "Content-Type": "application/json"
            }
        })
    }

    static prepareData(data, paySysId, publicKey) {

        var result = {
            paysys_id: paySysId,
            payment_account: CreditCard.mask(data.card_number),
            crypted_payment: Payment.encryptPayment(data, publicKey)
        };

        if (data.notify_by_email) result.notify_by_email = data.notify_by_email;
        if (data.notify_by_phone) result.notify_by_phone = data.notify_by_phone;
        /**
         * > POST /api/client/{version}/invoices/<invoice_id>/payments
         {
             paysys_id: enum,		// id платежной системы,один из Paysys id enum
             crypted_payment: Base64String($CryptedPayment)		// {required}  платежные реквизиты клиента в ЗАШИФРОВАННОМ открытым ключем виде! (возможно в формате PEM)
             payment_account: string,	// {required} для Visa/Master - номер карточки, для PayPal - email, ...)
             notify_by_email: email,	// уведомить о результате платежа по email (если null или отсутствует - не уведомлять)
             notify_by_phone: phone	// уведомить о результате платежа по sms (если null или отсутствует - не уведомлять)
         }
         */
        return result;
    }

    static encryptPayment(data, publicKey) {
        var encrypter = new RSA(publicKey);
        return encrypter.encrypt(JSON.stringify({
            card_number: data.card_number,		// {required, digits only, len 12-24} номер карточки
            cardholder_name: data.cardholder_name,	// {required, english letters} имя владельца карты
            cvv: data.cvv,			// {required, digits only, fix len} CVV код
            expiry_date: data.expiry_date,		// {required, format "mm/yyyy"} дата действия карты
            salt: Utils.generateSalt(64)			// {required} набор случайных данных для усиления шифрования
        }), "base64");
    }
}

window.Payment = Payment;