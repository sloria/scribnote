'use strict';

var app = angular.module('appApp');

app.controller('BooksCtrl', function ($scope, Book, AppAlert, $hotkey) {

  $scope.books = [];
  Book.query().then(function(books) {
    $scope.books = books;
  }, function(error) {
    AppAlert.add('danger', 'Could not fetch books. Please try again later.');
  });

  $scope.addForm = {
    active: false,
    first: null,
    last: null,
    title: null,
    activate: function() {
      $scope.addForm.active = true;
    },
    deactivate: function() {
      $scope.addForm.active = false;
    },
    submit: function() {
      var bookPromise = Book.create({
        title: this.title,
        author_first: this.first,
        author_last: this.last
      });

      bookPromise.then(function(newBook) {
        $scope.books.push(newBook);
        $scope.addForm.active = false;
        AppAlert.add('success', 'Added book.');
      }, function(error) {
        console.error(error);
        AppAlert.add('danger', 'An error occurred while creating the book. Please try again later.');
      });
    }
  };

  $scope.delete = function(book, index) {
    Book.delete(book.id).then(function() {
      $scope.books.splice(index, 1);
      AppAlert.add('warning', 'Deleted book.');
    }, function(error) {
      console.error(error);
      AppAlert.add('danger', 'An error occurred on the server.');
    });
  };


  $hotkey.bind('ctrl + n', function() {
    $scope.addForm.activate();
  });

  $hotkey.bind('escape', function() {
    $scope.addForm.deactivate();
  });

});


app.controller('BookDetailCtrl',
    function($scope, $routeParams, Book, Note, AppAlert, $hotkey) {
  // Initialize variables
  var bookID = $routeParams.id;
  $scope.book = {};
  $scope.author = {};
  $scope.notes = [];

  function addNoteSuccess(newNote) {
    $scope.notes.push(newNote);
  }

  function addNoteError(error) {
    console.error(error);
    AppAlert.add('danger', 'Could not create note. Please try again later.');
  }

  $scope.addNoteForm = {
    focus: true,
    text: '',
    submit: function() {
      var payload = {
        book_id: bookID,
        text: $scope.addNoteForm.text
      };
      Note.create(payload).then(addNoteSuccess, addNoteError);
      $scope.addNoteForm.text = '';
    }
  };

  $scope.deleteNote = function(note, index) {
    Note.delete(note.id).then(function() {
      $scope.notes.splice(index, 1);
      AppAlert.add('danger', 'Deleted note.');
    });
  };

  $scope.editNote = function(newText, oldText, note) {
    var updatePromise = Note.update(note.id, {text: newText});

    updatePromise.then(function() {
      console.debug('updated note');
    },
      function(error) {
        console.error(error);
        AppAlert.add('danger', 'Could not update note.');
      }
    );
    return;
  };

  Book.get(bookID)
    .then(function(book) {
      $scope.book = book;
      $scope.author = book.author;
    }, function(error) {
      console.error(error);
      AppAlert.add('danger', 'Could not retrieve book');
    });

  Note.queryByBookID(bookID)
    .then(function(notes) {
      $scope.notes = notes;
    });

  $hotkey.bind('ctrl + n', function() {
      $scope.addNoteForm.focus = true;
    });

});
