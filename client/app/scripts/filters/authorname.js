'use strict';

angular.module('appApp')
  .filter('authorName', function () {
    return function (author, lastFirst) {
      if (lastFirst) {
        return [author.last, author.first].join(', ');
      } else {
        return [author.first, author.last].join(' ');
      }
    };
  });
