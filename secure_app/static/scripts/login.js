//flaskAddress="http://localhost:5678"; //DLA NIE SSL (http)
flaskAddress="https://localhost:5678"; //DLA SSL (docker glownie) (https)
var min_pass_str=50;

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

function returnToIndex(){
    window.location.replace(flaskAddress+"/index");
}

function checkPasswordStrength(p){

    var sum=0;
    var formatS = /[ `!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;
    var formatU = /[QWERTYUIOPASDFGHJKLZXCVBNM]/;
    var formatL = /[qwertyuiopasdfghjklzxcvbnm]/;
    var formatN = /[1234567890]/;

    if(formatS.test(p)){
        sum+=32;
    }
    if(formatU.test(p)){
        sum+=26;
    }
    if(formatL.test(p)){
        sum+=26
    }
    if(formatN.test(p)){
        sum+=10
    }

    return p.length*Math.log2(sum)
}

function checkData(){

    console.log("xdd")
    var p = document.getElementById("pass_input").value;

    if(min_pass_str>checkPasswordStrength(p)){
        document.getElementById("login_button").disabled=true;
        document.getElementById("error_message").innerHTML="too weak new password";
    } else{
        document.getElementById("login_button").disabled=false;
        document.getElementById("error_message").innerHTML="";
    }
}