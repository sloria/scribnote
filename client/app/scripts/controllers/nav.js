'use strict';

angular.module('appApp')
  .controller('NavCtrl', function ($scope, $location, Auth, AppAlert) {
    $scope.logout = function() {
      Auth.logout();
      $location.path('/');
      AppAlert.add('info', 'You have successfully logged out');
    };

    $scope.isAuthenticated = function() {
      return Auth.isAuthenticated();
    };
  });
