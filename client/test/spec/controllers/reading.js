'use strict';

describe('Controller: ReadingCtrl', function () {

  // load the controller's module
  beforeEach(module('appApp'));

  var ReadingCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    ReadingCtrl = $controller('ReadingCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
