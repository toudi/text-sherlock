var sherlock = angular.module('sherlock', []).
	config(['$routeProvider', function($routeProvider) {
		$routeProvider.
			when('/', {
				templateUrl: '/static/partials/mainpage.html',
				controller: MainPageController
			}).
			when('/:project/:file/:lineno', {
				templateUrl: '/static/partials/file.html',
				controller: DisplayFileController
			}).
			when('/:project', {
				templateUrl: '/static/partials/project.html',
				controller: ProjectController
			}).
			otherwise({redirectTo: '/'})
	}]);

sherlock.factory('clipboard', function(){
	return {'howdy': 'doodles'};
});