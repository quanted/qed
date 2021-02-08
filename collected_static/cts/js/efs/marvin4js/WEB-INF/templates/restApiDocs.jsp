<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/functions" prefix="fn"%>
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Api documentation of JChem Web Services</title>
	<link rel="stylesheet" type="text/css" href="${contextPath}/docs/style/style.css">
	<link rel="shortcut icon" href="${contextPath}/docs/style/favicon.ico">
</head>
<body>
<c:forEach var="restApiDoc" items="${restApiDocs}">
<h2>${restApiDoc['http-method']} ${restApiDoc['request-uri']}</h2>

<c:if test="${restApiDoc.javaDoc.comment != null}" >
<p>${restApiDoc.javaDoc.comment}</p>
</c:if>

<c:if test="${restApiDoc['path-params'] != null}" >
<p>Path parameters: ${restApiDoc['path-params']}</p>
</c:if>

<c:if test="${restApiDoc['query-params'] != null}" >
<p>Query parameters: ${restApiDoc['query-params']}</p>
</c:if>

<p>Request (<code><b>Content-Type:</b> ${restApiDoc['content-type']}</code>)</p>
<c:if test="${restApiDoc['http-method'] != 'GET'}" >
<jsp:include page="/gendocs/generateEmbedded?className=${restApiDoc['request-type']}" />
</c:if>

<c:if test="${restApiDoc['response-type'] != null}" >
<p>Response</p>
<jsp:include page="/gendocs/generateEmbedded?className=${restApiDoc['response-type']}" />
</c:if>

</c:forEach>
</body>
</html>