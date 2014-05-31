'use strict';

var app = angular.module('appApp');

app.controller('MainCtrl', ['$scope', 'Auth', 'AppAlert', '$location', '$window',
  function ($s, Auth, AppAlert, $location, $window) {
  if ($window.sessionStorage.token) {
    $location.path('/reading/');
  }
  $s.REGISTER = 'register';
  $s.LOGIN = 'login';
  $s.FORM = $s.REGISTER;

  $s.newUser = {
    first: '',
    last: '',
    email: '',
    password: ''
  };

  $s.user = {
    email: '',
    password: ''
  };

  // TODO
  $s.submitRegister = function() {
    console.log('submitting...');
    console.log($s.newUser);
  };

  $s.submitLogin = function() {
    var promise = Auth.login($s.user.email, $s.user.password);
    promise.success(function(resp) {
      var msg = 'Welcome back!';
      AppAlert.add('success', msg);
      $location.path('/reading/');
    });

    promise.error(function(resp) {
      AppAlert.add('danger', resp.message || 'Error: Could not log in. Please try again.');
      console.error(resp);
    });
  };

}]);
