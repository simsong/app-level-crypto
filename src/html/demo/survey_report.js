$(document).ready(function() {
   // Every 2 seconds, fetch a new table
   setInterval(function () {
      $.get('survey_report.cgi', { 'request': 'fetch_results' }, function(response) {
         $("#response").html(response);
         $("#response table tr:nth(1)").css({ 'background-color': "#ffffcc" });
      });
   },2000);
});
