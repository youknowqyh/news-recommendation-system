var cors = require('cors');


var createError = require('http-errors');
var express = require('express');
var passport = require('passport');
var path = require('path');
var bodyParser = require('body-parser');

var auth = require('./routes/auth');
var indexRouter = require('./routes/index');
var news = require('./routes/news');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, '../client/build/'));
app.set('view engine', 'jade'); 
app.use('/static', express.static(path.join(__dirname, '../client/build/static/')));



// app.all('*', function(req, res, next) {
//   res.header("Access-Control-Allow-Origin", "*");
//   res.header("Access-Control-Allow-Headers", "X-Requested-With");
//   next();
// });
// TODO: remove this when deployment
app.use(cors());
app.use(bodyParser.json());

var config = require('./config/config.json');
require('./models/main.js').connect(config.mongoDbUri);

app.use(passport.initialize());
var localSignupStrategy = require('./passport/signup_passport');
var localLoginStrategy = require('./passport/login_passport');
passport.use('local-signup', localSignupStrategy);
passport.use('local-login', localLoginStrategy);

// pass the authenticaion checker middleware
const authCheckMiddleware = require('./middleware/auth_check');
app.use('/news', authCheckMiddleware);

app.use('/', indexRouter);
app.use('/auth', auth);
app.use('/news', news);
// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

module.exports = app;
