
console.log("TU")

fetch("/friendsimages").then(
    (e) => e.json()).then( e =>{
        console.log(e)
        document.getElementById("for_images").innerHTML+="<ul>"
        for(var x=0; x<e.length;x++){

            if(e[x]=="shared"){
                continue;
            }

            document.getElementById("for_images").innerHTML+='<li><a href="/image-friends/'+e[x]+'">'+e[x]+'</a></li>'
        }
        document.getElementById("for_images").innerHTML+="</ul>"
    }
)