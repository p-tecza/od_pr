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

        if(p!=rp){
            document.getElementById("register_r_pass").style.backgroundColor="#FBB2B2";
            document.getElementById("login_button").disabled=true;
            document.getElementById("error_message").innerHTML="passwords not equal.";
        }else{
            document.getElementById("register_r_pass").style.backgroundColor="#FFFFFF";
            document.getElementById("login_button").disabled=false;
            document.getElementById("error_message").innerHTML="";
        }

    }

}