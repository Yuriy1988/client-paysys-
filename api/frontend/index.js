/**
 * Created by gasya on 28.03.16.
 * DigitalOutlooks corporation.
 */

var webpack = require('webpack');
var config = require('./webpack.config');
var compiler = webpack(config);

console.log("[WEBPACK] start");

compiler.run(function (err, stats) {
    if (!err) {
        console.log("[WEBPACK] building finished");
    } else {
        console.error("[WEBPACK] ERROR! building FAILED!");
    }
});
