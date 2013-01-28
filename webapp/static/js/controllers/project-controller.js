function ProjectController($scope, clipboard, $routeParams) {
	getProjects($scope, clipboard);
	$scope.project = $routeParams.project;

	if ($routeParams.q) {
		$.getJSON('/search', {
				q: $routeParams.q,
				project: $scope.project,
				type: 'json'
			}, function(out) {
				results = {};
				for (i in out.results) {
					result = out.results[i];
					if (typeof(results[result.file]) == 'undefined') {
						results[result.file] = [];
					}
					results[result.file].push(result.match);

						//.replace($routeParams.q, '<b>' + $routeParams.q + '</b>'));
				}

				$scope.$apply(function(){
					$scope.results = results;
				});
		});
	}
}