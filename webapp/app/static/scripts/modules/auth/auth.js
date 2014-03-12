'use strict';

angular.module('app.module.auth', [])
    .controller('AuthCtrl', [
        '$scope',
        '$rootScope',
        '$location',
        'AuthService',
        function($scope, $rootScope, $location, AuthService) {

            // base authentication controller, provides a whoami function to
            // fetch the user data, also it provides a logout function which logs the
            // user out and cleans all session relevant variables

            $rootScope.user = {};
            $rootScope.user.loggedIn = false;

            $rootScope.whoami = function() {
                AuthService.whoami().then(
                    function(success) {
                        var userData = success.data;
                        if (userData) {
                            // set the user object on the rootScope so that the user is
                            // easy accessible globally within the app
                            $rootScope.user = userData;
                            $rootScope.user.loggedIn = true;
                        }
                    },
                    function() {
                        $rootScope.user = {};
                        $rootScope.user.loggedIn = false;
                    }
                );
            };
        }
    ]);

