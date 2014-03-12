'use strict';

var app = angular.module('app', [
        'ngCookies',
        'ngRoute',
        'ngSanitize',
        'restangular',

        'app.module.main'
    ])

    .config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true).hashPrefix('!');
    }])

    .controller('AppCtrl', [
        '$scope',
        '$rootScope',
        '$controller',
        '$window',
        function($scope, $rootScope, $controller, $window) {

            // global controller which sets up all required parameters for the app
            $controller('AuthCtrl', { $scope: $scope });

            $scope.browserReload = function(newPath) {
                // browser reload function, makes a simple window location reload
                // but this is a better way to keep the code testable without mocking
                // the angular $window object
                // if newPath is set, also change the path and reload
                if (!!newPath && newPath != window.location.pathname) {
                    $window.location.pathname = newPath;
                } else {
                    $window.location.reload();
                }
            };

            $rootScope.whoami();
        }
    ]);
