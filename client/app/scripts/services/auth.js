'use strict';

var app = angular.module('appApp');

app.factory('Auth', function ($http, $window, serverConfig) {
  var tokenUrl = serverConfig.DOMAIN + '/api/authenticate/';
  return {

    /**
     * Log in a user by sending a request for a JWT, and saving the token to
     * sessionStorage.
     */
    login: function(username, password) {
      var promise = $http.post(tokenUrl, {username: username, password: password});

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
