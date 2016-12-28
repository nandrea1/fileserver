/**
 * Created by nickandreadis on 12/27/16.
 */
var ws = new WebSocket("ws://localhost:8000/ws");
ws.onmessage = function (evt)
             {
                var event = JSON.parse(evt.data);
                console.log(event);
                created_at = event.created_at;
                event_type = event.event_type;
                event_value = event.event_value;
                console.log(event_value)
                event_html = "<tr><td>" + created_at + "</td><td>" + event_type + "</td><td>" + event_value + "</td></tr>";
                console.log(event_html)
                $("#events").append(event_html)
             };
$(document).ready(function() {
  $('#events').DataTable( {
      'processing': true,
      'serverSide': true,
      'ajax': '/api/events',
      'searching': false,
      'columns': [
          {'data': 'created_at'},
          {'data': 'event_type'},
          {'data': 'event_value'}
      ]
  });
});