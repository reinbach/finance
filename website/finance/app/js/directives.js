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
    directive('trxTransferAccountName', function() {
        return function($scope, element) {
            if ($scope.account.account_id == $scope.trx.debit.account_id) {
                element.text($scope.trx.credit.name);
            } else {
                element.text($scope.trx.debit.name);
            }
        };
    }).
    directive('trxDebitAmount', ['$filter', function($filter) {
        return function($scope, element) {
            if ($scope.account.account_id == $scope.trx.debit.account_id) {
                element.text($filter('currency')($scope.trx.amount));
            }
        };
    }]).
    directive('trxCreditAmount', ['$filter', function($filter) {
        return function($scope, element) {
            if ($scope.account.account_id == $scope.trx.credit.account_id) {
                element.text($filter('currency')($scope.trx.amount));
            }
        };
    }]).
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
    }]).
    directive('modal', ['$parse',function($parse) {
        var backdropEl;
        var body = angular.element(document.getElementsByTagName('body')[0]);
        var defaultOpts = {
            backdrop: true,
            escape: true
        };
        return {
            restrict: 'EA',
            link: function(scope, elm, attrs) {
                var opts = angular.extend(defaultOpts, scope.$eval(attrs.uiOptions || attrs.bsOptions || attrs.options));
                var shownExpr = attrs.modal || attrs.show;
                var setClosed;

                if (attrs.close) {
                    setClosed = function() {
                        scope.$apply(attrs.close);
                    };
                } else {
                    setClosed = function() {
                        scope.$apply(function() {
                            $parse(shownExpr).assign(scope, false);
                        });
                    };
                }
                elm.addClass('modal');

                if (opts.backdrop && !backdropEl) {
                    backdropEl = angular.element('<div class="modal-backdrop"></div>');
                    backdropEl.css('display','none');
                    body.append(backdropEl);
                }

                function setShown(shown) {
                    scope.$apply(function() {
                        model.assign(scope, shown);
                    });
                }

                function escapeClose(evt) {
                    if (evt.which === 27) { setClosed(); }
                }
                function clickClose() {
                    setClosed();
                }

                function close() {
                    if (opts.escape) { body.unbind('keyup', escapeClose); }
                    if (opts.backdrop) {
                        backdropEl.css('display', 'none').removeClass('in');
                        backdropEl.unbind('click', clickClose);
                    }
                    elm.css('display', 'none').removeClass('in');
                    body.removeClass('modal-open');
                }
                function open() {
                    if (opts.escape) { body.bind('keyup', escapeClose); }
                    if (opts.backdrop) {
                        backdropEl.css('display', 'block').addClass('in');
                        if(opts.backdrop != "static") {
                            backdropEl.bind('click', clickClose);
                        }
                    }
                    elm.css('display', 'block').addClass('in');
                    body.addClass('modal-open');
                }

                scope.$watch(shownExpr, function(isShown, oldShown) {
                    if (isShown) {
                        open();
                    } else {
                        close();
                    }
                });
            }
        };
    }]);
