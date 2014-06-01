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
    .when('/login', {
      templateUrl: 'views/login.html',
      controller: 'LoginCtrl'
    })
    .otherwise({
      redirectTo: '/'
    });
};

app.config(routeConfig);

app.value('serverConfig', {
  DOMAIN: 'http://localhost:5000'
});

app.factory('authTokenInterceptor', function($window, $q, $injector, $location) {
  var onSuccess = function(response) {
    return response;
  };

  // On error, we'll try to get a new token and return the response for the
  // original request
  var onError = function(response) {
    // TODO: set retry refresh token limit
    if (response.status === 401) {
      var deferred = $q.defer(); // defer until we can request a new token

      var onTokenSuccess = function(tokenResponse) {
        if (tokenResponse.data) {
          // Set token on root scope
          // TODO: Use session storage to store the token
          $window.sessionStorage.token = tokenResponse.data.result;
          // Now try the original request
          $injector.get('$http')(response.config).then(function(origResponse) {
            // Resolve the original request
            deferred.resolve(origResponse);
          }, function() { // something went wrong; reject the original request
            deferred.reject();
          });
        } else { // Login failed to return a token
          deferred.reject();
        }
      };

      // When token issue fails, redirect to sigin
      var onTokenError = function() {
        deferred.reject();
        $location.path('/login');
        return;
      };

      // Make the token request
      // TODO: Remove hardcoded domain
      var domain = 'http://localhost:5000';
      // Try to reissue token
      var tokenURL = domain + '/api/refresh_token';
      // Can't get http directly becase we're in the config stage
      $injector.get('$http').get(tokenURL).then(
        onTokenSuccess, onTokenError
      );
    }
    return $q.reject(response);  // unrecoverable error
  };

  return function(promise) {
    return promise.then(onSuccess, onError);
  };
});

// TODO: merge request and response interceptors into one factory?
app.factory('authRequestInterceptor', function($rootScope, $q, $window) {
  return {
    request: function(config) {
      config.headers = config.headers || {};
      var token = $window.sessionStorage.token;
      if (token) {
        config.headers.Authorization = 'Bearer ' + token;
      }
      return config;
    }
  };
});


app.config(function($httpProvider) {
  $httpProvider.responseInterceptors.push('authTokenInterceptor');
  $httpProvider.interceptors.push('authRequestInterceptor');
});

