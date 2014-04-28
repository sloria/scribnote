'use strict';

describe('Service: Authors', function () {

  // load the service's module
  beforeEach(module('appApp'));

  // instantiate service
  var Authors;
  beforeEach(inject(function (_Authors_) {
    Authors = _Authors_;
  }));

  it('should do something', function () {
    expect(!!Authors).toBe(true);
  });

});
