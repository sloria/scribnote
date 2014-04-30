'use strict';

var app = angular.module('appApp');

app.factory('AppAlert', function ($rootScope, $timeout) {

  $rootScope.alerts = [];
  var alertService =  {
    add: function(type, msg) {
      $rootScope.alerts.push({
        type: type,
        msg: msg,
        close: function() {
          alertService.closeAlert(this);
        },
      });
      $timeout(function() {
        $rootScope.alerts.pop();
      }, 2000);
    },

    closeAlert: function(alert) {
      this.closeAlertIdx($rootScope.alerts.indexOf(alert));
    },
    closeAlertIdx: function(index) {
      $rootScope.alerts.splice(index, 1);
    }
  };
  return alertService;

});
