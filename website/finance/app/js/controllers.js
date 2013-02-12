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


function FinanceCtrlAccounts($scope, Account) {
    $scope.accounts = Account.query();

    $scope.remove = function(account_id) {
        var account = new Account();
        account.$remove(
            {accountId: account_id},
            function() {
                $scope.accounts = Account.query();
            }
        );
    };
}
FinanceCtrlAccounts.$inject = ['$scope', 'Account'];


function FinanceCtrlAccountsAdd($scope, $location, Account, AccountType) {
    $scope.account_types = AccountType.query();
    $scope.add = function() {
        var newAccount = new Account($scope.account);
        newAccount.$save(
            {},
            function() {
                $location.path("/accounts");
            },
            function(e) {
                console.log(e);
            }
        );
    };
}
FinanceCtrlAccountsAdd.$inject = ['$scope', '$location', 'Account', 'AccountType'];

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
        newAccountType.$save(
            {},
            function() {
                $scope.account_types = AccountType.query();
                $scope.closeAccountTypeAddModal();
            }
        );
    };

    $scope.remove = function(account_type_id) {
        var accountType = new AccountType();
        accountType.$remove(
            {accountTypeId: account_type_id},
            function() {
                $scope.account_types = AccountType.query();
            }
        );
    };
}
FinanceCtrlAccountTypes.$inject = ['$scope', 'AccountType'];
