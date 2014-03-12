'use strict';

angular.module('app')
    .config(['RestangularProvider', function(RestangularProvider) {
        // default configuration for restangular plugin
        RestangularProvider.setBaseUrl('/api/');
    }]);
