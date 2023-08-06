'use strict';

var schedulizer = angular.module('homeApp').
  config(['$routeProvider',
    function config($routeProvider) {
      $routeProvider.
      when('/', {
        template: '<home></home>'
      }).
      otherwise('/');
  }
]);