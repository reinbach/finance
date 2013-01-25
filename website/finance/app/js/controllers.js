'use strict';

/* Controllers */


function FinanceCtrlLogin(scope, http, location, api_url) {
    scope.response = "";
    scope.login = function() {
        scope.response = "";
        http.post(api_url + '/login', scope.user).
            success(function(data){
                // redirect to accounts page
                location.path("/accounts");
            }).
            error(function(data){
                scope.response = data.message;
            });
    }
}
FinanceCtrlLogin.$inject = ['$scope', '$http', '$location', 'api_url'];


function FinanceCtrlAccounts() {
}
FinanceCtrlAccounts.$inject = [];
