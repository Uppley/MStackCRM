'use strict';

/* Controllers */

function IndexController($scope) {
    console.log("You are the best programmer in the world!");
}

function AboutController($scope) {
    console.log("You are the best programmer in the world!");
}



//

// ------------------------------------------------------
// ----------------- Authentication ---------------------
// ------------------------------------------------------

function RegisterController($scope) {
    $scope.message = "This is a random register message. Do register here";
}

function LoginController($scope, $location, $window, $rootScope, Generic) {
    //
    $scope.message = "This is a random login message. Do login here";
    console.log($scope.message);


    $scope.showChangeFields = function() {
        console.log($scope.email);
        console.log($scope.password);
    }

    $scope.beginLogin = function() {
        if (Boolean($scope.email) && Boolean($scope.password)) {
            Generic.loginUser($scope.email, $scope.password).then(function(results) {
                console.log(results);
                if (results['data']['success'] === true) {
                    // This means the login was successful
                    // Fill the object here
                    $window.localStorage['loggedInUser'] = results['data']['user']['email'];
                    // Redirect the user to the initial page stored in root
                    $location.path("/");
                } else {
                    // This means the login was successful
                }
            });
        }
    }
}









// ------------------------------------------------------
// ----------------- All of The List --------------------
// ------------------------------------------------------

/**
	NOTE Needed List-Types:
	Project
	Client
	Users
	Servers
	Plugins -- NOTE: Will be the last of the list
*/

function PostListController($scope, Post) {
    var postsQuery = Post.get({}, function(posts) {
        $scope.posts = posts.objects;
    });
}

function ProjectListController($scope, $uibModal, $log, Project) {
    Project.getProjects()
        .then(function(projects) {
            $scope.products = projects.data.objects;
        });
    $scope.open = function(row) {
        $scope.previousProduct = row;
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'myModalContent.html',
            controller: ProductModalController,
            size: 'lg',
            resolve: {
                product: function() {
                    return row;
                }
            }
        });

        modalInstance.result.then(function(product) {
            $scope.changedProduct = product;
            console.log($scope.changedProduct);
        }, function() {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.openProduct = function() {
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'newProductType.html',
            controller: ProductTypeModal,
            size: 'lg',
            resolve: {

            }
        });

        modalInstance.result.then(function(product) {
            $scope.changedProduct = product;

            console.log($scope.changedProduct);

        }, function() {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };


}


function GenericListController($scope, Client) {
    Client.getClients()
        .then(function(clients) {
            console.log(clients.data.objects);
            $scope.clients = clients.data.objects;
        });
}

function ClientListController($scope, $uibModal, $log, Client) {
    Client.getClients()
        .then(function(clients) {
            console.log(clients.data.objects);
            $scope.clients = clients.data.objects;
            // Get the number of projects the client has
            for (var i = 0; i < $scope.clients.length; i++) {
                $scope.clients[i].num_of_projects = $scope.clients[i].projects.length;
            }
        });

    $scope.open = function(row) {

        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'myModalContent.html',
            controller: ClientModalController,
            size: 'lg',
            resolve: {
                client: function() {
                    return row;
                }
            }
        });

        modalInstance.result.then(function(client) {
            $scope.chanedClient = client['client'];
            // Maybe? Check to see if data changed 
            // Save the data into the database if there was a change. Check  the row for something different
            console.log($scope.chanedClient);
            if (client['runTrain'] === true) {
                // activate post request with client data (id)
                Client.trainFace($scope.chanedClient).then(function (result) {
                    console.log(result);
                })
            }
        }, function() {
            $log.info('Modal dismissed at: ' + new Date());
            // Send that data to the database and modify it
        });
    };
}

function ClientServersListController($scope, Server, toastr) {

    Server.getServers()
        .then(function(servers) {
            console.log(servers.data.objects);
            $scope.servers = servers.data.objects;
        });

    $scope.showAddField = false;

    $scope.changeField = function() {
        $scope.showAddField = !$scope.showAddField;
    }

    $scope.addServer = function() {
            // Get models for server installation
            if (Boolean($scope.addName) == false || Boolean($scope.addCompanyName) == false) {
                toastr.error('Your credentials are not good.\n Please enter them in', 'Error');
                return;
            }
            var req_obj = {
                    'name': $scope.addName,
                    'company': $scope.addCompanyName
                }
                // Send add request
            Server.createServer(req_obj)
                .then(function(response) {
                    console.log(response);
                    $scope.showAddField = false;
                });

        }
        // $scope.addServer();
    $scope.removeServer = function(id) {
        // Create pop-up menu
        // Remove server from list

        _.remove($scope.servers, function(server) {
            return server.id === id;
        });
    }
}


// ------------------------------------------------------
// ----------------- Detail Controllers -----------------
// ------------------------------------------------------

function PostDetailController($scope, $routeParams, Post) {
    var postQuery = Post.get({
        postId: $routeParams.postId
    }, function(post) {
        $scope.post = post;
    });
}



// ------------------------------------------------------
// ---------------------- Modals ------------------------
// ------------------------------------------------------
var ProductModalController = function($scope, $uibModalInstance, product) {


    $scope.product = product || {};
    if ($scope.product.type == "") {
        $scope.product.type = "Project Type 1";

    }
    $scope.ok = function() {
        $uibModalInstance.close($scope.product);
    };

    $scope.cancel = function() {
        $uibModalInstance.dismiss('cancel');
    };

}

var ProductTypeModal = function($scope, $uibModalInstance) {


    $scope.productType = {};
    $scope.ok = function() {
        $uibModalInstance.close($scope.productType);
    };

    $scope.cancel = function() {
        $uibModalInstance.dismiss('cancel');
    };

}

var ClientModalController = function($scope, $uibModalInstance, client) {

    // Modal Controller Logic Goes Here
    $scope.client = client || {};

    // Tell if you should activate the function necessary

    $scope.trainFace = function() {
        if ($scope.client == {}) {
            $uibModalInstance.dismiss('cancel');
        } else {
            $uibModalInstance.close({
                "client": $scope.client,
                "runTrain": true
            });
        }

    }

    $scope.ok = function() {
        $uibModalInstance.close({
            "client": $scope.client,
            "runTrain": false
        });
    };

    $scope.cancel = function() {
        $uibModalInstance.dismiss('cancel');
    };

}
