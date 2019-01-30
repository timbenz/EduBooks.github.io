angular.module('pictureQuiz', ['ui.router', 'ngAnimate'])
.constant('dataUrl', {'url': 'data/'})
.config(function ($stateProvider, $urlRouterProvider) {
  // routing configuration code
  $urlRouterProvider
    .otherwise('/');

  $stateProvider
    .state('Home', {
      templateUrl: 'html/routes/homeTmpl.html',
      url: '/',
      controller: 'homeCtrl'
    })
    .state('Quiz', {
      templateUrl: 'html/routes/quizTmpl.html',
      url: '/quiz/:quizBriefName',
      controller: 'quizCtrl',
    })
    .state('Results', {
      templateUrl: 'html/routes/resultsTmpl.html',
      url: '/results',
      params : {
        title: '',
        secondsElapsed: 0,
        userCorrectArray: [],
        percentGreatJob: 0
      },
      controller: 'resultsCtrl'
    });
});
