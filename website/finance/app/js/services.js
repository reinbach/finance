'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('financeApp.services', []).
    value('version', '0.1').
    factory('notify', ['$window', function(win) {
        var msgs = [];
        return function(msg) {
            msgs.push(msg);
            if (msgs.length == 3) {
                win.alert(msgs.join("\n"));
                msgs = [];
            }
        };
    }]);

