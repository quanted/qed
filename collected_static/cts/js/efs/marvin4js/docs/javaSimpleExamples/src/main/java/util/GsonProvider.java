package util;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.lang.annotation.Annotation;
import java.lang.reflect.Type;

import javax.ws.rs.Consumes;
import javax.ws.rs.Produces;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.MultivaluedMap;
import javax.ws.rs.ext.MessageBodyReader;
import javax.ws.rs.ext.MessageBodyWriter;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;

@Consumes({ MediaType.APPLICATION_JSON, "text/json" })
@Produces({ MediaType.APPLICATION_JSON, "text/json" })
public class GsonProvider implements MessageBodyReader<JsonElement>,
		MessageBodyWriter<JsonElement> {

	private Gson gson;

	public GsonProvider() {
		GsonBuilder gsonBuilder = new GsonBuilder();
		gson = gsonBuilder.create();
	}

	public boolean isWriteable(Class<?> type, Type genericType,
			Annotation[] annotations, MediaType mediaType) {
		return JsonElement.class.isAssignableFrom(type);
	}

	public long getSize(JsonElement t, Class<?> type, Type genericType,
			Annotation[] annotations, MediaType mediaType) {
		return 0;
	}

	public void writeTo(JsonElement t, Class<?> type, Type genericType,
			Annotation[] annotations, MediaType mediaType,
			MultivaluedMap<String, Object> httpHeaders,
			OutputStream entityStream) throws IOException,
			WebApplicationException {
		OutputStreamWriter writer = new OutputStreamWriter(entityStream, "UTF-8");
		try {
			gson.toJson(t, type, writer);
		} finally {
			writer.close();
		}

	}

	public boolean isReadable(Class<?> type, Type genericType,
			Annotation[] annotations, MediaType mediaType) {
		return JsonElement.class.isAssignableFrom(type);
	}

	public JsonElement readFrom(Class<JsonElement> type, Type genericType,
			Annotation[] annotations, MediaType mediaType,
			MultivaluedMap<String, String> httpHeaders, InputStream entityStream)
			throws IOException, WebApplicationException {
		InputStreamReader streamReader = new InputStreamReader(entityStream, "UTF-8");
	    try {
	      return gson.fromJson(streamReader, type);
	    } finally {
	      streamReader.close();
	    }
	}

}
