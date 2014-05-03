/**
 * An editable blockquote, similar to X-editable.
 */
'use strict';

var app = angular.module('appApp');

app.directive('editableQuote', function () {
  return {
    templateUrl: 'scripts/directives/editable-quote.html',
    transclude: true,
    restrict: 'E',
    scope: {
      eqText: '@',
      eqRows: '@',
      eqCols: '@',
      eqSubmit: '&',
      eqCiteAuthor: '@',
      eqCiteTitle: '@',
      eqPlaceholder : '@'
    },
    link: function postLink(scope) {
      var oldText = scope.eqText;

      scope.EDITING = 'e';
      scope.VIEWING = 'v';
      scope.MODE = scope.VIEWING;

      // Enable text editing
      scope.activate = function() {
        scope.MODE = scope.EDITING;
      };

      // Disable text editing
      scope.deactivate = function() {
        scope.MODE = scope.VIEWING;
      };

      scope.submit = function() {
        scope.eqSubmit({newText: scope.eqText, oldText: oldText});
        scope.MODE = scope.VIEWING;
      };
    }
  };
});
