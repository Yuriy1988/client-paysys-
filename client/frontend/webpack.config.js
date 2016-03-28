/**
 * Created by gasya on 28.03.16.
 * DigitalOutlooks corporation.
 */
const path = require('path');
const webpack = require('webpack');

const DEV_MODE = process.env.DEV_MODE == 'true' || false;

var config = {
    DEV_MODE: DEV_MODE,
    entry: [
        './src/index'
    ],
    output: {
        path: path.join(__dirname, '../static/js'),
        filename: 'payment_form.js'
    },
    plugins: [
        new webpack.optimize.OccurenceOrderPlugin(),
        new webpack.NoErrorsPlugin(),
        new webpack.DefinePlugin({
            DEV_MODE: DEV_MODE
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
