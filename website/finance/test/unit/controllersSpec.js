'use strict';

/* jasmine specs for controllers go here */

describe('FinanceCtrlLogin controllers', function(){
    var ctrl, scope, $httpBackend;
    var api_url = "";

    beforeEach(inject(function(_$httpBackend_, $rootScope, $controller) {
        $httpBackend = _$httpBackend_;
        $httpBackend.whenPOST('/login', {username:'admin', password:'wrong'}).
            respond(400, {'message': 'Invalid username/password.'});
        $httpBackend.whenPOST('/login', {username:'admin', password:'correct'}).
            respond(200, {'message': 'Invalid username/password.'});
        scope = $rootScope.$new();
        ctrl = $controller(FinanceCtrlLogin, {$scope: scope, api_url: api_url});
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
  var financeCtrlAccounts;


  beforeEach(function(){
    financeCtrlAccounts = new FinanceCtrlAccounts();
  });


  it('should ....', function() {
    //spec body
  });
});
