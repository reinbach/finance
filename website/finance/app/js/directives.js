'use strict';

/* Directives */


angular.module('financeApp.directives', []).
    directive('appVersion', ['version', function(version) {
        return function(scope, elm, attrs) {
            elm.text(version);
        };
    }]).
    directive('focus', function() {
        return function(scope, element) {
            element[0].focus();
        };
    });
