

function showUserContent() {
    console.log("dz");
    document.getElementById("dropdownUserContent").style.display = "block";
}

window.onclick = function (event) {
    if (!event.target.matches('#dropdownUserContent')) {
        if (!event.target.matches('#viewdropdown')) {
            console.log("oob");
            document.getElementById("dropdownUserContent").style.display = "none";
        }
    }
}

function logoutFunction() {
    document.getElementById("dropdownUserContent").style.display = "none";
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
