'use strict';

angular.module('AngularFlask', ['angularFlaskServices', 'ngResource', 'ngRoute', 'ngAnimate', 'ui.bootstrap', 'toastr'])
    .config(['$routeProvider', '$locationProvider',
        function($routeProvider, $locationProvider) {
            $routeProvider
            // ------------------------------------------------------
            // --------------------- Generics -----------------------
            // ------------------------------------------------------
                .when('/', {
                    templateUrl: 'static/partials/landing.html',
                    controller: IndexController
                })
                .when('/about', {
                    templateUrl: 'static/partials/about.html',
                    controller: AboutController
                })
                // ------------------------------------------------------
                // ------------------ Authentication --------------------
                // ------------------------------------------------------
                .when('/register', {
                    templateUrl: 'static/partials/register.html',
                    controller: RegisterController
                })
                .when('/login', {
                    templateUrl: 'static/partials/login.html',
                    controller: LoginController
                })
                // ------------------------------------------------------
                // ---------------------- List --------------------------
                // ------------------------------------------------------
                .when('/post', {
                    templateUrl: 'static/partials/post-list.html',
                    controller: PostListController
                })
                .when('/servers', {
                    templateUrl: 'static/partials/list-servers.html',
                    controller: ClientServersListController
                })
                .when('/clients', {
                    templateUrl: 'static/partials/list-clients.html',
                    controller: ClientListController
                })
                .when('/products', {
                    templateUrl: 'static/partials/list-product.html',
                    controller: ProjectListController
                })
                .when('/blog', {
                    templateUrl: 'static/partials/post-list.html',
                    controller: PostListController
                })
                // ------------------------------------------------------
                // ------------------- Details --------------------------
                // ------------------------------------------------------
                .when('/clients/:clientId', {
                    templateUrl: '/static/partials/post-detail.html',
                    controller: PostDetailController
                })
                .when('/post/:postId', {
                    templateUrl: '/static/partials/post-detail.html',
                    controller: PostDetailController
                })

            .otherwise({
                redirectTo: '/'
            });

            $locationProvider.html5Mode({
                enabled: true,
                requireBase: false
            });
        }
    ])
    .run(function($rootScope, $window, $location) {
        //
        $rootScope.$on("$routeChangeStart", function(event, next, current) {
            if (Boolean($window.localStorage['loggedInUser']) === false ) {
                // no logged user, redirect to /login
                if (next.templateUrl === "partials/login.html") {} else {
                    $location.path("/login");
                }
            }

        });
    });
