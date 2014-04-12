'use strict';

/* Filters */

var financeFilters = angular.module('financeFilters', []);

financeFilters.filter('interpolate', ['version', function(version) {
    return function(text) {
        return String(text).replace(/\%VERSION\%/mg, version);
    }
}]);
