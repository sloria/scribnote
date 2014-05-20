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

// Interceptor that sends auth information if available on session storage
app.factory('authInterceptor', function($rootScope, $q, $window, $location) {
  return {
    request: function(config) {
      config.headers = config.headers || {};
      var token = $window.sessionStorage.token;
      if (token) {
        config.headers.Authorization = 'Basic ' + btoa(token + ':' + '');
      }
      return config || $q.when(config);
    },
    responseError: function(rejection) {
      if (rejection.status === 401) {
        delete $window.sessionStorage.token;
        $location.path('/login');
        // TODO: handle case where user not authenticated
      }
      return $q.reject(rejection);
    }
  };
});

app.config(function($httpProvider) {
  $httpProvider.interceptors.push('authInterceptor');
});

app.run(['$rootScope', '$injector', function($rootScope, $injector) {
  // Modify every http request to append auth token if it is available
  var transformRequest = function(data, headersGetter) {
    if ($rootScope.auth) {
      var token = $rootScope.auth.token;
      headersGetter().Authorization = 'Basic ' + btoa(token + ':' + '');
    }
    if (data) {
      return angular.toJson(data);
    }
  };
  $injector.get('$http').defaults.transformRequest = transformRequest;
}]);
