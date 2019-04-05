<?php
header("Access-Control-Allow-Origin: *");

function process_data($value){
        return $value;
}

try{
	$db = new PDO('mysql:host=localhost;dbname=educeco;charset=utf8', 'root', ''); //try to connect to the database
}
catch (Exception $e){
        die('Erreur : ' . $e->getMessage());                                       // if fails, abort the script's execution
}

$response = $db->query("SELECT * FROM tests ORDER BY id DESC LIMIT 1");               // request the DB to send the last record
$data = $response->fetch();
echo("{\"id\":\"". $data['id'] . "\",\"type\":" . "\"" . $data['type'] . "\",\"value\"" . ":" . "\"" . process_data($data['value']) . "\",\"unit\":" . "\"" . $data['unit'] . "\"}");        //prints the JSON-formatted values -and here the converted speed-
?>