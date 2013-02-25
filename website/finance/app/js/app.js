'use strict';


// Declare app level module which depends on filters, and services
angular.module('financeApp', ['ui', 'financeApp.filters', 'financeApp.services', 'financeApp.directives']).
    constant('api_url', 'http://localhost\\:5000').
    config(['$routeProvider', function($routeProvider) {
        $routeProvider.when(
            '/login',
            {templateUrl: 'partials/login.html', controller: FinanceCtrlLogin, secure: true}
        );
        $routeProvider.when(
            '/accounts',
            {templateUrl: 'partials/accounts.html', controller: FinanceCtrlAccounts}
        );
        $routeProvider.when(
            '/accounts/add',
            {templateUrl: 'partials/accounts_add.html', controller: FinanceCtrlAccountsAdd}
        );
        $routeProvider.when(
            '/accounts/edit/:accountId',
            {templateUrl: 'partials/accounts_add.html', controller: FinanceCtrlAccountsEdit}
        );
        $routeProvider.when(
            '/accounts/view/:accountId',
            {templateUrl: 'partials/accounts_view.html', controller: FinanceCtrlAccountsView}
        );
        $routeProvider.when(
            '/account/types',
            {templateUrl: 'partials/account_types.html', controller: FinanceCtrlAccountTypes}
        );
        $routeProvider.when(
            '/transactions/add',
            {templateUrl: 'partials/transactions_add.html', controller: FinanceCtrlTransactionsAdd}
        );
        $routeProvider.when(
            '/transactions/edit/:transactionId',
            {templateUrl: 'partials/transactions_add.html', controller: FinanceCtrlTransactionsEdit}
        );
        $routeProvider.otherwise({redirectTo: '/login'});
    }]).
    config(function($httpProvider) {
        var interceptor = ['$location', '$q', function(location, q) {
            function success(response) {
                return response;
            };

            function error(response) {
                if (response.status == 401) {
                    var deferred = q.defer();
                    location.path("/login");
                    return deferred.promise;
                };
                return q.reject(response);
            };

            return function(promise) {
                return promise.then(success, error);
            };
        }];

        $httpProvider.responseInterceptors.push(interceptor);
    });
