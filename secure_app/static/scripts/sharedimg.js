
console.log("TU")

fetch("/sharedimages").then(
    (e) => e.json()).then( e =>{
        console.log(e)
        document.getElementById("for_images").innerHTML+="<ul>"
        for(var x=0; x<e.length;x++){

            if(e[x]=="shared"){
                continue;
            }

            document.getElementById("for_images").innerHTML+='<li><a href="/image-shared/'+e[x]+'">'+e[x]+'</a></li>'
        }
        document.getElementById("for_images").innerHTML+="</ul>"
    }
)