'use strict';

/* Controllers */

function financeCtrl($scope, $rootScope, $http, tokenHandler, api_url) {
    $rootScope.$on('$routeChangeSuccess', function(event, routeData) {
        if (routeData.$route) {
            $scope.secure = routeData.$route.secure;
        }
    });

    $scope.logout = function() {
        tokenHandler.set("none");
        $http.get(api_url.replace('\\', '') + '/logout');
    }
}
financeCtrl.$inject = ['$scope', '$rootScope', '$http', 'tokenHandler', 'api_url'];

function FinanceCtrlLogin(scope, http, location, tokenHandler, api_url) {
    scope.response = "";
    scope.login = function() {
        scope.response = "";
        http.post(api_url.replace('\\', '') + '/login', scope.user).
            success(function(data){
                // set token
                tokenHandler.set(data.auth_token);
                // redirect to accounts page
                location.path("/accounts");
            }).
            error(function(data){
                scope.response = data.message;
            });
    }
}
FinanceCtrlLogin.$inject = ['$scope', '$http', '$location', 'tokenHandler', 'api_url'];


function FinanceCtrlAccounts(scope, AccountService) {
    scope.accounts = AccountService.query();
}
FinanceCtrlAccounts.$inject = ['$scope', 'Account'];


function FinanceCtrlAccountsAdd(scope, AccountService) {
    scope.account_types = [];
    scope.add = function() {
        newAccount = new AccountService({
        });
        newAccount.$save();
    }
}
FinanceCtrlAccountsAdd.$inject = ['$scope', 'Account'];

function FinanceCtrlAccountTypes($scope, AccountType) {
    $scope.account_types = AccountType.query();

    $scope.openAccountTypeAddModal = function() {
        $scope.accountTypeAdd = true;
    };

    $scope.closeAccountTypeAddModal = function() {
        $scope.accountTypeAdd = false;
    };

    $scope.add = function() {
        var newAccountType = new AccountType();
        newAccountType.name = $scope.account_type.name;
        newAccountType.$save();
    };
}
FinanceCtrlAccountTypes.$inject = ['$scope', 'AccountType'];
