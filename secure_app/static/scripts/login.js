var sanitizeHTML = function (str) {
	return str.replace(/[^\w. ]/gi, function (c) {
		return '&#' + c.charCodeAt(0) + ';';
	});
};

function checkIfInputSanitized(){

    username=document.getElementById("name_input").value;
    password=document.getElementById("pass_input").value;

    if(username!=sanitizeHTML(username) || password!=sanitizeHTML(password)){
        document.getElementById("name_input").innerHTML=sanitizeHTML(username);
        document.getElementById("pass_input").innerHTML=sanitizeHTML(password);
    }

}