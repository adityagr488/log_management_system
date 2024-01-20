const defaultQueryParameters = {
    "size": 0,
    "level": "string",
    "message": "string",
    "resourceId": "string",
    "timestamp": "string (date and time in ISO 8601 format)",
    "date": {
        "from_date": "string (date and time in ISO 8601 format)",
        "to_date": "string (date and time in ISO 8601 format)"
    },
    "traceId": "string",
    "spanId": "string",
    "commit": "string",
    "parentResourceId": "string"
}

var queryEditor = CodeMirror(document.getElementById("queryInput"), {
    mode: { name: "javascript", json: true },
    theme: "dracula",
    lineNumbers: true,
    autoCloseBrackets: true,
});

queryEditor.setValue(JSON.stringify(defaultQueryParameters, null, 2));

var responseViewer = CodeMirror(
    document.getElementById("queryResponse"),
    {
        mode: { name: "javascript", json: true },
        theme: "dracula",
        lineNumbers: true,
        readOnly: true,
    }
);

responseViewer.isReadOnly();

function resetQuery() {
    queryEditor.setValue(JSON.stringify(defaultQueryParameters, null, 2));
}

function clearResponse() {
    responseViewer.setValue("");
    document.getElementById("responseCode").innerHTML = "Response Status: ";
}

function executeQuery() {
    var query = queryEditor.getValue();
    document.getElementById("responseStatus").style.display = "none";
    document.getElementById("loadingIcon").style.display = "block";
    try {
        var parsedQuery = JSON.parse(query);

        fetch("/query", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(parsedQuery),
        })
            .then(response => {
                document.getElementById("loadingIcon").style.display = "none";
                document.getElementById("responseStatus").style.display = "block";
                document.getElementById("responseStatus").innerHTML = (response.status || "");
                return response.json();
            })
            .then(data => {
                responseViewer.setValue(JSON.stringify(data, null, 2));
                responseViewer.setOption("theme", "dracula");
            })
    } catch (error) {
        responseViewer.setValue(error.message || 'Error parsing the JSON');
    }
}


