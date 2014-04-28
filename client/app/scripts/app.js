'use strict';
var app = angular.module('appApp', ['ngResource', 'ngRoute']);

var routeConfig = function($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'views/main.html',
      controller: 'MainCtrl'
    })
    .when('/books', {
      templateUrl: 'views/books.html',
      controller: 'BooksCtrl'
    })
    .when('/books/:id', {
      templateUrl: 'views/book.html',
      controller: 'BookDetailCtrl'
    })
    .otherwise({
      redirectTo: '/'
    });
};

app.config(routeConfig);

app.value('serverConfig', {
  DOMAIN: 'http://localhost:5000'
});
