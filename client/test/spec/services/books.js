'use strict';

describe('Service: Books', function () {

  // load the service's module
  beforeEach(module('appApp'));

  // instantiate service
  var Books;
  beforeEach(inject(function (_Books_) {
    Books = _Books_;
  }));

  it('should do something', function () {
    expect(!!Books).toBe(true);
  });

});
