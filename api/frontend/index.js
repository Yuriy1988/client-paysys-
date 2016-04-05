/**
 * Created by gasya on 28.03.16.
 * DigitalOutlooks corporation.
 */

var webpack = require('webpack');
var config = require('./webpack.config');
var compiler = webpack(config);

const DEV_MODE = process.env.DEV_MODE == 'true' || false;

const S_WEBPACK = "WEBPACK";

log(S_WEBPACK, "start");

if (DEV_MODE) {
    log(S_WEBPACK, "ENV=development");
    compiler.watch({
        aggregateTimeout: 300,
        poll: true
    }, function (err, stats) {
        if (!err) {
            log(S_WEBPACK, "building finished");
        } else {
            log(S_WEBPACK, "ERROR! building FAILED!");
        }
    });
} else {
    log(S_WEBPACK, "ENV=production");
    compiler.run(function (err, stats) {
        console.log(stats);
        if (!err) {
            log(S_WEBPACK, "building finished");
        } else {
            log(S_WEBPACK, "ERROR! building FAILED!");
        }
    });
}


function log(sender, msg, type) {
    switch (type) {
        case "E":
            console.error(`${(new Date()).toLocaleString()} [${sender}] ${msg}`);
            break;
        default:
            console.log(`${(new Date()).toLocaleString()} [${sender}] ${msg}`);
    }
}