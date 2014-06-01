'use strict';

var app = angular.module('appApp');

app.factory('Author', function ($http, serverConfig) {
  var baseURL = serverConfig.DOMAIN + '/api/authors/';

  function Author(data) {
    angular.extend(this, data);
  }

  Author.get = function(id) {
    return $http.get(baseURL + id).then(function(response) {
        return new Author(response.data.result);
    });
  };

  Author.query = function() {
    return $http.get(baseURL).then(function(resp) {
        var authorDataArray = resp.data.result;
        return authorDataArray.map(function(authorData) {
            return new Author(authorData);
        });
    });
  };

  return Author;

});


