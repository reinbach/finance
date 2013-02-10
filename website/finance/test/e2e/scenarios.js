'use strict';

/* http://docs.angularjs.org/guide/dev_guide.e2e-testing */

describe('Finance App', function() {

    var login = function() {
        browser().navigateTo('#/login');
        input('user.username').enter('admin');
        input('user.password').enter('secret');
        element('[ng-view] button').click();
    }

    beforeEach(function() {
        browser().navigateTo('../../index.html');
    });


    it('should automatically redirect to /login when location hash/fragment is empty', function() {
        expect(browser().location().url()).toBe("/login");
    });


    describe('login', function() {

        beforeEach(function() {
            browser().navigateTo('#/login');
        });

        it('should render login when user navigates to /login', function() {
            expect(element('[ng-view] legend').text()).
                toMatch(/Please Sign In/);
            expect(element('[ng-view] button').attr('disabled')).
                toBe('disabled');
        });

        it('should focus on the username input field initially', function() {
            expect(element('[ng-view] input:text').attr('focus')).
                toBe("");
            expect(element('[ng-view] input:password').attr('focus')).
                toBe(undefined);
        });

        it('should enable submit button once username and password fields have values', function() {
            input('user.username').enter('admin');
            expect(element('[ng-view] button').attr('disabled')).
                toBe('disabled');
            input('user.password').enter('secret');
            expect(element('[ng-view] button').attr('disabled')).
                toBe(undefined);
            input('user.username').enter('');
            expect(element('[ng-view] button').attr('disabled')).
                toBe('disabled');
        });

        it('should redirect to accounts view on successful login', function() {
            login();
            expect(browser().location().url()).toBe('/accounts');
        });

    });

    describe('accounts', function() {

        beforeEach(function() {
            login();
            browser().navigateTo('#/accounts');
        });

        it('should be at accounts view', function() {
            expect(browser().location().url()).
                toBe('/accounts');
        });

        it('should render accounts when user navigates to /accounts', function() {
            expect(element('[ng-view] h1').text()).
                toBe('Accounts');
        });

    });

    describe('accounts add', function() {
        beforeEach(function() {
            login();
            browser().navigateTo('#/accounts');
            browser().navigateTo('#/accounts/add');
        });

        it('should be at the accounts add view', function() {
            expect(browser().location().url()).
                toBe('/accounts/add');
            expect(element('[ng-view] h1').text()).
                toBe('Add Account');
        });
    });

    describe('account_types', function() {

        beforeEach(function() {
            login();
            browser().navigateTo('#/accounts');
            browser().navigateTo('#/account/types');
        });

        it('should be at account types view', function() {
            expect(browser().location().url()).
                toBe('/account/types');
        });

        it('should render account types when user navigates to /account/types', function() {
            expect(element('[ng-view] h1').text()).
                toBe('Account Types');
        });

        // it('should open/close account type add modal when relevant button clicked', function() {
        //     expect(element('[ng-view] name="accountTypeForm"').css('display')).toEqual('none');
        //     element('[ng-view] button:first').click();
        //     expect(element('[ng-view] name="accountTypeForm"').css('display')).toEqual('block');
        //     element('[ng-view] div.modal-header button').click();
        //     expect(element('[ng-view] name="accountTypeForm"').css('display')).toEqual('none');
        // });

        it('should enable submit button once name field is valid', function() {
            element('[ng-view] button:first').click();
            input('account_type.name').enter('Expenses');
            expect(element('[ng-view] button.btn-primary').attr('disabled')).
                toBe(undefined);
            input('account_type.name').enter('Long Term Liabilities');
            expect(element('[ng-view] button.btn-primary').attr('disabled')).
                toBe('disabled');
        });

        it('should add/delete account type when valid name provided', function() {
            element('[ng-view] button:first').click();
            input('account_type.name').enter('Test Account Type');
            element('[ng-view] button.btn-primary').click();
            expect(element('[ng-view] table tbody tr:last').text()).toContain('Test Account Type');
        });

        // it('should not have previously deleted account type', function() {
        //     element('[ng-view] table tbody tr:last td button').click();
        //     expect(element('[ng-view] table tbody tr').text()).toContain('Test Account Type');
        // });

    });

});
