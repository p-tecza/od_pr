//DO DODANIA SPRAWDZENIE CO SIE ZNAJDUJE W SRODKU

//KONTROLA HASŁA DODANA

function emailValidation(){

    email=document.getElementById("email").value;
    var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    res = re.test(email);
    
    if(!res){
        document.getElementById("email").style.backgroundColor="#FBB2B2";
        document.getElementById("login_button").disabled=true;
        document.getElementById("error_message").innerHTML="e-mail is not correct.";
    }else{
        document.getElementById("email").style.backgroundColor="#FFFFFF";
        document.getElementById("login_button").disabled=false;
        document.getElementById("error_message").innerHTML="";
    }

}

function checkData(){

    {
        let p=document.getElementById("register_pass").value;
        let rp=document.getElementById("register_r_pass").value;

        entropy=checkPasswordStrength(p);

        if(p!=rp && entropy>=100){
            document.getElementById("register_r_pass").style.backgroundColor="#FBB2B2";
            document.getElementById("login_button").disabled=true;
            document.getElementById("error_message").innerHTML="passwords not equal.";
        }else if(entropy<100 && p==rp){
            document.getElementById("register_pass").style.backgroundColor="#FBB2B2";
            document.getElementById("login_button").disabled=true;
            document.getElementById("error_message").innerHTML="password too weak.";
        }
        else if(p!=rp && entropy<100){
            document.getElementById("register_pass").style.backgroundColor="#FBB2B2";
            document.getElementById("login_button").disabled=true;
            document.getElementById("error_message").innerHTML="passwords not equal and password is too weak.";
        }
        else{
            document.getElementById("register_r_pass").style.backgroundColor="#FFFFFF";
            document.getElementById("register_pass").style.backgroundColor="#FFFFFF";
            document.getElementById("login_button").disabled=false;
            document.getElementById("error_message").innerHTML="";
        }

    }

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

var sanitizeHTML = function (str) {
	return str.replace(/[^\w. ]/gi, function (c) {
		return '&#' + c.charCodeAt(0) + ';';
	});
};

function checkIfInputSanitized(){

    let username=document.getElementById("register_name").value;
    let p=document.getElementById("register_pass").value;
    let rp=document.getElementById("register_r_pass").value;

    if(p!=sanitizeHTML(p) || rp!=sanitizeHTML(rp) || username!=sanitizeHTML(username)){
        document.getElementById("register_name").innerHTML=sanitizeHTML(username);
        document.getElementById("register_pass").innerHTML=sanitizeHTML(p);
        document.getElementById("register_r_pass").innerHTML=sanitizeHTML(rp);
    }

}