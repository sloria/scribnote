'use strict';

var app = angular.module('appApp');

app.factory('Auth', function ($http, $window, serverConfig) {
  var authURL = serverConfig.DOMAIN + '/api/authenticate';
  return {

    isAuthenticated: function() {
      return $window.sessionStorage.token != null;
    },

    /**
     * Log in a user by sending a request for a JWT, and saving the token to
     * sessionStorage.
     */
    login: function(username, password) {
      var promise = $http.post(authURL, {username: username, password: password});

      promise.success(function(response) {
        $window.sessionStorage.token = response.token;
      });

      promise.error(function() {
        delete $window.sessionStorage.token;
      });

      return promise;
    },

    /**
     * Log out by deleting the current token.
     */
    logout: function() {
      delete $window.sessionStorage.token;
    }

  };
});
