function validateForm() {
    var x = document.forms["login-form"]["username"].value;
    if (x==null || x=="") {
        alert("Please enter your username");
        return false;
    }
    var y = document.forms["login-form"]["password"].value;
    if (y==null || y=="") {
        alert("Please enter your password");
        return false;
    }
}