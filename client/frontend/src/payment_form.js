/**
 * Created by gasya on 28.03.16.
 * DigitalOutlooks corporation.
 */
import React, {Component} from 'react'
import ReactDOM from 'react-dom'
import { ajax } from 'jquery'

import Utils, { Validator, CreditCard, Payment } from '../utils'
import { Field, ComboBox, CVVInput } from '../components'
import { PAYSYS, DEFAULT_PAYSYS } from '../configs'

class PaymentForm extends Component {
    constructor(props) {
        super(props);
        this.handleDataChange = this.handleDataChange.bind(this);
        this.handleCardNumberChange = this.handleCardNumberChange.bind(this);
        this.handleSubmitForm = this.handleSubmitForm.bind(this);
        this.state = {
            data: {
                card_number: "",
                cardholder_name: "",
                cvv: ""
            },
            paySysId: DEFAULT_PAYSYS
        };
        this.publicKey = "";
        ajax({
            url: Utils.getPublicKeyUrl(),
            dataType: "json"
        }).done((function (data) {
            this.publicKey = data.key
        }).bind(this));
    }

    handleDataChange({target:{name,value}}) { // e.target.name, e.target.value
        this.setState({
            data: Object.assign({}, this.state.data, {
                [name]: value
            })
        })
    }

    handleCardNumberChange(e) {
        this.setState({
            data: Object.assign({}, this.state.data, {
                'card_number': (e.target.value).replace(/\s/g, "")
            })
        })
    }

    validateData(data) {
        return Validator.validate({
            card_number: CreditCard.validator
        }, data)
    }

    handleSubmitForm(e) {
        console.log("Submit");
        Payment.create(this.state.data, this.state.paySysId, this.publicKey)
            .done(function () {

            })
            .fail(function () {

            });
        e.preventDefault();
    }

    render() {
        const { data } = this.state;
        const errors = this.validateData(data);

        return (
            <div className="login-box">

                <div className="login-box-body">
                    {
                        (store.showLogo) ? (
                            <div className="shop-logo-container">
                                <img className="shop-logo" src={store.logo}/>
                            </div>
                        ) : null
                    }
                    <h2>
                        {store.storeName}
                    </h2>
                    <div className="row">
                        <div className="col-xs-12">
                            <div className="form-group">
                                <a href={store.storeUrl} target="_blank"
                                   className="btn btn-warning btn-flat pull-right">
                                    <i className="fa fa-home"/> Visit store
                                </a>
                            </div>
                        </div>
                    </div>

                    <p >{store.description}</p>
                    <h2><strong>{invoice.amount} {invoice.currency}</strong></h2>
                    <form onSubmit={this.handleSubmitForm}>
                        <table>
                            <tbody>
                            <tr>
                                <td width="100%">
                                    <Field name="card_number"
                                           onChange={this.handleCardNumberChange}
                                           value={CreditCard.prepareNumber(data.card_number)}
                                           errors={errors.card_number}
                                           placeholder="1234 5678 9012 3456"
                                           label="Card number"
                                           preserveCursor={true}
                                    />
                                </td>
                                <td style={{verticalAlign:"top"}}>
                                    <div className="cc-icon-wrapper">
                                        <img src={CreditCard.getIconByNumber(data.card_number)}/>
                                    </div>
                                </td>
                            </tr>
                            </tbody>
                        </table>


                        <Field icon="user"
                               name="cardholder_name"
                               onChange={this.handleDataChange}
                               value={data.cardholder_name}
                               errors={errors.cardholder_name}
                               placeholder="Ivanov Ivan"
                               label="Cardholder name"
                        />

                        <Field icon="key"
                               name="cvv"
                               onChange={this.handleDataChange}
                               type="password"
                               value={data.cvv}
                               errors={errors.cvv}
                               placeholder="123"
                               label="CVV"
                        />


                        <CVVInput name="cvv"
                                  onChange={this.handleDataChange}
                                  type="password"
                                  value={data.cvv}
                                  errors={errors.cvv}
                                  placeholder="123"
                                  label="CVV"
                        />

                        <div className="row">
                            <div className="col-xs-6">
                                <ComboBox name="month"
                                          onChange={this.handleDataChange}
                                          value={data.month}
                                          errors={errors.month}
                                          placeholder="01"
                                          label="Month">
                                    {
                                        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].map(function (i) {
                                            let val = i.toString();
                                            val = (val.length < 2) ? ("0" + val) : val;
                                            return <option key={i} value={val}>{val}</option>;
                                        })
                                    }
                                </ComboBox>
                            </div>
                            <div className="col-xs-6">
                                <Field icon="key"
                                       name="year"
                                       onChange={this.handleDataChange}
                                       value={data.year}
                                       errors={errors.year}
                                       placeholder="2016"
                                       label="Year"
                                />
                            </div>
                        </div>


                        <Field icon="envelope"
                               name="notify_by_email"
                               onChange={this.handleDataChange}
                               value={data.notify_by_email}
                               errors={errors.notify_by_email}
                               placeholder="example@example.com"
                               label="Notify by Email"
                        />

                        <Field icon="phone"
                               name="notify_by_phone"
                               onChange={this.handleDataChange}
                               value={data.notify_by_phone}
                               errors={errors.notify_by_phone}
                               placeholder="+380991234567"
                               label="Notify by Phone"
                        />

                        <div className="row">
                            <div className="col-xs-12">
                                <button type="submit" className="btn btn-success btn-flat btn-block">
                                    <i className="fa fa-credit-card"/> Submit Payment
                                </button>
                            </div>
                        </div>
                    </form>
                    <div className="row">
                        <hr />
                        <div className="col-xs-12">
                            <a href="/" className="pull-right" target="_blank"><b>XOP</b>ay</a>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}


ReactDOM.render(<PaymentForm />, document.getElementById("root"));
