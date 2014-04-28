'use strict';

var app = angular.module('appApp');

app.controller('AuthorsCtrl', function ($scope, Authors) {
  Authors.query(function(response) {
    $scope.authors = response.result;
  });
});


app.controller('AuthorDetailCtrl', function($scope, $routeParams, Authors) {
  Authors.get({id: $routeParams.id}, function(response) {
    $scope.author = response.result;
  });
});
