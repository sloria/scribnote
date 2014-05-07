'use strict';

var app = angular.module('appApp');

app.controller('MainCtrl', ['$scope', 'Auth', 'AppAlert',
  function ($s, Auth, AppAlert) {
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
      AppAlert.add('success', 'Success!');
    });
    promise.error(function(resp, status) {
      AppAlert.add('danger', 'Error: Could not log in. Please try again.');
      console.error(resp);
    });
  };

}]);
