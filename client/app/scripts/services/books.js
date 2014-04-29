'use strict';

var app = angular.module('appApp');

app.factory('Book', function ($resource, $http, serverConfig) {
  var baseURL = serverConfig.DOMAIN + '/api/books/';

  function Book(data) {
    angular.extend(this, data);
  }

  // Static method to get book by id
  Book.get = function(id) {
    return $http.get(baseURL + id).then(function(response) {
        return new Book(response.data.result);
    });
  };

  // instance method to create new book
  Book.create = function(params) {
    return $http.post(baseURL, params).then(function(resp) {
        return new Book(resp.data.result);
    });
  };

  // GET all books
  Book.query = function() {
    return $http.get(baseURL).then(function(resp) {
        var bookDataArray = resp.data.result;
        return bookDataArray.map(function(bookData) {
            return new Book(bookData);
        })
    });
  };

  // Delete a book
  Book.delete = function(id) {
    return $http.delete(baseURL + id);
  };

  return Book;
});
