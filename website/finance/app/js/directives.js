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
    directive('dropdownToggle', ['$document', '$location', '$window',
                                 function ($document, $location, $window) {
        var openElement = null, close;
        return {
            restrict: 'CA',
            link: function(scope, element, attrs) {
                scope.$watch(
                    function dropdownTogglePathWatch() {
                        return $location.path();
                    },
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
    directive('financeUpload', ['uuid', 'fileUploader',
                                function(uuid, fileUploader) {
        return {
            restrict: 'E',
            replace: true,
            scope: {
                chooseFileButtonText: '@',
                uploadFileButtonText: '@',
                uploadUrl: '@',
                maxFiles: '@',
                maxFileSizeMb: '@',
                autoUpload: '@',
                uploadFileName: '@',
                getAdditionalData: '&',
                onProgress: '&',
                onDone: '&',
                onError: '&'
            },
            template: '<div>' +
                '<input type="file" style="opacity:0" />' +
                '<label class="btn btn-success" ng-click="choose()">' +
                '  {{ chooseFileButtonText }}</label>' +
                '<div class="well file-names">{{ uploadFileName }}</div>' +
                '<a href="#/accounts" class="btn">Cancel</a> ' +
                '<button class="upload-button btn btn-primary" ' +
                '  ng-show="showUploadButton" ng-click="upload()">' +
                '    {{ uploadFileButtonText }}</button>' +
                '</div>',
            compile: function compile(tElement, tAttrs, transclude) {
                var fileInput = angular.element(tElement.children()[0]);
                var fileLabel = angular.element(tElement.children()[1]);

                if (!tAttrs.maxFiles) {
                    tAttrs.maxFiles = 1;
                    fileInput.removeAttr("multiple")
                } else {
                    fileInput.attr("multiple", "multiple");
                }

                if (!tAttrs.maxFileSizeMb) {
                    tAttrs.maxFileSizeMb = 50;
                }

                var fileId = uuid.new();
                fileInput.attr("id", fileId);
                fileLabel.attr("for", fileId);

                return function postLink(scope, el, attrs, ctl) {
                    scope.files = [];
                    scope.showUploadButton = false;

                    el.bind('change', function(e) {
                        if (!e.target.files.length) return;

                        scope.files = [];
                        var tooBig = [];
                        if (e.target.files.length > scope.maxFiles) {
                            raiseError(
                                e.target.files, 'TOO_MANY_FILES',
                                "Cannot upload " +
                                    e.target.files.length +
                                    " files, maxium allowed is " +
                                    scope.maxFiles
                            )
                            return;
                        }

                        for (var i = 0; i < scope.maxFiles; i++) {
                            if (i >= e.target.files.length) break;

                            var file = e.target.files[i];
                            scope.files.push(file);

                            if (file.size > scope.maxFileSizeMb * 1048576) {
                                tooBig.push(file);
                            }
                        }

                        if (tooBig.length > 0) {
                            raiseError(
                                tooBig, 'MAX_SIZE_EXCEEDED',
                                "Files are larger than the specified max (" +
                                    scope.maxFileSizeMb + "MB)");
                            return;
                        }

                        if (scope.autoUpload &&
                            scope.autoUpload.toLowerCase() == 'true') {
                            scope.upload();
                        } else {
                            scope.$apply(function() {
                                var filename = "";
                                for (i = 0; i < scope.files.length; i++) {
                                    if (i > 0) {
                                        filename = filename + ", ";
                                    }
                                    filename = filename + scope.files[i].name;
                                }
                                scope.uploadFileName = filename;
                                scope.showUploadButton = true;
                            })
                        }
                    });

                    scope.upload = function() {
                        console.log("are we attempting to upload?")
                        var data = null;
                        if (scope.getAdditionalData) {
                            data = scope.getAdditionalData();
                        }

                        if (angular.version.major <= 1 &&
                            angular.version.minor < 2 ) {
                            //older versions of angular's q-service
                            //don't have a notify callback
                            //pass the onProgress callback into the service
                            fileUploader
                                .post(scope.files, data, function(complete) {
                                    scope.onProgress({percentDone: complete});
                                })
                                .to(scope.uploadUrl)
                                .then(function(ret) {
                                    scope.onDone({files: ret.files,
                                                  data: ret.data});
                                }, function(error) {
                                    scope.onError({files: scope.files,
                                                   type: 'UPLOAD_ERROR',
                                                   msg: error});
                                })
                        } else {
                            fileUploader
                                .post(scope.files, data)
                                .to(scope.uploadUrl)
                                .then(function(ret) {
                                    scope.onDone({files: ret.files,
                                                  data: ret.data});
                                }, function(error) {
                                    scope.onError({files: scope.files,
                                                   type: 'UPLOAD_ERROR',
                                                   msg: error});
                                },  function(progress) {
                                    scope.onProgress({percentDone: progress});
                                });
                        }

                        resetFileInput();
                    };

                    function raiseError(files, type, msg) {
                        scope.onError({files: files, type: type, msg: msg});
                        resetFileInput();
                    }

                    function resetFileInput() {
                        var parent = fileInput.parent();

                        fileInput.remove();
                        var input = document.createElement("input");
                        var attr = document.createAttribute("type");
                        attr.nodeValue = "file";
                        input.setAttributeNode(attr);

                        var inputId = uuid.new();
                        attr = document.createAttribute("id");
                        attr.nodeValue = inputId;
                        input.setAttributeNode(attr);

                        attr = document.createAttribute("style");
                        attr.nodeValue = "opacity: 0;display:inline;width:0";
                        input.setAttributeNode(attr);

                        if (scope.maxFiles > 1) {
                            attr = document.createAttribute("multiple");
                            attr.nodeValue = "multiple";
                            input.setAttributeNode(attr);
                        }

                        fileLabel.after(input);
                        fileLabel.attr("for", inputId);

                        fileInput = angular.element(input);
                    }
                }
            }
        }
    }]).
    directive('modal', ['$parse', function($parse) {
        var backdropEl;
        var body = angular.element(document.getElementsByTagName('body')[0]);
        var defaultOpts = {
            backdrop: true,
            escape: true
        };
        return {
            restrict: 'EA',
            link: function(scope, elm, attrs) {
                var opts = angular.extend(defaultOpts, scope.$eval(
                    attrs.uiOptions || attrs.bsOptions || attrs.options));
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
                    backdropEl = angular.element(
                        '<div class="modal-backdrop"></div>');
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
