'use strict';

var app = angular.module('appApp');

app.controller('BooksCtrl', function ($scope, Book) {

  $scope.error = null;
  $scope.books = [];
  Book.query().then(function(books) {
    $scope.books = books;
  }, function(error) {
    $scope.error = 'Could not fetch books. Please try again later.';
  });

  $scope.addForm = {
    active: false,
    first: null,
    last: null,
    title: null,
    activate: function() {
      $scope.addForm.active = true;
    },
    deactivate: function() {
      $scope.addForm.active = false;
    },
    submit: function() {
      var bookPromise = Book.create({
        title: this.title,
        author_first: this.first,
        author_last: this.last
      })

      bookPromise.then(function(newBook) {
        $scope.books.push(newBook);
        $scope.addForm.active = false;
      }, function(error) {
        $scope.error('An error occurred while creating the book. Please try again later.');
      });
    }
  };

  $scope.delete = function(book, index) {
    Book.delete(book.id).then(function() {
      $scope.books.splice(index, 1);
    }, function(error) {
      console.error(error);
      $scope.error('An error occurred on the server.');
    });
  };

});


app.controller('BookDetailCtrl', function($scope, $routeParams, Book) {
  // Initialize variables
  $scope.book = {};
  $scope.author = {};
  Book.get($routeParams.id)
    .then(function(book) {
      $scope.book = book;
      $scope.author = book.author;
    }, function(error) {
      console.log('Could not retrieve book');
  });

});
