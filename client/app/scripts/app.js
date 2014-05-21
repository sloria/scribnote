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
    if (response.status === 401) {
      var deferred = $q.defer(); // defer until we can request a new token
      // Can't get http directly becase we're in the config stage

      // Try to reissue token

      var onTokenSuccess = function(tokenResponse) {
        if (tokenResponse.data) {
          // Set token on root scope
          // TODO: Use session storage to store the token
          $window.sessionStorage.auth.token = tokenResponse.data.result;
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
      // TODO: JSON-P?
      var domain = 'http://localhost:5000';
      var tokenURL = domain + '/api/token';
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

app.config(function($httpProvider) {
  $httpProvider.responseInterceptors.push('authTokenInterceptor');
});

app.run(['$window', '$injector', function($window, $injector) {
  $window.sessionStorage.auth = {};
  // Modify every http request to append auth token if it is available
  var transformRequest = function(data, headersGetter) {
    var token = $window.sessionStorage.auth.token;
    if (token) {
      headersGetter().Authorization = 'Basic ' + btoa(token + ':' + '');
    }
    if (data) {
      return angular.toJson(data);
    }
  };
  $injector.get('$http').defaults.transformRequest = transformRequest;
}]);
