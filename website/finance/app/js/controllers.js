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
    $scope.action = 'Add'
    $scope.account_types = AccountType.query();
    $scope.save = function() {
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


function FinanceCtrlAccountsEdit($scope, $location, $routeParams, Account, AccountType) {
    $scope.action = 'Edit'
    $scope.account_types = AccountType.query();
    var newAccount = new Account();
    newAccount.$get(
        {accountId: $routeParams.accountId},
        function(data) {
            $scope.account = data;
        }
    )
    $scope.save = function() {
        $scope.account.$update(
            {accountId: $routeParams.accountId},
            function() {
                $location.path("/accounts");
            },
            function(e) {
                console.log(e);
            }
        );
    };
}
FinanceCtrlAccountsEdit.$inject = ['$scope', '$routeParams', 'Account', 'AccountType'];


function FinanceCtrlAccountsView($scope, $routeParams, $http, Account, api_url) {
    $scope.transactions = [];
    var account = new Account();
    account.$get(
        {accountId: $routeParams.accountId},
        function(data) {
            $scope.account = data;
            $http.get(api_url.replace('\\', '') + '/accounts/transactions/' + account.account_id).
                success(function(data){
                    $scope.transactions = data;
                });
        }
    );
}
FinanceCtrlAccountsView.$inject = ['$scope', '$routeParams', '$http', 'Account', 'api_url'];


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


function FinanceCtrlTransactionsAdd($scope, $location, Transaction, Account) {
    $scope.action = 'Add'
    $scope.accounts = Account.query();
    $scope.save = function() {
        var newTransaction = new Transaction($scope.transaction);
        newTransaction.$save(
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
FinanceCtrlTransactionsAdd.$inject = ['$scope', '$location', 'Transaction', 'Account'];
