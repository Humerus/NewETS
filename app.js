var express = require('express');
var api = require('./routes/api');
var http = require('http');
var path = require('path');

var app = express();

app.set('port', process.env.PORT || 8080);
app.use(express.logger('dev'));
app.use(express.bodyParser());

app.use(express.methodOverride());
app.use(express.cookieParser('food'));
app.use(express.session());

app.use(app.router);
app.use(express.static(path.join(__dirname, 'public')));
app.enable('trust proxy');

app.use(express.errorHandler());

app.get('/', function(req, res) {
    res.sendfile(__dirname + '/public/index.html');
});

app.use(function(req, res, next) {
    res.status(404);
    res.redirect("/");
});

http.createServer(app).listen(app.get('port'), function() {
    console.log('Express server listening on port ' + app.get('port'));
});
