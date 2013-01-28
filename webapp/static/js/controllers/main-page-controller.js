function updateProjectsList($scope, clipboard) {
	$scope.$apply(function(){
		$scope.projects = clipboard.projects;
	});
}

function getProjects($scope, clipboard) {
	if (typeof(clipboard.projects) == 'undefined') {
		$.getJSON('/projects', function(out) {
			clipboard.projects = out.projects;
			updateProjectsList($scope, clipboard);
		});
	}
	else {
		updateProjectsList($scope, clipboard);
	}
}

function MainPageController($scope, clipboard, $routeParams) {
	getProjects($scope, clipboard);
}