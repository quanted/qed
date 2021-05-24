package service;


import java.io.File;



import javax.ws.rs.client.Client;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.client.Entity;
import javax.ws.rs.client.WebTarget;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import org.glassfish.jersey.media.multipart.FormDataMultiPart;
import org.glassfish.jersey.media.multipart.MultiPart;
import org.glassfish.jersey.media.multipart.MultiPartFeature;
import org.glassfish.jersey.media.multipart.file.FileDataBodyPart;

import util.GsonProvider;



public class ServiceImportImpl implements Service {

	
	
	public String callFunc(String filename) {
		
		Client client = ClientBuilder.newBuilder().register(GsonProvider.class).register(MultiPartFeature.class).build();
		WebTarget cxnImport = client.target("https://restdemo.chemaxon.com/rest-v0").path("data").path("sample");
		
		
		
		
		
			FileDataBodyPart filePart = new FileDataBodyPart("file", new File("examples.mrv"));
	    	MultiPart multipart = new FormDataMultiPart()
	        .field("tableName", "test")
	        .field("monitorID", "id")
	        .bodyPart(filePart);
	     
	    	Response response = cxnImport.request().post(Entity.entity(multipart, multipart.getMediaType()));

	   
	    	return response.toString(); 

	}

}
