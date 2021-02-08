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


public class TableServiceImpl implements TableService {

	
	
	public List<List<String>> getTableContent(String query) {
		Client client = ClientBuilder.newBuilder().register(GsonProvider.class).build();
		WebTarget cxnSearch = client.target("https://restdemo.chemaxon.com/rest-v0").path("data").path("sample").path("table").path("Drugbank_all").path("search");
		JsonElement request = createRequestObject(query);
		//System.out.println("Req:"+request.toString());
		JsonElement response = cxnSearch.request(MediaType.APPLICATION_JSON_TYPE).post(Entity.entity(request, MediaType.APPLICATION_JSON),JsonElement.class);
		//System.out.println("Resp:"+response.toString());
		return extractTableFromResponse(response); 

	}

	private List<List<String>> extractTableFromResponse(JsonElement element) {
		JsonArray data=element.getAsJsonObject().get("data").getAsJsonArray();
		List<List<String>> table=new ArrayList<List<String>>();
		for (JsonElement row:data) {
			List<String> tableRow=new ArrayList<String>();
			table.add(tableRow);
			tableRow.add(row.getAsJsonObject().get("cd_id").getAsString());
			tableRow.add(row.getAsJsonObject().get("c_drugbank_id").getAsString());
			JsonElement sim=row.getAsJsonObject().get("similarity");
			tableRow.add(sim==null?"NA":sim.getAsString());
			tableRow.add(row.getAsJsonObject().get("c_smiles").getAsString());

			JsonElement brands=row.getAsJsonObject().get("c_brands");
			tableRow.add(brands==null?"None":brands.getAsString());
		}
		return table;
	}

	private JsonObject createRequestObject(String query) {;
		JsonObject root=new JsonObject();
		JsonObject searchOptions=new JsonObject();
		root.add("searchOptions", searchOptions);
		JsonObject paging=new JsonObject();
		root.add("paging", paging);
		JsonObject similarity=new JsonObject();
		searchOptions.add("similarity", similarity);
		
		searchOptions.add("searchType", new JsonPrimitive("SIMILARITY"));
		searchOptions.add("queryStructure", new JsonPrimitive(query));


		similarity.add("descriptor", new JsonPrimitive("CFP"));
		similarity.add("threshold", new JsonPrimitive(0.5));

		paging.add("limit", new JsonPrimitive(10));
		paging.add("offset", new JsonPrimitive(0));
		return root;
	}

}
