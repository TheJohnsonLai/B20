var request_box = document.getElementById("my_request_box");
var close = document.getElementById("close_box");
var area = document.getElementById("remark_area");

// Flips nav-bar ON and OFF, mobile view
function flipMenu() {
    var m = document.getElementById("nav-menu");
    var h = document.getElementById("hidden-header");
    // Style can start as NULL
    if (m.style.display != "none") {
        m.style.display = "none";
        h.style.display = "block";
    } else {
        m.style.display = "block";
        h.style.display = "none";
    }
}

//initiate content's top margin 
var heading_height = document.getElementById("bar").clientHeight
var content = document.getElementsByClassName("content")[0]
var w = window.innerWidth;

var marginOfContent = heading_height + (w*0.01)
content.style.marginTop = marginOfContent + "px";

//change content's top margin as screen size change
function changeMargin() {
    var heading_height = document.getElementById("bar").clientHeight
    var content = document.getElementsByClassName("content")[0]
    var w = window.innerWidth;
    
    var marginOfContent = heading_height + (w*0.02)
    content.style.marginTop = marginOfContent + "px";
}

//close remark request
close.onclick = function() {
    request_box.style.display = "none";
}

//open remark request and change heading acording to the button
function clicked(clicked_but){
    const click = clicked_but.target;
    request_box.style.display = "block";
    document.getElementById("title").innerHTML = `Request For Remark ${click.id}`;
    area.setAttribute("value",`${click.id}`);
}

document.querySelectorAll('button').forEach(button => button.addEventListener('click', clicked));
window.addEventListener("resize", changeMargin);