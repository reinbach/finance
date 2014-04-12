'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
var financeServices = angular.module('financeServices',
                                     ['ngResource', 'ngCookies']);

financeServices.value('version', '0.1');

financeServices.factory(
    'tokenHandler',
    ['$http', '$cookies',
     function($http, $cookies) {
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
     }]);

financeServices.factory(
    'Account',
    ['$resource', 'api_url',
     function($resource, api_url) {
         return $resource(api_url + '/accounts/:accountId', {}, {
             'update': { method: 'PUT'},
         });
     }]);

financeServices.factory(
    'AccountType',
    ['$resource', 'api_url',
     function($resource, api_url) {
         return $resource(api_url + '/account/types/:accountTypeId', {});
     }]);

financeServices.factory(
    'Transaction',
    ['$resource', 'api_url',
     function($resource, api_url) {
         return $resource(api_url + '/transactions/:transactionId', {}, {
             'update': { method: 'PUT'},
         });
     }]);
