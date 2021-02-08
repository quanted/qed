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

//load the list of tables in the sample database
$request = $client->get('data/sample/table');
$response = $request->send();
$tables = $response->json();

//iterate through each table
foreach($tables as $table) {
	echo 'Searching in table: ' . $table['tableName'] . PHP_EOL;

	//perform an advanced search request that looks for benzene
	//specify SMILES as the molecule format and disable image generation
	$request = $client->post('data/sample/table/' . $table['tableName'] . '/search', null, json_encode(array(
		'searchOptions' => array(
			'queryStructure' => 'C1=CC=CC=C1'
		),
		'display' => array(
			'include' => array('cd_id', 'cd_structure'),
			'parameters' => array(
				'cd_structure-display' => array(
					'parameters' => array(
						'structureData' => 'cxsmiles',
						'image' => array(
							'returnImage' => false
						)
					)
				)
			)
		),
		'paging' => array(
			'limit' => 1
		)

	)));
	$request->setHeader('Content-Type', 'application/json');
	$response = $request->send();
	$results = $response->json();

	//display the search results
	echo $results['total'] . ' structures containing benzene' . PHP_EOL;
	if ($results['total'] > 0) {
		echo 'First one is ID ' . $results['data'][0]['cd_id'] . ': ' . $results['data'][0]['cd_structure']['structureData']['structure'] . PHP_EOL;
	}
	echo PHP_EOL;

}

?>