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

//make a request to the root url
$request = $client->get('');
$response = $request->send();
$data = $response->json();

//display a hello message
echo $data['welcomeMessage'] . ' ' . $data['version'] . PHP_EOL;

?>