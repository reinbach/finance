'use strict';

/* http://docs.angularjs.org/guide/dev_guide.e2e-testing */

describe('Finance App', function() {

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
            input('user.username').enter('admin');
            input('user.password').enter('secret');
            element('[ng-view] button').click();
            expect(browser().location().url()).toBe('/accounts');
        });

    });


    describe('accounts', function() {

        beforeEach(function() {
            browser().navigateTo('#/login');
            input('user.username').enter('admin');
            input('user.password').enter('secret');
            element('[ng-view] button').click();
            browser().navigateTo('#/accounts');
        });

        it('should be at accounts view', function() {
            expect(browser().location().url()).toBe('/accounts');
        });

        it('should render accounts when user navigates to /accounts', function() {
            expect(element('[ng-view] h1').text()).
                toBe('Accounts');
        });

    });
});
