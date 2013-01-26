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

    });


    describe('accounts', function() {

        beforeEach(function() {
            browser().navigateTo('#/accounts');
        });


        it('should render accounts when user navigates to /accounts', function() {
            expect(element('[ng-view] p:first').text()).
                toMatch(/List of accounts goes here.../);
        });

    });
});
