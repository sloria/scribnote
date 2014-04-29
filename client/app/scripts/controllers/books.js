'use strict';

var app = angular.module('appApp');

app.controller('BooksCtrl', function ($scope, Book) {
  var self = this;

  self.error = null;
  self.books = [];
  Book.query().then(function(books) {
    self.books = books;
  }, function(error) {
    self.error = 'Could not fetch books. Please try again later.';
  });

  self.addForm = {
    active: false,
    first: null,
    last: null,
    title: null,
    submit: function() {
      Book.create({
        title: this.title,
        author_first: this.first,
        author_last: this.last
      })
      .then(function(newBook) {
        self.books.push(newBook);
        self.addForm.active = false;
      });
    }
  };



  self.addBook = function() {
    self.addForm.active = true;
  };
  // Namespace controller
  $scope.BooksCtrl = self;
});


app.controller('BookDetailCtrl', function($scope, $routeParams, Book) {
  Book.get($routeParams.id).then(function(book) {
    $scope.book = book;
  }, function(error) {
    console.log('Could not retrieve book');
  })
});
