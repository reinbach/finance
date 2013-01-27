'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('financeApp.services', ['ngResource']).
    value('version', '0.1').
    factory('Account', function($resource, api_url) {
        return $resource(api_url + '/accounts/:accountId', {}, {
            query: {method: 'GET', params: {accountId: ''}, isArray: true}
        });
    });
