/**
 * Created by gasya on 30.03.16.
 * DigitalOutlooks corporation.
 */
import React, { Component } from 'react'
import {InputComponent} from './inputComponent'

export class Field extends InputComponent {
    constructor(props) {
        super(props);
        this.selectionStart = 0;
        this.selectionEnd = 0;
        this.prevValue = "";
    }

    componentWillUpdate() {
        if (this.props.preserveCursor) {
            this.selectionStart = this._input.selectionStart;
            this.selectionEnd = this._input.selectionEnd;
            this.prevValue = this._input.prevValue;
        }
    }

    componentDidUpdate(nextProps, nextState) {
        if (this.props.preserveCursor) {
            if (this.props.value != nextProps.value) {
                var i = 0;
                var c;
                do {
                    c = this._input.value.charAt(this._input.selectionStart + i - 1);
                    i++;
                } while (c == " ");


                this._input.selectionStart = this.selectionStart + i;
                this._input.selectionEnd = this.selectionEnd + i;
            }
        }
    }

    renderChild(props) {
        return (
            <input ref={(c) => this._input = c} className="form-control" {...props}/>
        );
    }
}


export class ComboBox extends InputComponent {
    constructor(props) {
        super(props);
    }

    renderChild(props) {
        return (
            <select className="form-control" {...props}>
                {props.children}
            </select>
        );
    }
}