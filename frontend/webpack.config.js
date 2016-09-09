/**
 * Created by gasya on 28.03.16.
 * DigitalOutlooks corporation.
 */
const path = require('path');
const webpack = require('webpack');
const argumentParser = require("node-argument-parser");

const argv = argumentParser.parse("./arguments.json", process);

//prod
const DEV_MODE = process.env.DEV_MODE == 'true' || false;
const XOPAY_CLIENT_HOST = argv.clientHost || "http://www.xopay.com";
const XOPAY_CLIENT_API_VERSION = argv.clientApiVersion || "dev";


// const DEV_MODE = process.env.DEV_MODE == 'true' || false;
// const XOPAY_CLIENT_HOST = 'http://127.0.0.1:7254'//"http://www.xopay.com"; dev
// const XOPAY_CLIENT_API_VERSION =  "dev";

//Print info
console.log("Configuration:");
console.log("\tClient hostname:\t\t",XOPAY_CLIENT_HOST);
console.log("\tClient api version:\t\t",XOPAY_CLIENT_API_VERSION);
console.log("");

var config = {
    DEV_MODE: DEV_MODE,
    entry: {
        "payment_form": './src/payment_form.js',
        "get_button": './src/get_button.js'
    },
    output: {
        path: path.join(__dirname, '/static/client/js'),
        filename: '[name].js'
    },
    plugins: [
        new webpack.optimize.OccurenceOrderPlugin(),
        new webpack.NoErrorsPlugin(),
        new webpack.DefinePlugin({
            DEV_MODE: DEV_MODE,
            XOPAY_CLIENT_HOST: JSON.stringify(XOPAY_CLIENT_HOST),
            XOPAY_CLIENT_API_VERSION: JSON.stringify(XOPAY_CLIENT_API_VERSION)
        })
    ],
    module: {
        loaders: [
            {
                test: /\.js$/,
                loader: 'babel',
                query: {
                    presets: ['es2015', 'react']
                },
                exclude: /node_modules/,
                include: __dirname
            },
            {
                test: /\.json$/,
                loader: 'json'
            }
        ]
    }
};


if (DEV_MODE == false) { //Production
    config.plugins.push(new webpack.optimize.UglifyJsPlugin());
}

if (DEV_MODE == true) { //Development
    config.devtool = 'cheap-module-eval-source-map';
}

module.exports = config;
