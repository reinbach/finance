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

describe('FinanceCtrlAccountTypes', function(){
    var financeCtrlAccountTypes, scope;
    var AccountTypeService;

    beforeEach(inject(function($rootScope) {
        AccountTypeService = {query: jasmine.createSpy()};
        scope = $rootScope.$new();

        financeCtrlAccountTypes = new FinanceCtrlAccountTypes(scope, AccountTypeService);
    }));


    it('should ....', function() {
        //spec body
    });
});
