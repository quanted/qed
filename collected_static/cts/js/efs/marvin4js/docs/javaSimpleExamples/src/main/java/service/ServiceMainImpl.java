package service;

import java.util.ArrayList;
import java.util.List;

import javax.ws.rs.client.Client;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.client.Entity;
import javax.ws.rs.client.WebTarget;
import javax.ws.rs.core.MediaType;

import util.GsonProvider;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonPrimitive;


public class ServiceMainImpl implements Service {

	
	
	public String callFunc(String param) {
		Client client = ClientBuilder.newBuilder().register(GsonProvider.class).build();
		WebTarget cxnSearch = client.target("https://restdemo.chemaxon.com/rest-v0");
		String response = cxnSearch.request().get(String.class);
		//System.out.println("Resp:"+response.toString());
		return response; 

	}

}
