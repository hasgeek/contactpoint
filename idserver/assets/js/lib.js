/*
lib.js is a file that can be loaded from all applications that want to
subscribe to an RFID tap.
After loading this file, take the action that will be
executed on tap, in the following manner:
$(window).on('tap:received', function(e, data) {
    //...do my stuff and do it well...
});
*/
$(function() {
  var listen = function() {
  	var taps = new WebSocket("ws://127.0.0.1:8008/listen_taps");
  	taps.onmessage = function(evt) {
      var d = JSON.parse(evt.data);
      $(window).trigger('tap:received', d);
    }
  	taps.onclose = function() {
      //WebSocket closed
    };
    taps.onerror = function (evt) {
      console.log("Error:", evt);
    }
  };
  listen();
}());