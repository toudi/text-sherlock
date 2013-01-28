function DisplayFileController($scope, $routeParams) {
	$scope.project = $routeParams.project;
	$scope.file = $routeParams.file;
	$scope.line = $routeParams.line;
}