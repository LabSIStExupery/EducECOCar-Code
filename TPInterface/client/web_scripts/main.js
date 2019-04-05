$(function(){
    var tid = setInterval(function(){
        $.ajax({
            url: 'http://localhost/EducEco/TPInterface/server/get_data.php',
            type: 'GET',
            dataType: "json"
          })
          .done(function(data) {
            $("#title").text(data.type + " :");
            $("#value").text(data.value);
            $("#unit").text(data.unit);
            console.log(data);
          })
          .fail(function(err) {
            console.log('Error: ' + err.status);
          });
    }, 500);

/*function abortTimer() { // to be called when you want to stop the timer
  clearInterval(tid);
}*/

})