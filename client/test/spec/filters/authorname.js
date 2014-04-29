'use strict';

describe('Filter: authorName', function () {

  // load the filter's module
  beforeEach(module('appApp'));

  // initialize a new instance of the filter before each test
  var authorName;
  beforeEach(inject(function ($filter) {
    authorName = $filter('authorName');
  }));

  it('should return the input prefixed with "authorName filter:"', function () {
    var text = 'angularjs';
    expect(authorName(text)).toBe('authorName filter: ' + text);
  });

});
