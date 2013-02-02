'use strict';

/* Directives */


angular.module('financeApp.directives', []).
    directive('appVersion', ['version', function(version) {
        return function(scope, elm, attrs) {
            elm.text(version);
        };
    }]).
    directive('focus', function() {
        return function(scope, element) {
            element[0].focus();
        };
    }).
    directive('dropdownToggle', ['$document', '$location', '$window', function ($document, $location, $window) {
        var openElement = null, close;
        return {
            restrict: 'CA',
            link: function(scope, element, attrs) {
                scope.$watch(
                    function dropdownTogglePathWatch() { return $location.path(); },
                    function dropdownTogglePathWatchAction() {
                        if (close) { close(); }
                    }
                );

                element.parent().bind('click', function(event) {
                    if (close) { close(); }
                });

                element.bind('click', function(event) {
                    event.preventDefault();
                    event.stopPropagation();

                    var iWasOpen = false;

                    if (openElement) {
                        iWasOpen = openElement === element;
                        close();
                    }

                    if (!iWasOpen){
                        element.parent().addClass('open');
                        openElement = element;

                        close = function (event) {
                            if (event) {
                                event.preventDefault();
                                event.stopPropagation();
                            }
                            $document.unbind('click', close);
                            element.parent().removeClass('open');
                            close = null;
                            openElement = null;
                        };

                        $document.bind('click', close);
                    }
                });
            }
        };
    }]);
