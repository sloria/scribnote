'use strict';

var app = angular.module('appApp');

app.directive('syncFocus', function($timeout, $rootScope) {
  return {
    restrict: 'A',
    scope: {
      focusValue: "=syncFocus"
    },
    link: function($scope, $element, attrs) {
      $scope.$watch('focusValue', function(currentValue, previousValue) {
        if (currentValue === true && !previousValue) {
          $element[0].focus();
        } else if (currentValue === false && previousValue) {
          $element[0].blur();
        }
      })
    }
  }
});

