/**
 * Created by gasya on 30.03.16.
 * DigitalOutlooks corporation.
 */
import React from 'react'
import {InputComponent} from './inputComponent'

export class CVVInput extends InputComponent {
    constructor(props) {
        super(props);
        this.state = {
            value: "",
            visibility: false
        };
        this.renderButtons = this.renderButtons.bind(this);
        this.renderControl = this.renderControl.bind(this);
        this.showControlHandler = this.showControlHandler.bind(this);
        this.hideControlHandler = this.hideControlHandler.bind(this);
    }

    static getRadnomArray() {
        var numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
        var randomNumbers = [];
        var N = numbers.length;
        for (let i = 0; i < N; i++) {
            randomNumbers.push(numbers.splice(Math.floor(Math.random() * numbers.length), 1))
        }
        return randomNumbers;
    }

    handleClick(i) {
        if (i == 'clear') {
            this.setState({
                value: ""
            })
        } else if (0 <= i && i <= 9) {
            this.setState({
                value: this.state.value + i.toString()
            })
        } else {
            throw new RangeError("should be 0..9 or clear");
        }
    }

    showControlHandler() {
        this.setState({
            visibility: true
        })
    }

    hideControlHandler(e) {

        if (!e.preventClose) {
            this.setState({
                visibility: false
            })
        }
    }

    componentDidMount() {
        this._input.addEventListener("focus", this.showControlHandler);
        this._input.addEventListener("click", this.preventCloseNative);
        document.addEventListener("click", this.hideControlHandler);
    }

    componentWillUnmount() {
        this._input.removeEventListener("focus", this.showControlHandler);
        this._input.removeEventListener("click", this.preventCloseNative);
        document.removeEventListener("click", this.hideControlHandler);
    }

    renderButtons() {
        var self = this;
        return CVVInput.getRadnomArray().map(function (i, ind) {
            return (
                <div className="cvv-btn"
                     onClick={self.handleClick.bind(self, i)}
                     key={ind}>
                    {i}
                </div>
            );
        }).concat([
            <div className="cvv-btn"
                 onClick={self.handleClick.bind(self, 'clear')}
                 key="clear">
                <i className="fa fa-trash"/>
            </div>
        ]);
    }

    preventClose(e) {
        e.nativeEvent.preventClose = true;
    }

    preventCloseNative(e) {
        e.preventClose = true;
    }

    renderControl() {
        if (this.state.visibility) {
            return (
                <div className="cvv-btns-wrapper"
                     onClick={this.preventClose}>
                    {this.renderButtons()}
                </div>
            );
        } else {
            return null;
        }
    }

    renderChild(props) {

        return (
            <div>
                <input value={this.state.value}
                       type="password"
                       className="form-control"
                       ref={(input) => this._input = input}
                />
                {this.renderControl()}
            </div>
        );
    }
}