<?php

/*
#Installation

Windows:
https://getcomposer.org/Composer-Setup.exe

Linux:
curl -sS https://getcomposer.org/installer | php
php composer.phar require guzzle/guzzle:~3.7
*/

//load the installed guzzle rest client
require 'vendor/autoload.php';
use Guzzle\Http\Client;

//create a rest client to jchem web services
$client = new Client('http://localhost:8080/webservices2/rest-v0/');

echo 'Searching... ';

//perform an advanced search request that looks for purin
$request = $client->post('data/sample/table/Drugbank_all/search', null, json_encode(array(
	'searchOptions' => array(
		'queryStructure' => 'purin'
	),
	'display' => array(
		'include' => array('cd_id')
	),
	'filter' => array(
		'orderBy' => 'cd_molweight'
	),
	'paging' => array(
		'limit' => 5
	)

)));
$request->setHeader('Content-Type', 'application/json');
$response = $request->send();
$results = $response->json();

//get all the data stored
echo $results['total'] . ' structures found containing purin' . PHP_EOL . PHP_EOL;
foreach ($results['data'] as $result) {
	echo 'ID ' . $result['cd_id'] . ': ';

	$request = $client->get('data/sample/table/Drugbank_all/detail/' . $result['cd_id'] . '/polarSurfaceArea');
	$response = $request->send();
	$calcresults = $response->json();
	
	echo 'TPSA: ' . $calcresults['polarSurfaceArea'] . PHP_EOL;
}

echo PHP_EOL;

?>