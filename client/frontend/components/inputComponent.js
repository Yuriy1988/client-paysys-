/**
 * Created by gasya on 04.04.16.
 * DigitalOutlooks corporation.
 */
import React, { Component } from 'react'

export class InputComponent extends Component {
    constructor(props) {
        super(props);
        this.renderAddon = this.renderAddon.bind(this);
        this.hasAddon = this.hasAddon.bind(this);
    }

    renderAddon() {
        const {icon} = this.props;
        if (!icon) return null;
        return (
            <span className="input-group-addon">
                <i className={`fa fa-${icon}`}/>
            </span>
        );
    }

    hasAddon() {
        const {icon} = this.props;
        return (!!icon);
    }

    renderChild() {
        return null;
    }

    render() {
        const { errors=[], label, children } = this.props;
        const props = Object.assign({}, this.props);
        delete props.icon;
        delete props.errors;
        delete props.label;

        return (
            <div className={`form-group ${(errors.length > 0) ? "has-error" : ""}`}>
                {
                    (label) ? <label>{label}</label> : null
                }
                <div className={`${(this.hasAddon())?"input-group ":""}`}>
                    {this.renderChild(props)}
                    {this.renderAddon()}
                </div>
                { errors.map((error, i)=><span key={i} className="help-block">{error}</span>) }
            </div>
        );
    }
}