'use strict';

/* jasmine specs for controllers go here */

describe('FinanceCtrlLogin controllers', function(){
    var ctrl, scope, $httpBackend, tokenHandler;
    var api_url = "";

    beforeEach(inject(function(_$httpBackend_, $rootScope, $controller) {
        tokenHandler = {set: jasmine.createSpy()};

        $httpBackend = _$httpBackend_;
        $httpBackend.whenPOST('/login', {username:'admin', password:'wrong'}).
            respond(400, {'message': 'Invalid username/password.'});
        $httpBackend.whenPOST('/login', {username:'admin', password:'correct'}).
            respond(200, {'message': 'Invalid username/password.'});
        scope = $rootScope.$new();
        ctrl = $controller(FinanceCtrlLogin, {$scope: scope, tokenHandler: tokenHandler, api_url: api_url});
    }));


    it('should create empty response', function() {
        expect(scope.response).toBe("");
        expect(scope.response.length).toBe(0);
    });

    it('should update response for failed login', function() {
        scope.user = {username: 'admin', password: 'wrong'}
        scope.login();
        $httpBackend.flush();
        expect(scope.response).toBe("Invalid username/password.");
    });

    it('should redirect to accounts page on successful login', function() {
        scope.user = {username: 'admin', password: 'correct'}
        scope.login();
        $httpBackend.flush();
        expect(scope.response).toBe("");
    });
});


describe('FinanceCtrlAccounts', function(){
    var financeCtrlAccounts, $scope, AccountStub;

    beforeEach(inject(function($rootScope) {
        AccountStub = function AccountServiceStub() {
            this.$remove = jasmine.createSpy();
        }
        AccountStub.query = jasmine.createSpy();

        $scope = $rootScope.$new();
        financeCtrlAccounts = new FinanceCtrlAccounts($scope, AccountStub);
    }));

    it('should call query on account service init', function() {
        expect(AccountStub.query).toHaveBeenCalled();
    });

    // it('should call remove on account service when remove function called', function() {
    //     expect(AccountStub.query.calls.length).toBe(1);
    //     $scope.remove('1');
    // });
});


describe('FinanceCtrlAccountsAdd', function(){
    var financeCtrlAccountsAdd, $scope, AccountStub, AccountTypeStub;

    beforeEach(inject(function($rootScope) {
        AccountStub = function AccountServiceStub() {
            this.$save = jasmine.createSpy();
        }
        AccountStub.save = jasmine.createSpy();

        AccountTypeStub = function AccountTypeServiceStub() {
            this.stub = true;
        }
        AccountTypeStub.query = jasmine.createSpy();

        $scope = $rootScope.$new();
        financeCtrlAccountsAdd = new FinanceCtrlAccountsAdd($scope, {}, AccountStub, AccountTypeStub);
    }));

    it('should set action to "Add"', function() {
        expect($scope.action).toBe('Add');
    });

    it('should call query on account service init', function() {
        expect(AccountTypeStub.query).toHaveBeenCalled();
    });
});


describe('FinanceCtrlAccountsEdit', function(){
    var financeCtrlAccountsEdit, $scope, AccountStub, AccountTypeStub;

    beforeEach(inject(function($rootScope) {
        AccountStub = function AccountServiceStub() {
            this.$get = jasmine.createSpy();
        }
        AccountStub.save = jasmine.createSpy();

        AccountTypeStub = function AccountTypeServiceStub() {
            this.stub = true;
        }
        AccountTypeStub.query = jasmine.createSpy();

        $scope = $rootScope.$new();
        financeCtrlAccountsEdit = new FinanceCtrlAccountsEdit($scope, {}, {}, AccountStub, AccountTypeStub);
    }));

    it('should set action to "Edit"', function() {
        expect($scope.action).toBe('Edit');
    });

    it('should call query on account service init', function() {
        expect(AccountTypeStub.query).toHaveBeenCalled();
    });
});


describe('FinanceCtrlAccountTypes', function(){
    var financeCtrlAccountTypes, $scope, AccountTypeStub;

    beforeEach(inject(function($rootScope) {
        AccountTypeStub = function AccountTypeServiceStub() {
            this.$save = jasmine.createSpy();
            this.$remove = jasmine.createSpy();
        }
        AccountTypeStub.query = jasmine.createSpy();

        $scope = $rootScope.$new();
        financeCtrlAccountTypes = new FinanceCtrlAccountTypes($scope, AccountTypeStub);
    }));


    it('should get a list of account types on init', function() {
        expect(AccountTypeStub.query).toHaveBeenCalled();
    });
});
