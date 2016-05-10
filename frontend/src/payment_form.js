/**
 * Created by gasya on 28.03.16.
 * DigitalOutlooks corporation.
 */
import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import ajax from 'axios'
import 'babel-polyfill'

import Utils, { Validator, CreditCard, Payment } from '../utils'
import { Field, ComboBox, CVVInput, StatusBox } from '../components'
import { PAYSYS, DEFAULT_PAYSYS } from '../configs'

class PaymentForm extends Component {
  constructor(props) {
    super(props);
    this.handleDataChange = this.handleDataChange.bind(this);
    this.handleCardNumberChange = this.handleCardNumberChange.bind(this);
    this.handleSubmitForm = this.handleSubmitForm.bind(this);
    this.hideError = this.hideError.bind(this);
    this.hideInfo = this.hideInfo.bind(this);

    this.initData.call(this);

    this.state = {
      data: {
        card_number: "",
        cardholder_name: "",
        cvv: ""
      },
      paySysId: DEFAULT_PAYSYS,
      paymentId: null,
      error: "",
      info: "",
      hardValidation: false
    };
    this.publicKey = "";


    ajax({
      url: Utils.getPublicKeyUrl(),
      dataType: "json"
    }).then((function (response) {
      switch (response.status) {
        case 200:
          this.publicKey = response.data.key;
          break;
        default:
          console.log(response); //TODO catch error
      }
    }).bind(this));
  }

  initData() {
    const months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
    const currentYear = (new Date()).getFullYear();
    const years = [];
    for (var i = 0; i < 8; i++) {
      years.push(currentYear + i);
    }

    this.months = months;
    this.years = years;
  }

  handleDataChange({target:{name, value}}) { // e.target.name, e.target.value
    this.setState({
      hardValidation: false,
      data: Object.assign({}, this.state.data, {
        [name]: value
      })
    })
  }

  handleCardNumberChange(e) {
    this.setState({
      hardValidation: false,
      data: Object.assign({}, this.state.data, {
        'card_number': (e.target.value).replace(/\s/g, "")
      })
    })
  }

  validateData(data, hard = false) {
    return Validator.validate({
      card_number: CreditCard.validator,
      cvv: CreditCard.cvvValidator,
      cardholder_name: CreditCard.ownerValidator
    }, data, hard)
  }

  handleSubmitForm(e) {
    e.preventDefault();
    const self = this;
    const {data, paySysId} = this.state;

    if (this.validateData(data, true).__count == 0) {
      self.setState({
        paymentId: "new"
      });
      Payment.create(data, paySysId, this.publicKey)
        .then(function (response) {
          //self.setState({info: "Good"}); //TODO
          self.setState({
            paymentId: response.data.id
          });
          //debugger;
        })
        .catch(function (response) {
          self.setState({
            error: "Something went wrong",
            paymentId: null
          });
          debugger;
        });
    } else {
      this.setState({
        hardValidation: true
      })
    }
  }

  hideError() {
    this.setState({error: ""})
  }

  hideInfo() {
    this.setState({info: ""})
  }

  render() {
    const {data, hardValidation} = this.state;
    const errors = this.validateData(data, hardValidation);

    return (
      <div className="login-box">
        {this.renderError(this.state.error, this.hideError)}
        {this.renderInfo(this.state.info, this.hideInfo)}

        <div className="login-box-body">
          {
            (store.showLogo) ? (
              <div className="shop-logo-container">
                <img className="shop-logo" src={store.logo}/>
              </div>
            ) : null
          }

          <h2>
            <a href={store.storeUrl} target="_blank"
            >
              <i className="fa fa-home"/> {store.storeName}
            </a>
          </h2>

          <p >{store.description}</p>
          <h2><strong>{invoice.total_price} {invoice.currency}</strong></h2>

          {
            (this.state.paymentId) ?
              this.renderStatus(this.state.paymentId)
              : (
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

                <div className="row">
                  <div className="col-xs-3">
                    <CVVInput name="cvv"
                              onChange={this.handleDataChange}
                              type="password"
                              value={data.cvv}
                              errors={errors.cvv}
                              placeholder="123"
                              label="CVV"
                    />
                  </div>
                  <div className="col-xs-9">
                    <div className="row">
                      <div className="col-xs-6">

                        <ComboBox name="month"
                                  onChange={this.handleDataChange}
                                  value={data.month}
                                  errors={errors.month}
                                  placeholder="01"
                                  label="Exp.Month">
                          {
                            this.months.map(function (i) {
                              let val = i.toString();
                              val = (val.length < 2) ? ("0" + val) : val;
                              return <option key={i} value={val}>{val}</option>;
                            })
                          }
                        </ComboBox>
                      </div>
                      <div className="col-xs-6">
                        <ComboBox name="year"
                                  onChange={this.handleDataChange}
                                  value={data.year}
                                  errors={errors.year}
                                  placeholder="2016"
                                  label="Exp.Year">
                          {
                            this.years.map(function (i) {
                              let val = i.toString();
                              val = (val.length < 2) ? ("0" + val) : val;
                              return <option key={i} value={val}>{val}</option>;
                            })
                          }
                        </ComboBox>
                      </div>
                    </div>
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
            )
          }

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

  renderError(error, onClose = ()=>1) {
    if (error) {
      return (
        <div className="alert alert-danger alert-dismissable form-group">
          <button type="button" className="close" onClick={onClose}>×</button>
          {error}
        </div>
      )
    }
  }

  renderStatus(paymentId) {
    if (paymentId) {
      return (
        <StatusBox paymentId={paymentId}/>
      );
    }
  }

  renderInfo(info, onClose = ()=>1) {
    if (info) {
      return (
        <div className="alert alert-info alert-dismissable form-group">
          <button type="button" className="close" onClick={onClose}>×</button>
          {info}
        </div>
      )
    }
  }
}


ReactDOM.render(<PaymentForm />
  , document.getElementById("root"));
