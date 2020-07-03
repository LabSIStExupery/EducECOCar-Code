<?php
error_reporting(E_ALL);
ini_set('display_errors', TRUE);
ini_set('display_startup_errors', TRUE);
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

function getMain($conn){
    //fetching basic infos  
    $r = $conn->prepare("SELECT Speed FROM Speed ORDER BY id DESC LIMIT 0,1;");
    $r->execute();
    $d1 = $r->fetch();
    $speed = $d1[0];

    $r = $conn->prepare("SELECT Percentage FROM PBattery ORDER BY id DESC LIMIT 0,1;");
    $r->execute();
    $d1 = $r->fetch();
    $percentage = $d1[0];

    $r = $conn->prepare("SELECT Time FROM PAutonomy ORDER BY id DESC LIMIT 0,1;");
    $r->execute();
    $d1 = $r->fetch();
    $time = $d1[0];
   
    $r = $conn->prepare("SELECT Distance FROM PDistance ORDER BY id DESC LIMIT 0,1;");
    $r->execute();
    $d1 = $r->fetch();
    $distance = $d1[0];

    $hours = floor($time / 60);
    $minutes = ($time % 60);

    unset($d1); //delete var $d1 to free memory and keep ressources
    unset($time);

    //fetching instant power
    $r = $conn->prepare("SELECT (Battery.Cell1 + Battery.Cell2 + Battery.Cell3), TS FROM Battery ORDER BY id DESC LIMIT 0,1;");
    $r->execute();
    $d2 = $r->fetch();
    $totalVoltage = $d2[0];
    $TS = $d2[1];
    $r = $conn->prepare("SELECT Current FROM Current WHERE TS = ?;");
    $r-> execute(array($TS));
    $d2 = $r->fetch();
    $instantPower = $totalVoltage * $d2[0];
    unset($d2); //delete var $d2 to free memory and keep ressources

    //fetching AVG speed
    $r = $conn->prepare("SELECT AVG(Speed) FROM Speed ORDER BY TS DESC LIMIT 0,180");
    $r->execute();
    $d3 = $r->fetch();
    $AVGSpeed = $d3[0];
    unset($d3); //delete var $d3 to free memory and keep ressources
    return array(
        "speed" => $speed,
        "power" => $instantPower,
        "percentage" => $percentage,
        "hours" => $hours,
        "minutes" => $minutes,
        "avgspeed" => $AVGSpeed,
        "distance" => $distance
    );
}

function getTemp($conn){
    $r = $conn->prepare("SELECT Temp1, Temp2, Temp3 FROM Temperature ORDER BY id DESC LIMIT 0,1");
    $r->execute();
    $d = $r->fetch();
    $temp1 = $d[0];
    $temp2 = $d[1];
    $temp3 = $d[2];

    return array(
        "temp1" => $temp1,
        "temp2" => $temp2,
        "temp3" => $temp3
    );
}

function getElectrical($conn){
    //fetching basic data
    $start = microtime(true);

    $r = $conn->prepare("SELECT Percentage FROM PBattery ORDER BY id DESC LIMIT 0,1");
    $r->execute();
    $d = $r->fetch();
    $percentage = $d[0];

    $r = $conn->prepare("SELECT Time FROM PAutonomy ORDER BY id DESC LIMIT 0,1");
    $r->execute();
    $d = $r->fetch();
    $time = $d[0];

    $r = $conn->prepare("SELECT Cell1, Cell2, Cell3 FROM Battery ORDER BY id DESC LIMIT 0,1;");
    $r->execute();
    $d = $r->fetch();
    $cell3 = $d[0];
    $cell1 = $d[1];
    $cell2 = $d[2];

    $hours = floor($time / 60);
    $minutes = ($time % 60);

    //fetching instant power
    $r = $conn->prepare("SELECT (Battery.Cell1 + Battery.Cell2 + Battery.Cell3), TS FROM Battery ORDER BY id DESC LIMIT 0,1;");
    $r->execute();
    $d2 = $r->fetch();
    $totalVoltage = $d2[0];
    $TS = $d2[1];
    $r = $conn->prepare("SELECT Current FROM Current WHERE TS = ?;");
    $r-> execute(array($TS));
    $d2 = $r->fetch();
    $instantPower = $totalVoltage * $d2[0];
    unset($d2); //delete var $d2 to free memory and keep ressources

    //processing cellBars
    $cellBar1 = ($cell1-3)/1.2*100;
    $cellBar2 = ($cell2-3)/1.2*100;
    $cellBar3 = ($cell3-3)/1.2*100;

    $rawConfig = file_get_contents("/home/pi/Educeco/config.json");
    $config = json_decode($rawConfig, true);

    $maxCapacity = $config["BatteryCapacity"];
    $capacity = $percentage * 100 / $maxCapacity;
    echo(microtime(true) - $start);
    return array(
        "percentage" => $percentage,
        "hours" => $hours,
        "minutes" => $minutes,
        "capacity" => $capacity,
        "cell1voltage" => $cell1,
        "cell2voltage" => $cell2,
        "cell2voltage" => $cell2,
        "cell1bar" => $cellBar1,
        "cell2bar" => $cellBar2,
        "cell3bar" => $cellBar3,
        "power" => $instantPower
    );

}

$rawConfig = file_get_contents("/home/pi/Educeco/config.json");
$config = json_decode($rawConfig, true);
$database = $config["database"]["databaseName"];
$username = $config["database"]["databaseUser"];
$password = $config["database"]["databasePassword"];
$servername = $config["database"]["databaseHost"];

try {
    $conn = new PDO("mysql:host=$servername;dbname=$database", $username, $password);
    // set the PDO error mode to exception
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    echo(json_encode(array("errors" => array("title" => "Database Connection", "content" => "Impossible de se connecter à la base de données"))));
}

if(isset($_GET["panel"])){
    switch($_GET["panel"]){
        case "main":
            $data = getMain($conn);
            echo(json_encode($data));
            break;
        case "temp":
            $data = getTemp($conn);
            echo(json_encode($data));
            break;
        case "electrical":
            $data = getElectrical($conn);
            echo(json_encode($data));
    }
}
else{
    echo(json_encode(array("errors" => array("title" => "Panel selection", "content" => "Aucun panel selectionné"))));
}

$conn = null;
?>
