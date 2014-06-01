'use strict';

var app = angular.module('appApp');

app.controller('AuthorsCtrl', function ($scope, Author, AppAlert) {
  Author.query().then(function(authors){
    $scope.authors = authors;
  }, function(error) {
    AppAlert.add('danger', 'Could not fetch authors. Please try again later.');
  });
});


app.controller('AuthorDetailCtrl', function($scope, $routeParams, Author) {
  Author.get($routeParams.id).then(function(author) {
    $scope.author = author;
  });
});
