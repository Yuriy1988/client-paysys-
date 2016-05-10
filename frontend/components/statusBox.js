/**
 * Created by gasya on 10.05.16.
 * DigitalOutlooks corporation.
 */
import React, { Component } from "react";
import Utils from '../utils'

export class StatusBox extends Component {
  constructor(props) {
    super(props);
    this.startUpdating = this.startUpdating.bind(this);
    this.stopUpdating = this.stopUpdating.bind(this);
    this.state = {
      status: "NEW"
    }
  }

  componentDidMount() {
    this.startUpdating(1000, (data) => {
      const {id, status} = data;
      this.setState({status});
      if (["SUCCESS", "REJECTED"].indexOf(status) !== -1) {
        this.stopUpdating();
      }
    });
  }

  componentWillUnmount() {
    this.stopUpdating();
  }

  startUpdating(interval, cb) {
    this.stopUpdating();
    this._interval = setInterval(() => {
      if (this.props.paymentId != "new") {
        ajax({
          url: Utils.getStatusUrl(this.props.paymentId),
          dataType: "json"
        }).then((response) => {
          switch (response.status) {
            case 200:
              cb(response.data);
              break;
            default:
              console.log(response); //TODO catch error
          }
        }).catch((error) => console.log(error));
      }
    }, interval)
  }

  stopUpdating() {
    clearInterval(this._interval);
  }

  getStatusName(status) {
    switch (status) {
      case "NEW":
        return "Creating payment";
      case "CREATED":
        return "Payment created";
      case "ACCEPTED":
        return "Payment accepted";
      case "3D_SECURE":
        return "Need 3D secure";
      case "REJECTED":
        return "Payment rejected";
      case "SUCCESS":
        return "Success payment";
    }
  }

  getStatusClass(status) {
    switch (status) {
      case "NEW":
        return "info";
      case "CREATED":
        return "info";
      case "ACCEPTED":
        return "info";
      case "3D_SECURE":
        return "warning";
      case "REJECTED":
        return "danger";
      case "SUCCESS":
        return "success";
    }
  }


  render() {
    const {status} = this.state;
    return (
      <div className={`alert alert-${this.getStatusClass(status)} form-group`}>
        {this.getStatusName(status)}
      </div>
    );
  }
}
