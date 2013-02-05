'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('financeApp.services', ['ngResource']).
    value('version', '0.1').
    factory('tokenHandler', ['$http', function($http) {
        var tokenHandler = {};
        var token = "none";

        tokenHandler.set = function(newToken) {
            $http.defaults.headers.common['AuthToken'] = newToken;
        };

        return tokenHandler;
    }]).
    factory('Account', ['$resource', 'api_url',  function($resource, api_url) {
        return $resource(api_url + '/accounts/:accountId', {}, {
            query: {method: 'GET', isArray: true},
            save: {method: 'POST'}
        });
    }]).
    factory('AccountType', ['$resource', 'api_url',  function($resource, api_url) {
        return $resource(api_url + '/account/types/:accountTypeId', {}, {
            query: {method: 'GET', isArray: true},
            save: {method: 'POST'}
        });
    }]);

