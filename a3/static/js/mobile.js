// Flips nav-bar ON and OFF, mobile view
function flipMenu() {
    var m = document.getElementById("nav-menu");
    if (m.style.display === "block") {
        m.style.display = "none";
    } else {
        m.style.display = "block";
    }
}