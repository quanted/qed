<%@ tag description="display the whole nodeTree" pageEncoding="UTF-8"%>
<%@ attribute name="node" type="java.util.Map" required="true"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib prefix="template" tagdir="/WEB-INF/tags"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/functions" prefix="fn"%>

<table>
	<thead>
		<tr>
			<th>Option</th>
			<th>Type</th>
			<th>Description</th>
		</tr>
	</thead>
	<tbody>
		<c:choose>
			<c:when test="${!node.$jsonArray && !node.$jsonObject}">
				<c:forEach var="entry" items="${node}">
					<c:choose>
						<c:when test="${!fn:startsWith(entry.key,'$')}">
							<c:set var="typeNode" value="${entry.value}" />
							<c:if test="${entry.value.$jsonArray || entry.value.$jsonObject}">
								<c:set var="typeNode" value="${typeNode.$elementType}" />
							</c:if>

							<c:choose>
								<c:when test="${typeNode.$isPrimitive}">
									<tr>
										<c:choose>
											<c:when test="${entry.value.$jsonArray}">
												<td>${entry.key}</td>
												<td>ARRAY OF ${typeNode.$type}</td>
											</c:when>
											<c:when test="${entry.value.$jsonObject}">
												<td>${entry.key}</td>
												<td>MAP OF ${typeNode.$type}</td>
											</c:when>
											<c:otherwise>
												<td>${entry.key}</td>
												<td>${typeNode.$type}</td>
											</c:otherwise>
										</c:choose>
										<td><c:if test="${typeNode.$defaultValue != null}">default: <b>${typeNode.$defaultValue}</b>
											</c:if> <c:if test="${entry.value.$doc != null}"><br />${entry.value.$doc.comment}<br />${entry.value.$doc.tags.see}</c:if> <c:if test="${fn:length(typeNode.$values) > 0}">
												<ul>
													<c:forEach var="value" items="${typeNode.$values}">
														<li><c:choose>
																<c:when test="${typeNode.$defaultValue == value.$value}">
																	<b>${value.$value}</b>
																</c:when>
																<c:otherwise>
																	<i>${value.$value}</i>
																</c:otherwise>
															</c:choose> <c:if test="${value.$doc.comment != null}">: ${value.$doc.comment}<br />${value.$doc.tags.see}</c:if></li>
													</c:forEach>
												</ul>
											</c:if></td>
									</tr>
								</c:when>
								<c:otherwise>
									<tr>
										<c:choose>
											<c:when test="${entry.value.$jsonArray}">
												<td>${entry.key}</td>
												<td>ARRAY</td>
												<c:set var="printNode" value="${typeNode}" />
											</c:when>
											<c:when test="${entry.value.$jsonObject}">
												<td>${entry.key}</td>
												<td>MAP</td>
												<c:set var="printNode" value="${typeNode}" />
											</c:when>
											<c:otherwise>
												<td>${entry.key}</td>
												<td>OPTION GROUP</td>
												<c:set var="printNode" value="${typeNode}" />
											</c:otherwise>
										</c:choose>
										<td><c:if test="${entry.value.$doc.comment != null}">${entry.value.$doc.comment}<br />${entry.value.$doc.tags.see}</c:if> <template:printNode node="${printNode}" /></td>
									</tr>
								</c:otherwise>
							</c:choose>
						</c:when>
					</c:choose>
				</c:forEach>
			</c:when>
			<c:otherwise>
				<tr>
					<c:choose>
						<c:when test="${node.$jsonArray}">
							<td></td>
							<td>ARRAY OF ${node.$elementType.$type}</td>
						</c:when>
						<c:when test="${node.$jsonObject}">
							<td></td>
							<td>MAP OF ${node.$elementType.$type}</td>
						</c:when>
						<c:otherwise>
							<td>?</td>
							<td>?</td>
						</c:otherwise>
					</c:choose>
					<td></td>
				</tr>
			</c:otherwise>
		</c:choose>
	</tbody>
</table>


