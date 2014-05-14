'use strict';

var app = angular.module('appApp');

// TODO: Use separate service for Book model
app.factory('ReadingList', function ($http, serverConfig) {
  var baseUrl = serverConfig.DOMAIN + '/api/reading/';

  function Book(data) {
    angular.extend(this, data);
    this.createdDate = new Date(data.created);
  }

  function ReadingList() {}

  ReadingList.get = function() {
    return $http.get(baseUrl).then(function(response) {
      var bookArray = response.data.result;
      return bookArray.map(function(bookData) {
        return new Book(bookData);
      });
    });
  }

  return ReadingList;


});
