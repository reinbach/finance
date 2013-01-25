'use strict';


// Declare app level module which depends on filters, and services
angular.module('financeApp', ['financeApp.filters', 'financeApp.services', 'financeApp.directives']).
    constant('api_url', 'http://localhost:5000/').
    config(['$routeProvider', function($routeProvider) {
        $routeProvider.when('/login', {templateUrl: 'partials/login.html', controller: FinanceCtrlLogin});
        $routeProvider.when('/accounts', {templateUrl: 'partials/accounts.html', controller: FinanceCtrlAccounts});
        $routeProvider.otherwise({redirectTo: '/login'});
    }]).
    config(function($httpProvider) {
        var interceptor = ['$location', '$q', function($location, $q) {
            function success(response) {
                return response;
            };

            function error(response) {
                if (response.status == 401) {
                    var deferred = $q.defer();
                    $location.path("/login");
                    return deferred.promise;
                };
                return $q.reject(response);
            };

            return function(promise) {
                return promise.then(success, error);
            };
        }];

        $httpProvider.responseInterceptors.push(interceptor);
    });
