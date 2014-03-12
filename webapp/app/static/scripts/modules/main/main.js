'use strict';

angular.module('app.module.main', [
        'app.module.auth'
    ])

    .config(['$routeProvider', function($routeProvider) {
        $routeProvider.when('/', {
            templateUrl: '/webapp/static/scripts/modules/main/main.tpl.html'
        });
    }])

    .controller('MainCtrl', [
        '$scope',
        '$rootScope',
        function($scope, $rootScope) {
            var userWatcher = $rootScope.$watch('user', function() {
                if ($rootScope.user.loggedIn) {
                    $scope.template = { name: 'Dashboard', url: '/webapp/static/scripts/modules/dashboard/dashboard.tpl.html'};
                } else {
                    $scope.template = { name: 'Login', url: '/webapp/static/scripts/modules/auth/login.html'};
                }
            });

            $scope.$on('$destroy', function() {
                // remove watcher
                userWatcher();
            });
        }
    ]);

