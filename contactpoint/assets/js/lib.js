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
  /*
  Reconnecting Web Socket Library version: 64fd94093e2a49a4643dd2cfbbd60df5225b0ed7
  https://github.com/joewalnes/reconnecting-websocket/
  */
function ReconnectingWebSocket(a){function f(g){c=new WebSocket(a);if(b.debug||ReconnectingWebSocket.debugAll){console.debug("ReconnectingWebSocket","attempt-connect",a)}var h=c;var i=setTimeout(function(){if(b.debug||ReconnectingWebSocket.debugAll){console.debug("ReconnectingWebSocket","connection-timeout",a)}e=true;h.close();e=false},b.timeoutInterval);c.onopen=function(c){clearTimeout(i);if(b.debug||ReconnectingWebSocket.debugAll){console.debug("ReconnectingWebSocket","onopen",a)}b.readyState=WebSocket.OPEN;g=false;b.onopen(c)};c.onclose=function(h){clearTimeout(i);c=null;if(d){b.readyState=WebSocket.CLOSED;b.onclose(h)}else{b.readyState=WebSocket.CONNECTING;if(!g&&!e){if(b.debug||ReconnectingWebSocket.debugAll){console.debug("ReconnectingWebSocket","onclose",a)}b.onclose(h)}setTimeout(function(){f(true)},b.reconnectInterval)}};c.onmessage=function(c){if(b.debug||ReconnectingWebSocket.debugAll){console.debug("ReconnectingWebSocket","onmessage",a,c.data)}b.onmessage(c)};c.onerror=function(c){if(b.debug||ReconnectingWebSocket.debugAll){console.debug("ReconnectingWebSocket","onerror",a,c)}b.onerror(c)}}this.debug=false;this.reconnectInterval=1e3;this.timeoutInterval=2e3;var b=this;var c;var d=false;var e=false;this.url=a;this.readyState=WebSocket.CONNECTING;this.URL=a;this.onopen=function(a){};this.onclose=function(a){};this.onmessage=function(a){};this.onerror=function(a){};f(a);this.send=function(d){if(c){if(b.debug||ReconnectingWebSocket.debugAll){console.debug("ReconnectingWebSocket","send",a,d)}return c.send(d)}else{throw"INVALID_STATE_ERR : Pausing to reconnect websocket"}};this.close=function(){if(c){d=true;c.close()}};this.refresh=function(){if(c){c.close()}}}ReconnectingWebSocket.debugAll=false

  var listen = function() {
  	var taps = new ReconnectingWebSocket("ws://127.0.0.1:8008/listen_taps");
  	taps.onmessage = function(evt) {
      var d = JSON.parse(evt.data);
      $(window).trigger('rfid:action', d);
    };
    taps.onopen = function() {
      $(window).trigger('rfid:server_active');
    };
  	taps.onclose = function() {
      $(window).trigger('rfid:server_inactive');
    };
    taps.onerror = function (evt) {
      console.log("Error:", evt);
    };

  };
  listen();
}());