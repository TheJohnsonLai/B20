var request_box = document.getElementById("my_request_box");
var close = document.getElementById("close_box");
var area = document.getElementById("remark_area");
var feedBack = document.getElementById("AnonymousFeedback");
var MarksRemarkRequest = document.getElementById("MarksRemarkRequest");

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

//switch subtabs
var myFeedBack = document.getElementById("myFeedback");
var mark = document.getElementById("gride-container");
MarksRemarkRequest.onclick = function() {
    myFeedBack.style.display = "none";
    mark.style.display = "grid";
    //mark
    MarksRemarkRequest.style.border = "1.5px solid rgb(19, 40, 85)";
    MarksRemarkRequest.style.borderBottom = "none";
    MarksRemarkRequest.style.borderRadius = "6px";
    MarksRemarkRequest.style.borderBottomLeftRadius = "0px";
    MarksRemarkRequest.style.borderBottomRightRadius = "0px";
    MarksRemarkRequest.style.backgroundColor = "rgb(19, 40, 85)";
    MarksRemarkRequest.style.color = "white";

    //feedback
    feedBack.style.border = "none";
    feedBack.style.borderBottom = "none";
    feedBack.style.borderRadius = "none";
    feedBack.style.borderBottomLeftRadius = "none";
    feedBack.style.borderBottomRightRadius = "none";
    feedBack.style.backgroundColor = "rgb(220, 229, 238)";
    feedBack.style.color = "rgb(19, 40, 85)";
}
feedBack.onclick = function() {
    mark.style.display = "none";
    myFeedBack.style.display = "block";
    //feedback
    feedBack.style.border = "1.5px solid rgb(19, 40, 85)";
    feedBack.style.borderBottom = "none";
    feedBack.style.borderRadius = "6px";
    feedBack.style.borderBottomLeftRadius = "0px";
    feedBack.style.borderBottomRightRadius = "0px";
    feedBack.style.backgroundColor = "rgb(19, 40, 85)";
    feedBack.style.color = "white";

    //mark
    MarksRemarkRequest.style.border = "none";
    MarksRemarkRequest.style.borderBottom = "none";
    MarksRemarkRequest.style.borderRadius = "none";
    MarksRemarkRequest.style.borderBottomLeftRadius = "none";
    MarksRemarkRequest.style.borderBottomRightRadius = "none";
    MarksRemarkRequest.style.backgroundColor = "rgb(220, 229, 238)";
    MarksRemarkRequest.style.color = "rgb(19, 40, 85)";
}


//close remark request
close.onclick = function() {
    request_box.style.animation = "close 1s";
    setTimeout(function(){
        request_box.style.display = "none";
        request_box.style.animation = "none";
    }, 1000);
}

//open remark request and change heading acording to the button
function clicked(clicked_but){
    const click = clicked_but.target;
    request_box.style.display = "block";
    request_box.style.animation = "open 1.5s";
    document.getElementById("title").innerHTML = `Request For Remark ${click.id}`;
    area.setAttribute("value",`${click.id}`);
}

//check submission
document.getElementById("remark_request").onsubmit = function (event) {
    if (!confirm("Click OK To Submit")) {
        event.preventDefault();
    }
}
document.getElementById("feedback_form").onsubmit = function (event) {
    if (!confirm("Click OK To Submit")) {
        event.preventDefault();
    }
}

//loop through instructor and put them as chioces
instructorList = JSON.parse(instructorList);
for(key in instructorList){
    document.getElementById('instructor').innerHTML += '<option class="choice" value="">' + instructorList[key].FNAME + " " + instructorList[key].LNAME+ "-" + instructorList[key].UTORID + '</option>';
}
for(key in instructorList){
    document.getElementsByClassName('choice')[key].setAttribute("value",instructorList[key].UTORID);
}
document.querySelectorAll('.grid-container').forEach(button => button.addEventListener('click', clicked));
window.addEventListener("resize", changeMargin);