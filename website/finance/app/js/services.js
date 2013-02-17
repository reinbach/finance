'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('financeApp.services', ['ngResource', 'ngCookies']).
    value('version', '0.1').
    factory('tokenHandler', ['$http', '$cookies', function($http, $cookies) {
        var tokenHandler = {};
        var token = $cookies.authToken || "none";

        tokenHandler.set = function(newToken) {
            token = newToken;
            $cookies.authToken = newToken;
            $http.defaults.headers.common['AuthToken'] = newToken;
        };

        tokenHandler.get = function() {
            return token;
        }

        if (token != "none") {
            tokenHandler.set(token);
        }

        return tokenHandler;
    }]).
    factory('Account', ['$resource', 'api_url',  function($resource, api_url) {
        return $resource(api_url + '/accounts/:accountId', {}, {
            'update': { method: 'PUT'},
        });
    }]).
    factory('AccountType', ['$resource', 'api_url',  function($resource, api_url) {
        return $resource(api_url + '/account/types/:accountTypeId', {});
    }]).
    factory('Transaction', ['$resource', 'api_url',  function($resource, api_url) {
        return $resource(api_url + '/transactions/:transactionId', {}, {
            'update': { method: 'PUT'},
        });
    }]);

