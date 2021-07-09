var createError = require('http-errors');
var express = require('express');
var path = require('path');

var indexRouter = require('./routes/index');
var news = require('./routes/news');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, '../client/build/'));
app.set('view engine', 'jade'); 
app.use('/static', express.static(path.join(__dirname, '../client/build/static/')));

app.all('*', function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  next();
});

app.use('/', indexRouter);
app.use('/news', news);
// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

module.exports = app;
