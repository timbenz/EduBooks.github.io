angular.module('pictureQuiz')
.directive('pictureQuestionShortAnswer', function() {
  return {
    restrict: 'E',
    templateUrl: 'html/directives/pictureQuestionShortAnswer.html',
    scope: {
      title: '@',
      autoSubmit: '=',
      numQuestions: '@',
      currentQuestion: '@',
      questionId: '=',
      question: '@',
      pictureQuestion: '@',
      correctAnswerArray: '=',
      userCorrect: '=',
      userAnswered: '=',
      userAnsweredCorrectly: '=',
      getNextQuestion: '&'
    },
    controller: function($scope) {
      $scope.userAnswered = false;
      $scope.userAnsweredCorrectly = false;
      $scope.processUserInput = function(selection, whereFrom) {
        if (!$scope.userAnswered) { // if haven't already answered question
          $scope.userAnswered = true;
          if (selection) {
            selection = selection.toLowerCase();
            for (var i = 0; i < $scope.correctAnswerArray.length; i++) {
              var correctAns = '';
              if ($scope.correctAnswerArray[i]) {
                correctAns = $scope.correctAnswerArray[i].toLowerCase();
                if (selection === correctAns) {
                  $scope.userCorrect[$scope.questionId] = true;
                  $scope.userAnsweredCorrectly = true;
                  return;
                }
              }
            }
          }

          $scope.userCorrect[$scope.questionId] = false;
          $scope.userAnsweredCorrectly = false;
        }
      }
    }
  }
});
