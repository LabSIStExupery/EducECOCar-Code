olderrors = [];

function parseErrors(json){
    errors = [];
    data = JSON.parse(json);

    for(var err of data){
        errors.push({"title" : err["title"], "content" : err["content"]});
    }
    return errors;
}

function updateErrors(errors){
    if(olderrors !== errors){
        finalErr = "";
        for (i=0; i<errors.length; i++){
            finalErr += `<div class="error" id="err1">
            <p class="errTitle">` + errors[i]["title"] + `</p>
            <p class="errContent">` + errors[i]["content"] + `</p>
        </div>`
        }
        document.getElementById("errors").innerHTML = finalErr;
        olderrors = errors;
    }
}

function updateMain(json){
    var speed = document.getElementById("speed");
    var power = document.getElementById("power");
    var batterypercentage = document.getElementById("percentage");
    var hours = document.getElementById("hours");
    var minutes = document.getElementById("minutes");
    var batterybar = document.getElementById("remainingbattery");
    var avgspeed = document.getElementById("avgspeed");
    var distance = document.getElementById("distance");

    data = JSON.parse(json);

    speed.innerHTML = data["speed"];
    power.innerHTML = data["power"];
    batterypercentage.innerHTML = data["percentage"];
    hours.innerHTML = data["hours"];
    minutes.innerHTML = data["minutes"];
    batterybar.style.height =  100 - parseInt(data["percentage"]) + "%";
    avgspeed.innerHTML = data["avgspeed"];
    distance.innerHTML = data["distance"];
}

function updateTemp(json){
    var temp1 = document.getElementById("temp1V");
    var temp2 = document.getElementById("temp2V");
    var temp3 = document.getElementById("temp3V");

    data = JSON.parse(json);

    temp1.innerHTML = data["temp1"];
    temp2.innerHTML = data["temp2"];
    temp3.innerHTML = data["temp3"];
}

function updateElectrical(json){
    var percentage = document.getElementById("epercentage");
    var hours = document.getElementById("ehours");
    var minutes = document.getElementById("eminutes");
    var capacity = document.getElementById("capacity");
    var cell1Voltage = document.getElementById("cellVoltage1");
    var cell2Voltage = document.getElementById("cellVoltage2");
    var cell3Voltage = document.getElementById("cellVoltage3");
    var cell1bar = document.getElementById("cellbar1");
    var cell2bar = document.getElementById("cellbar2");
    var cell3bar = document.getElementById("cellbar3");
    var power = document.getElementById("epower");
    var batterybar = document.getElementById("eremainingbattery");

    data = JSON.parse(json)

    percentage.innerHTML = data["percentage"]
    hours.innerHTML = data["hours"];
    minutes.innerHTML = data["minutes"];
    batterybar.style.height =  100 - parseInt(data["percentage"]) + "%";
    capacity.innerHTML = data["capacity"];
    power.innerHTML = data["power"]
    cell1Voltage.innerHTML = data["cell1voltage"];
    cell2Voltage.innerHTML = data["cell2voltage"];
    cell3Voltage.innerHTML = data["cell3voltage"];
    batterybar.style.height =  100 - parseInt(data["percentage"]) + "%";
    cell1bar.style.width = 100 - parseInt(data["cell1bar"]) + "%";
    cell2bar.style.width = 100 - parseInt(data["cell2bar"]) + "%";
    cell3bar.style.width = 100 - parseInt(data["cell3bar"]) + "%";
}

//while(true){
    console.log("Entrée dans la boucle");
    var panel = "main";
    //setTimeout(2000, function(){
        console.log("Ajax, premiere partie");
        $.ajax({
            url : "http://localhost/educeco/getscreen.php",
            type : "GET",
            dataType: "text",
            success : function(content, status){
				console.log("Succes de l'ajax 1");
                panel = content;
                var main = document.getElementById("mainScreen");
                var electrical = document.getElementById("electrical");
                var temp = document.getElementById("temp");

                if(panel == "main"){
                    main.style.display = "block";
                    electrical.style.display = "none";
                    temp.style.display = "none";
                } else if (panel == "electrical"){
                    main.style.display = "none";
                    electrical.style.display = "block";
                    temp.style.display = "none";
                } else if (panel == "temp"){
                    main.style.display = "none";
                    electrical.style.display = "none";
                    temp.style.display = "block";
                }
            }
        });
        $.ajax({
            url : 'http://localhost/educeco/getdata.php', // La ressource ciblée
            type : 'GET', // Le type de la requête HTTP.
            data : 'panel=' + panel,
            dataType : 'json',
            success : function(content, status){
				console.log(content);
                if(panel == "main"){
                    updateMain(content);
                } else if (panel == "electrical") {
                    updateElectrical(content);
                } else if (panel == "temp"){
                    updateTemp(content);
                }
            },
            error: function(result, status, error){
                alert("can't fetch data");
            }
         //});
    });
//}
