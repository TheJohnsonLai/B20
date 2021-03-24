var request_box = document.getElementById("my_request_box");
var close = document.getElementById("close_box");
var area = document.getElementById("remark_area");

close.onclick = function() {
    request_box.style.display = "none";
}

function clicked(clicked_but){
    const click = clicked_but.target;
    request_box.style.display = "block";
    document.getElementById("title").innerHTML = `Request For Remark ${click.id}`;
    area.setAttribute("value",`${click.id}`);
}

document.querySelectorAll('button').forEach(button => button.addEventListener('click', clicked));