'use strict';

describe('Service: Note', function () {

  // load the service's module
  beforeEach(module('appApp'));

  // instantiate service
  var Note;
  beforeEach(inject(function (_Note_) {
    Note = _Note_;
  }));

  it('should do something', function () {
    expect(!!Note).toBe(true);
  });

});
