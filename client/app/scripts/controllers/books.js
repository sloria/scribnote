'use strict';

var app = angular.module('appApp');

app.controller('BooksCtrl', function ($scope, $http, Books) {
  var self = this;
  Books.query(function(response) {
    self.books = response.result;
  });
  $scope.BooksCtrl = self;
});
