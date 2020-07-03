<?php
header('Content-Type: text/plain');
header('Access-Control-Allow-Origin: *');

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
    echo "Connection failed: " . $e->getMessage();
}

$r = $conn->prepare("SELECT panel from screen");
$r->execute();
$d = $r->fetch();
$panel = strtolower($d[0]);
echo($panel),

$conn = null;
?>
