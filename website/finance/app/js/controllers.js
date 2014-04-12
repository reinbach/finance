'use strict';

/* controllers */

var financeControllers = angular.module('financeControllers', []);

financeControllers.controller(
    'financeControllers',
    ['$scope', '$rootScope', 'tokenHandler', '$http', 'api_url',
     function($scope, $rootScope, tokenHandler, $http, api_url) {
         $rootScope.$on('$routeChangeSuccess', function(event, routeData) {
             if (routeData.$route) {
                 //test
                 console.log(routeData.$route.secure);
                 $scope.secure = routeData.$route.secure;
             }
         });

         $scope.logout = function() {
             tokenHandler.set("none");
             $http.get(api_url.replace('\\', '') + '/logout');
         }
     }
    ]);


financeControllers.controller(
    'FinanceLoginCtrl',
    ['$scope', '$http', '$location', 'tokenHandler', 'api_url',
     function($scope, $http, $location, tokenHandler, api_url) {
         $scope.response = "";
         $scope.login = function() {
             $scope.response = "";
             $http.post(api_url.replace('\\', '') + '/login', $scope.user).
                 success(function(data){
                     // set token
                     tokenHandler.set(data.auth_token);
                     // redirect to accounts page
                     $location.path("/accounts");
                 }).
                 error(function(data){
                     $scope.response = data.message;
                 });
         }
     }
    ]);


financeControllers.controller(
    'FinanceAccountsCtrl',
    ['$scope', 'Account',
     function($scope, Account) {
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
    ]);


financeControllers.controller(
    'FinanceAccountsAddCtrl',
    ['$scope', '$location', 'Account', 'AccountType',
     function($scope, $location, Account, AccountType) {
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
    ]);


financeControllers.controller(
    'FinanceAccountsEditCtrl',
    ['$scope', '$location', '$routeParams', 'Account','AccountType',
     function($scope, $location, $routeParams, Account, AccountType) {
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
    ]);


financeControllers.controller(
    'FinanceAccountsViewCtrl',
    ['$scope', '$routeParams', '$http', 'Account','api_url',
     function($scope, $routeParams, $http, Account, api_url) {
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
    ]);


financeControllers.controller(
    'FinanceAccountTypesCtrl',
    ['$scope', 'AccountType',
     function($scope, AccountType) {
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
    ]);


financeControllers.controller(
    'FinanceTransactionsAddCtrl',
    ['$scope', '$location', 'Transaction', 'Account',
     function($scope, $location, Transaction, Account) {
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
    ]);


financeControllers.controller(
    'FinanceTransactionsEditCtrl',
    ['$scope', '$location', '$routeParams', 'Transaction', 'Account',
     function($scope, $location, $routeParams, Transaction, Account) {
         $scope.action = 'Edit'
         $scope.accounts = Account.query();
         var newTransaction = new Transaction();
         newTransaction.$get(
             {transactionId: $routeParams.transactionId},
             function(data) {
                 $scope.transaction = data;
                 $scope.transaction.debit = data.account_debit_id;
                 $scope.transaction.credit = data.account_credit_id;
             }
         );
         $scope.save = function() {
             $scope.transaction.$update(
                 {transactionId: $routeParams.transactionId},
                 function() {
                     $location.path("/accounts");
                 },
                 function(e) {
                     console.log(e);
                 }
             );
         };
     }
    ]);

financeControllers.controller(
    'FinanceTransactionsUploadCtrl',
    ['$scope', '$location', 'Transaction', 'Account',
     function($scope, $location, Transaction, Account) {
         $scope.action = 'Upload'
         $scope.accounts = Account.query();
         $scope.upload = function() {
             console.log("upload that file")
         };
     }
    ]);
