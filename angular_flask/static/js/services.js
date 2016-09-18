'use strict';

angular.module('angularFlaskServices', ['ngResource'])
    .factory('Post', function($resource) {
        return $resource('/api/post/:postId', {}, {
            query: {
                method: 'GET',
                params: {
                    postId: ''
                },
                isArray: true
            }
        });
    })
    .factory('Server', ['$http', function($http) {
        var urlBase = "/api/server";
        var addservapi = "/api/addserver";
        var dataFactory = {};

        dataFactory.getServers = function() {
            return $http.get(urlBase);
        }

        dataFactory.getServer = function(id) {
            return $http.get(urlBase + '/' + id);
        }

        dataFactory.createServer = function(custServ) {
            return $http.post(addservapi, custServ);
        }


        return dataFactory;
    }])
    .factory('Project', ['$http', function($http) {
        var urlBase = "/api/project";
        var addservapi = "/api/project";
        var dataFactory = {};

        dataFactory.getProjects = function() {
            return $http.get(urlBase);
        }

        dataFactory.getProject = function(id) {
            return $http.get(urlBase + '/' + id);
        }

        dataFactory.createProject = function(projectObj) {
            return $http.post(addservapi, projectObj);
        }


        return dataFactory;
    }])
    .factory('Generic', ['$http', function($http) {
        var urlBase = "/api/login";
        var addservapi = "/api/project";
        var dataFactory = {};

        dataFactory.loginUser = function(email, password) {
            return $http.post(urlBase, {'email': email, 'password': password});
        }


        return dataFactory;
    }])
    .factory('Client', ['$http', function($http) {
        var urlBase = "/api/client";
        var addservapi = "/api/client";
        var dataFactory = {};

        dataFactory.getClients = function() {
            return $http.get(urlBase);
        }

        dataFactory.getClient = function(id) {
            return $http.get(urlBase + '/' + id);
        }

        dataFactory.createClient = function(clientObj) {
            return $http.post(addservapi, clientObj);
        }

        dataFactory.trainFace = function (clientObj) {
            return $http.post(addservapi+'/train', clientObj);
        }
        return dataFactory;
    }]);

// Create a login factory
