'use strict';

var app = angular.module('appApp');

app.factory('Note', function ($http, serverConfig, relativeDate) {
  var baseUrl = serverConfig.DOMAIN + '/api/notes/';

  // Constructor
  function Note(data) {
    var self = this;
    angular.extend(self, data);
    self.createdDate = new Date(self.created);
    relativeDate.set(self.created, function(relDate) {
      self.createdRelative = relDate;
    });
  }

  Note.get = function(id) {
    return $http.get(baseUrl + id)
      .then(function(resp) { return new Note(resp.data.result); });
  };

  Note.create = function(params) {
    return $http.post(baseUrl, params).then(function(resp) {
      return new Note(resp.data.result);
    });
  };

  Note.update = function(id, params) {
    return $http.put(baseUrl + id, params).then(function(resp) {
      return new Note(resp.data.result);
    });
  };

  Note.query = function() {
    return $http.get(baseUrl).then(function(resp) {
      var noteDataArray = resp.data.result;
      return noteDataArray.map(function(noteData) {
        return new Note(noteData);
      });
    });
  };

  Note.queryByBookID = function(bookID) {
    var url = serverConfig.DOMAIN + '/api/books/' + bookID + '/notes/';
    return $http.get(url).then(function(resp) {
      var noteDataArray = resp.data.result;
      return noteDataArray.map(function(noteData) {
        return new Note(noteData);
      });
    });
  };

  Note.delete = function(id) {
    return $http.delete(baseUrl  + id);
  };

  return Note;

});
