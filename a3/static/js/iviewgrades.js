// Grades Validator
function validateGrade() {
    var input = document.querySelector("#num-val").value;
    var exam = document.querySelector("#list-examname").value;
    var id = document.querySelector("#list-utorid").value;
    if (input < 0 || input > 100) {
        alert("marks must be between 0 - 100");
        return false;
    } else if (input == "") {        
        alert("please enter a value");
        return false;
    }
    if(exam == "--"){  
        alert("please select an assignment or test");
        return false;
    }
    if(id == "--"){  
        alert("please select a student id");
        return false;
    }
    alert("Marks updated");
    return true;
}
