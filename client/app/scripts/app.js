'use strict';
var app = angular.module('appApp', [
  'ngResource',
  'ngRoute',
  'ui.bootstrap',
  'drahak.hotkeys',
  'relativeDate'
]);

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

    .when('/authors', {
      templateUrl: 'views/authors.html',
      controller: 'AuthorsCtrl'
    })
    .when('/authors/:id', {
      templateUrl: 'views/author.html',
      controller: 'AuthorDetailCtrl'
    })

    .when('/reading', {
      templateUrl: 'views/reading.html',
      controller: 'ReadingCtrl'
    })
    .otherwise({
      redirectTo: '/'
    });
};

app.config(routeConfig);

app.value('serverConfig', {
  DOMAIN: 'http://localhost:5000'
});

// Interceptor that sends auth information if available on session storage
app.factory('authInterceptor', function($rootScope, $q, $window) {
  return {
    request: function(config) {
      config.headers = config.headers || {};
      var token = $window.sessionStorage.token;
      if (token) {
        config.headers.Authorization = 'Basic ' + btoa(token + ':' + '');
      }
      return config;
    },
    responseError: function(rejection) {
      if (rejection.status === 401) {
        delete $window.sessionStorage.token;
        // TODO: handle case where user not authenticated
      }
      return $q.reject(rejection);
    }
  };
});

app.config(function($httpProvider) {
  $httpProvider.interceptors.push('authInterceptor');
});
