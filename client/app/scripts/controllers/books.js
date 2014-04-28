'use strict';

var app = angular.module('appApp');

app.controller('BooksCtrl', function ($scope, Books) {
  var self = this;
  Books.query(function(response) {
    self.books = response.result;
  });
  // Namespace controller
  $scope.BooksCtrl = self;
});


app.controller('BookDetailCtrl', function($scope, $routeParams, Books) {
  Books.get({id: $routeParams.id}, function(response) {
    $scope.book = response.result;
    $scope.author = response.result.author;
  });
});
