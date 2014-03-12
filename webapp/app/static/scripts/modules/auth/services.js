'use strict';

angular.module('app.module.auth')
    .service('AuthService', ['Restangular', function(Restangular) {
        var service = Restangular.allUrl('');

        this.whoami = function() {
            return service.customGET('me');
        };

    }]);
