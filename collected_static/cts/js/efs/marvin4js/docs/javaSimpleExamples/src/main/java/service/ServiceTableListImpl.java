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


public class ServiceTableListImpl implements Service {

	
	
	public String callFunc(String query) {
		Client client = ClientBuilder.newBuilder().register(GsonProvider.class).build();
		WebTarget cxnSearch = client.target("https://restdemo.chemaxon.com/rest-v0").path("data").path("sample").path("table");
		JsonElement response = cxnSearch.request(MediaType.APPLICATION_JSON_TYPE).get(JsonElement.class);
		//System.out.println("Resp:"+response.toString());
		return extractJsonResponse(response); 

	}

	private String extractJsonResponse(JsonElement element) {
		JsonArray data=element.getAsJsonArray();
		StringBuffer tableNames=new StringBuffer();
		for (JsonElement row:data) {
			tableNames.append(row.getAsJsonObject().get("tableName").getAsString()+", ");
		}
		return tableNames.toString();
	}


}
