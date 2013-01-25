'use strict';

/* Controllers */


function FinanceCtrlLogin($scope, $http) {
    $scope.response = "";
    $scope.login = function() {
        $scope.response = "";
        $http.post('http://localhost:5000/login', $scope.user).
            success(function(data){
                // redirect to accounts page
            }).
            error(function(data){
                $scope.response = data.message;
                //test
                console.log($scope.response);
            });
    }
}
//FinanceCtrlLogin.$inject = ['$scope', '$http'];


function FinanceCtrlAccounts() {
}
FinanceCtrlAccounts.$inject = [];
