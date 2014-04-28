'use strict';

var app = angular.module('appApp');

app.controller('BooksCtrl', function ($scope, Books) {
  var self = this;

  self.addForm = {
    active: false,
    first: null,
    last: null,
    title: null,
    submit: function() {
      var payload = {
        title: this.title,
        author_first: this.first,
        author_last: this.last
      };
      console.log(payload);
    }
  };

  Books.query(function(response) {
    self.books = response.result;
  });

  self.addBook = function() {
    self.addForm.active = true;
  };
  // Namespace controller
  $scope.BooksCtrl = self;
});


app.controller('BookDetailCtrl', function($scope, $routeParams, Books) {
  Books.get({id: $routeParams.id}, function(response) {
    $scope.book = response.result;
    $scope.author = response.result.author;
  });
});
