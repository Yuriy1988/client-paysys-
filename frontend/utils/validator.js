/**
 * Created by gasya on 30.03.16.
 * DigitalOutlooks corporation.
 */

export class Validator {
    static validate(validators, data, hard = false) {
        let resultErrors = {};
        for (let key in validators) {
            if (hard || data[key]) {
                let errors = validators[key](data[key]);
                if (!(errors instanceof Array)) throw  new TypeError("Validator should return an array of errors (strings)");
                if (errors.length != 0) {
                    resultErrors[key] = errors;
                }
            }
        }
        return resultErrors;
    }
}