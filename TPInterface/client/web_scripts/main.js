function print_error(title, message){
  $("#error").css("display", "block");
  $("#err_title").text(title);
  $("#err_content").text(message);
}

function hide_error(){
  $("#error").css("display", "none");
}

$(function(){
    var oldID = 0;
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

            if(data.id == oldID){
              print_error("Données non-renouvellées", "Les données renvoyées par le server ne sont pas renouvellées, vérifiez que le parser est démarré, que le montage est relié à l'ordinateur et la base de données accessible.");
            } else {
              hide_error();
            }
            oldID = data.id;
          })
          .fail(function(err) {
            print_error("Données inateignables", "Le serveur ne renvoie pas de données, vérifiez la disponobilité du server PHP.")
          });
    }, 500);

/*function abortTimer() { // to be called when you want to stop the timer
  clearInterval(tid);
}*/

})