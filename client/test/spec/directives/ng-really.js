'use strict';

describe('Directive: ngReally', function () {

  // load the directive's module
  beforeEach(module('appApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<ng-really></ng-really>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the ngReally directive');
  }));
});
