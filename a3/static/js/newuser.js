function validateForm(){
    var a = document.forms["newuser-form"]["fname"].value;
    var b = document.forms["newuser-form"]["lname"].value;
    var c = document.forms["newuser-form"]["utorid"].value;
    var d = document.forms["newuser-form"]["username"].value;
    var e = document.forms["newuser-form"]["password"].value;
    var f = document.forms["newuser-form"]["password-check"].value;
    if (a==null || a==""){
        alert("Please enter your first name.");
        return false;
    }
    else if (b==null || b==""){
        alert("Please enter your last name.");
        return false;
    }
    else if (c==null || c==""){
        alert("Please enter your UTORid.");
        return false;
    }
    else if (c != parseInt(c)) {
        alert("UTORid should be an integer");
        return false;
    }
    else if (d==null || d==""){
        alert("Please enter a username.");
        return false;
    }
    else if (e==null || e==""){
        alert("Please enter a password.");
        return false;
    }
    else if (f==null || f==""){
        alert("Please verify your password.");
        return false;
    }
    else if (!(f===e)){
        alert("Your password and confirmation password do not match.");
        return false;
    }
}
