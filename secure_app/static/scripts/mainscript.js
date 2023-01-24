
//flaskAddress="http://127.0.0.1:5678"; //DLA NIE SSL (http)
flaskAddress="https://127.0.0.1:5678"; //DLA SSL (docker glownie) (https)

function showUserContent() {
    document.getElementById("dropdownUserContent").style.display = "block";
    document.getElementById("dropdownUserContent2").style.display = "block";
}

window.onclick = function (event) {
    if (!event.target.matches('#dropdownUserContent')) {
        if (!event.target.matches('#viewdropdown')) {
            document.getElementById("dropdownUserContent").style.display = "none";
            document.getElementById("dropdownUserContent2").style.display = "none";
        }
    }
}

function logoutFunction() {
    document.getElementById("dropdownUserContent").style.display = "none";
    document.getElementById("dropdownUserContent2").style.display = "none";
    console.log("lgout");

    localStorage.setItem("logout_bool", "true");

    const logoutAjax = new XMLHttpRequest();

    logoutAjax.onload = function () {
        redirectSite = this.responseText;
        window.location.replace("http://" + redirectSite);
        document.getElementById("logout_success_info").innerHTML = "logout successful.";
        console.log(redirectSite);
        console.log("dzilam");
        logout_bool = true;
        window.glob = "test";

    }

    logoutAjax.open("GET", "logout");
    logoutAjax.send();

}

function renderSettings(){
    window.location.replace(flaskAddress+"/settings");
}

function showThis(){
    var x = document.getElementById("hiddenCode").hidden;
    console.log(x)
  if (x == true) {
    document.getElementById("hiddenCode").hidden = false;
  } else {
    document.getElementById("hiddenCode").hidden = true;
  }
}

function showOptions(){

    var x = document.getElementById("sharing_select").hidden;

    if (x == true) {
        document.getElementById("sharing_select").hidden = false;
      } else {
        document.getElementById("sharing_select").hidden = true;
      }

}

function logoutFunction(){
  window.location.reload()
}


// function friendsInput(){

//     var x = document.getElementById("friends_input").hidden;

//     if (x == true) {
//         document.getElementById("friends_input").hidden = false;
//         document.getElementById("friends_info").hidden = false;
//       } else {
//         document.getElementById("friends_input").hidden = true;
//         document.getElementById("friends_info").hidden = true;
//       }

// }