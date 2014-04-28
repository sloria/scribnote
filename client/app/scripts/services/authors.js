'use strict';

var app = angular.module('appApp');

app.factory('Authors', function ($resource, serverConfig) {
  var url = serverConfig.DOMAIN + '/api/authors/:id';
  return $resource(url, {id: '@result.id'},
    {
      query: { isArray: false }
    });
});


