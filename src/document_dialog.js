var controllerPath = "/myAccount/myDocuments.htm";
var ownerId = null;
var autoApprove = true;

$(document).ready(function() {
	orbisApp.setUpRegularDialog("#packageDialog", {"Create Application Package":function(){processAndCallback()}, "Cancel":function(){$(this).dialog("close");}});
});
		
function downloadPDF(docId)
{
	$("#docId", "#downloadPdfForm").val(docId);
	$("#downloadPdfForm").submit();
}

function gotoDocMgt()
{
	$("#ownerId", "#docMgtForm").val(ownerId);
	$("#docMgtForm").submit();
}

/**
 * Parent page should call this function to display the dialog
 */	
function openPackageDialog(docOwnerId)
{
	if (null != docOwnerId)
	{
		ownerId = docOwnerId;
		
		$("#packageName", "#packageDialog").val("");
		$("#packageDialog #approved:checkbox").attr("checked", false);
		$("#packageDialog #docTable").empty();

		var request = new Object();
		request.action = "packageDialogData";
		request.ownerId = ownerId;
		request.rand = Math.floor(Math.random()*100000);

		$.post(controllerPath, request, function(data) {
			for (var i = 0; i < data.length; i++)
			{
				addDocType(data[i]);
			}
			$("#packageDialog").dialog("open");
			$("#packageDialog #packageName").focus();
		}, "json");
	}
	else
	{
		orbisApp.alertDialog("ERROR openPackageDialog(): Missing docOwnerId!!", true, 300);
	}
}

function addDocType(dtData)
{
	$("#docTable").append(makeDocTypeRow(dtData.docType));
	for (var i = 0; i < dtData.dtDocs.length; i++)
	{
		$("#docTable td:last").append(makeDocEntry(dtData.docType, dtData.dtDocs[i]));
	}		
}

function makeDocTypeRow(docType)
{
	var html = "";
	html += "<tr required='" + docType.requiredInPackage + "' docTypeName='" + docType.name + "'><td class='yellowBox'>";
	html += "<div>";
	html += "<div style='float:left;font-weight:bold;'>" + docType.name + "</div>";
	html += "<div style='float:right;font-size: small; color: #808080;font-style: italic'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
	if(docType.requiredInPackage)
	{
		html += "1 required";
	}
	else
	{
		html += "optional";
	} 
	html += "</div>";		
	html += "<div class='clearFix'></div>";
	html += "</div>";
	html += "<hr>";
	html += "</td></tr>";
	return html;
}

function makeDocEntry(docType, doc)
{
	var html = "";
	html += "<div style='float:left'>";
	html += "<a href='#' onclick='downloadPDF(" + doc.id + ");return false;'> <img src='/site/images/buttons/butPDF.gif'> </a>&nbsp;&nbsp;";
	html += doc.name;
	html += "</div>";
	html += "<div style='float:right'>";
	html += "<input type='radio' name='" + docType.id + "' value='" + doc.id + "'/>";
	html += "</div>";
	html += "<div class='clearFix'></div>";
	return html;
}


function processAndCallback() {
	var errors = new Array();
	
	if ($("#packageDialog #packageName").val() == "")
	{
		isValid = false;
		errors.push("Application Package name is missing.\n");
	}
	
	$("#packageDialog #docTable tr[required='true']").each(function() {
		if ($(this).find("input:radio:checked").length == 0)
		{
			isValid = false;
			errors.push("Package is missing a required \"" + $(this).attr("docTypeName") + "\" document.\n");
		}
	});

	if (errors.length == 0)
	{
		$("#packageDialog").dialog("close");
		
		// Create the package definition.
	    var pkgDef = new Array();
	    $("#packageDialog #docTable input:radio:checked").each(function() {
	    	var doc = new Object();
	    	doc.docTypeId = $(this).attr("name");
	    	doc.docId = $(this).val();
	    	pkgDef.push(doc);
	    });
		
		// **********************************************************************************
		// Call the callback function, passing along the package-definition.
		// The parent page should have an implementation of this function.
		   createPackage($("#packageDialog #packageName").val(), ownerId, pkgDef, isApproved());
		// **********************************************************************************
	}
	else
	{
		var errorMsg = "";
		for (var i = 0; i < errors.length; i++)
		{
			errorMsg += errors[i];
		}
		orbisApp.alertDialog(errorMsg, true, 300);
	}		

};

function isApproved()
{
	return autoApprove ? true : $("#packageDialog #approved:checked").length == 1;
}
