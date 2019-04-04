<?php
header("Access-Control-Allow-Origin: *");
try{
	$db = new PDO('mysql:host=localhost;dbname=educeco;charset=utf8', 'root', ''); //try to connect to the database
}
catch (Exception $e){
        die('Erreur : ' . $e->getMessage());                                       // if fails, abort the script's execution
}

$response = $db->query("SELECT type,value,unit FROM tests LIMIT 1");               // request the DB to send the last record
$data = $response->fetch();
echo("{\"type\":" . "\"" . $data['type'] . "\",\"value\"" . ":" . "\"" . $data['value']*3.6/10 . "\",\"unit\":" . "\"" . $data['unit'] . "\"}");        //prints the JSON-formatted values -and here the converted speed-
?>