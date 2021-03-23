var request_box = document.getElementById("my_request_box");
var close = document.getElementById("close_box");

close.onclick = function() {
    request_box.style.display = "none";
}

function clicked(clicked_but){
    const click = clicked_but.target;
    request_box.style.display = "block";
    document.getElementById("title").innerHTML = `REQUEST FOR REMARK ${click.id}`;
}

document.querySelectorAll('button').forEach(button => button.addEventListener('click', clicked));