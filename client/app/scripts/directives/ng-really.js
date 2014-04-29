'use strict';

angular.module('appApp')
  .directive('ngReally', function () {
    return {
      restrict: 'A',
      link: function postLink(scope, element, attrs) {
        element.bind('click', function() {
            var msg = attrs.ngReallyMessage;
            if (msg && confirm(msg)) {
                scope.$apply(attrs.ngReally);
            };
        })
      }
    };
  });
