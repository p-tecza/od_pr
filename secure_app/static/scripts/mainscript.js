var json_products;
var curr_json_products;

localStorage.setItem("logout_bool", "false");

const maxImagesOnPage=12;

function readJSON() {
    var rawFile = new XMLHttpRequest();
    var it = 0;

    rawFile.onreadystatechange = function () {
        if (rawFile.readyState === 4) {
            if (rawFile.status === 200 || rawFile.status == 0) {
                document.getElementById("av_products").innerHTML="";

                fetch('/fetch_json')
                    .then((response) => response.json())
                    .then((json) => {

                        for (var i = 0; i < json.length; i++) {

                            if(i>=maxImagesOnPage){
                                break;
                            }

                            pr = json[i].product_name;
                            qt = json[i].quantity;
                            ct = json[i].category;
                            im = json[i].image;
                            mn = json[i].price;
                            prepareImages(pr,im,mn);
                            
                            //innerHTML += "<li>" + pr + " | amount: "
                            //     + qt + " | category: " + ct + " | image: "+im+"</li>";
                            //document.getElementById(im).appendChild(imgDescription);

                        }

                        console.log("druknij");
                        console.log(json.length + "<- dlugosc jsona");
                        json_products = json;
                        curr_json_products = json_products;
                        console.log("TU JEST JSON PROD: ");
                        console.log(json_products);

                        console.log(typeof (json));

                        for (x in json) {
                            console.log("ok: " + x);
                        }

                    });
            }
        }
    }
    rawFile.open("GET", "fetch_json");
    rawFile.send();
}

function changeProductContentText() {
    var searchValText = document.getElementById("search_product").value;
    var searchValSelect = document.getElementById("select_product").value;

    if (searchValSelect == "any") searchValSelect = "";

    document.getElementById("av_products").innerHTML = "";

    var wysw = json_products.filter(x => x.product_name.includes(searchValText));
    wysw = wysw.filter(x => x.category.includes(searchValSelect));

    curr_json_products = wysw;

    console.log("WYSW = ");
    console.log(wysw);


    for (var i = 0; i < wysw.length; i++) {

        if(i>=maxImagesOnPage){
            break;
        }

        pr = wysw[i].product_name
        qt = wysw[i].quantity
        ct = wysw[i].category
        im = wysw[i].image;
        mn = wysw[i].price;

        prepareImages(pr,im,mn);

        // document.getElementById("av_products").innerHTML += "<li>" + pr + " | amount: "
        //     + qt + " | category: " + ct + " | image: "+im+"</li>";
    }

}

function changeProductContentSelect() {
    var searchValText = document.getElementById("search_product").value;
    var searchValSelect = document.getElementById("select_product").value;
    if (searchValSelect == "any") searchValSelect = "";

    document.getElementById("av_products").innerHTML = "";

    var wysw = json_products.filter(x => x.product_name.includes(searchValText));
    wysw = wysw.filter(x => x.category.includes(searchValSelect));


    for (var i = 0; i < wysw.length; i++) {

        if(i>=maxImagesOnPage){
            break;
        }

        pr = wysw[i].product_name
        qt = wysw[i].quantity
        ct = wysw[i].category
        im = wysw[i].image;
        mn = wysw[i].price;

        prepareImages(pr,im,mn);

        // document.getElementById("av_products").innerHTML += "<li>" + pr + " | amount: "
        //     + qt + " | category: " + ct + " | image: "+im+"</li>";
    }

}

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


readJSON();


function set_output(text) {
    output = document.getElementById("sse_test")
  
    if (!output) {
      output = document.createElement("span")
      output.setAttribute("id", "sse_test")
      document.body.appendChild(output)
    }
  
    output.innerText = text
  }

async function subscribe() {

    var noVisitorsVar='0';

    console.log("wys");

    const params = {
        noVisitors:noVisitorsVar
    };

    let response = await fetch("/subscribe", {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(params),
        cache: "no-cache",
        headers: new Headers({
          "content-type": "application/json"
        })
      });
  
    if (response.status == 502) {
      // Status 502 is a connection timeout error,
      // may happen when the connection was pending for too long,
      // and the remote server or a proxy closed it
      // let's reconnect
      await subscribe();
    } else if (response.status != 200) {
      // An error - let's show it
      set_output(response.statusText);
      // Reconnect in one second
      await new Promise(resolve => setTimeout(resolve, 3000));
      await subscribe();
    } else {
      // Get and show the message
      let message = await response.text();
      set_output("no. entries: "+message);
      noVisitorsVar=message;
      // Call subscribe() again to get the next message
      await new Promise(resolve => setTimeout(resolve, 3000));
      await subscribe();
    }
  }
  subscribe();

function prepareImages(pr,im,mn){
    var imgDiv = document.createElement("div");
    imgDiv.setAttribute("id","div_"+im);
    imgDiv.classList.add("product_div");

    var img = document.createElement("img");
    img.src="get_image/"+im;
    console.log(img.src);
    img.classList.add('product_image')
    img.setAttribute("id",im)

    pr_short=String(pr).substring(0,10);

    var imgDescription = document.createElement("p");
    imgDescription.innerHTML= pr_short + "...|" + mn
    imgDescription.title=pr+" | "+mn;

    imgDiv.appendChild(img);
    imgDiv.appendChild(imgDescription);

    document.getElementById("av_products").appendChild(imgDiv);
}