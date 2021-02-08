<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/functions" prefix="fn"%>
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Api documentation of: ${classNames}</title>
	<link rel="stylesheet" type="text/css" href="${contextPath}/docs/style/style.css">
	<link rel="shortcut icon" href="${contextPath}/docs/style/favicon.ico">
</head>
<body>
<c:forEach var="className" items="${fn:split(classNames, ',')}">
<h2>${className}</h2>
<jsp:include page="/gendocs/generateEmbedded?className=${className}" />
</c:forEach>
</body>
</html>