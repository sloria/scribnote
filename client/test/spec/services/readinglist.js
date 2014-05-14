'use strict';

describe('Service: readinglist', function () {

  // load the service's module
  beforeEach(module('appApp'));

  // instantiate service
  var readinglist;
  beforeEach(inject(function (_readinglist_) {
    readinglist = _readinglist_;
  }));

  it('should do something', function () {
    expect(!!readinglist).toBe(true);
  });

});
