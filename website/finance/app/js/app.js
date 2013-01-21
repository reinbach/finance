'use strict';


// Declare app level module which depends on filters, and services
angular.module('financeApp', ['financeApp.filters', 'financeApp.services', 'financeApp.directives']).
    config(['$routeProvider', function($routeProvider) {
        $routeProvider.when('/login', {templateUrl: 'partials/login.html', controller: FinanceCtrlLogin});
        $routeProvider.when('/accounts', {templateUrl: 'partials/accounts.html', controller: FinanceCtrlAccounts});
        $routeProvider.otherwise({redirectTo: '/login'});
    }]);
