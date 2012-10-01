/*
lib.js can be a file that can be loaded from all applications that want to
subscribe to an RFID tap.
I felt that this should also be protected from who can subscribe to WS that
pushes RFID taps.
As of now, the continuous polling that's happening validates that with jsonp.
Right now, I am keeping this open while it is in Proof of Concept.

@jace & @geohacker: you would be in a better position to take a call on how
to make this secure

After loading this file, you are needed to assign the action that will be
executed on tap, by att

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