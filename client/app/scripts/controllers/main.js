'use strict';

var app = angular.module('appApp');

app.controller('MainCtrl', ['$scope', function ($s) {
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

  $s.submitRegister = function() {
    console.log('submitting...');
    console.log($s.newUser);
  };

  $s.submitLogin = function() {
    console.log('submitting login..');
    console.log($s.user);
  };

}]);
