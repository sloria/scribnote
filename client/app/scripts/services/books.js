'use strict';

var app = angular.module('appApp');

app.factory('Books', function ($resource, serverConfig) {
  var url = serverConfig.DOMAIN + '/api/books/:id';
  return $resource(url, {id: '@result.id'},
    {
      query: { isArray: false }
    });
});
