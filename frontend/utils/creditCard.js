/**
 * Created by gasya on 30.03.16.
 * DigitalOutlooks corporation.
 */

export class CreditCard {
    static getIconByNumber(number) {
        switch (number[0]) {
            case "3":
                return "/static/client/img/cc-aexpress-icon.png";
                break;
            case "4":
                return "/static/client/img/cc-visa-icon.png";
                break;
            case "5":
                return "/static/client/img/cc-mastercard-icon.png";
                break;
            case "6":
                return "/static/client/img/cc-maestro-icon.png";
                break;
            default:
                return "/static/client/img/cc-card-icon.png"
        }
    }

    static checkLuhn(card) {
        card = card.replace(/\s/g, "");
        var offset = ((card.length % 2) == 0) ? 1 : 0;
        return card.split("").map(function (item, i) {
                return (((i + offset) % 2 + 1) * parseInt(item))
            }).map(function (item) {
                return (item > 9) ? item - 9 : item;
            }).reduce(function (prev, cur) {
                return prev + cur
            }, 0) % 10 == 0;
    }

    static validator(number) {
        let errors = [];
        if (!(/^\d{12,24}$/.test(number))) {
            errors.push("Card number should contain only 12-24 digits");
        } else if (!CreditCard.checkLuhn(number)) {
            errors.push("Card number is not valid");
        }
        return errors;
    }

    static cvvValidator(cvv) {
        let errors = [];
        if (!(/^\d{3}$/.test(cvv))) {
            errors.push("CVV should contain only 3 digits");
        }
        return errors;
    }

    static ownerValidator(owner) {
        // let errors = [];
        // if (!(/^[\w\s]{2,25}$/.test(owner))) {
        //     errors.push("Cardholder name should contain only 2-25 latin characters");
        // }
        // return errors;
        return [];
    }

    static prepareNumber(number) {
        return number.replace(/(\d{4})/g, (matches, match1, offset, str) => {
            if (offset + match1.length < str.length) {
                return match1 + " "
            } else {
                return match1;
            }
        });
    }

    static mask(number) {
        return number.split("").map((c, i, arr) => (i >= 6 && i < arr.length - 4) ? "*" : c).join("");
    }
}
