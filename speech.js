'use strict';

var express = require('express'),
    app = express(),
    vcapServices = require('vcap_services'),
    extend = require('util')._extend,
    watson = require('watson-developer-cloud'),
    bluemix = require('./config/bluemix'),
    i18n = require('i18next');

//i18n settings
// require('./config/i18n')(app);

// Bootstrap application settings
require('./config/express')(app);

// For local development, replace username and password
var config = extend({
    version: 'v1',
    "url": "https://stream.watsonplatform.net/speech-to-text/api",
    "username": "f10cdd68-c1f4-4a06-96fc-ed15ab867f10",
    "password": "wZbS5lNtI5YM"
}, vcapServices.getCredentials('speech_to_text'));

var authService = watson.authorization(config);

app.get('/speech', function (req, res) {
    res.render('speech', { ct: req._csrfToken });
});

// Get token using your credentials
app.post('/api/speech/token', function (req, res, next) {
    authService.getToken({ url: config.url }, function (err, token) {
        if (err)
            next(err);
        else
            res.send(token);
    });
});

// error-handler settings
require('./config/error-handler')(app);

// var port = process.env.VCAP_APP_PORT || 3000;
var port = process.env.PORT || 3000;
app.listen(port);
console.log('listening at:', port);
