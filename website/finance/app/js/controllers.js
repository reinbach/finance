'use strict';

/* Controllers */


function FinanceCtrlLogin($scope, $http, $location) {
    $scope.response = "";
    $scope.login = function() {
        $scope.response = "";
        $http.post('http://localhost:5000/login', $scope.user).
            success(function(data){
                // redirect to accounts page
                $location.path("/accounts");
            }).
            error(function(data){
                $scope.response = data.message;
            });
    }
}
//FinanceCtrlLogin.$inject = ['$scope', '$http'];


function FinanceCtrlAccounts() {
}
FinanceCtrlAccounts.$inject = [];
