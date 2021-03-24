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