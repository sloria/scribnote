'use strict';

var app = angular.module('appApp');

app.controller('ReadingCtrl', function ($scope, ReadingList, AppAlert) {
  $scope.books = [];

  ReadingList.get().then(function(books) {
    $scope.books = books;
  }, function(error) {
    AppAlert.add('danger', 'Could not fetch books. Please try again later.');
  });

});
