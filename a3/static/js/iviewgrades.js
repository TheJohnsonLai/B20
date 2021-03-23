// Grades Validator
function myfunction() {
    var input = document.querySelector("#num-val").value;
    if (input < 0 || input > 100) {
        alert("marks must be between 0 - 100");
        return false;
    } else if (input == "") {        
        alert("please enter a value");
        return false;
    }
    alert("Marks updated");
    return true;
}
