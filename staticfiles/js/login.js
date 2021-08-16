function ajax_call(type, url, data, success_function){
    $.ajax({
      type: type,
      url: url,
      headers: {'X-CSRFToken': getCookie('csrftoken')},
      data: data,
      dataType: 'json',
      success: success_function,
    });
}

// Submitting Login Form
$(function(){
    $('#login_form').bind('submit', function(e){
        e.preventDefault();
        let email = $('#login_email').val();
        let password = $('#login_password').val();
        ajax_call("POST", "/user-login", {'email': email, 'password': password}, login_response);
    });
});

function login_response(response){
    if(response.data == "success"){
          window.location = window.location;
    }
    else {
        document.getElementById('display_error').innerHTML = `<div class="alert alert-danger alert-dismissible fade show mt-2" role="alert">
              ${response.data}
              <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`;
    }
}

// Signup Function
$(function(){
    $('#signup_form').bind('submit', function(e){
        e.preventDefault();
        var data = {"username": $('#username').val(),
                    "email": $('#email').val(),
                    "password": $('#password1').val(),
                    "confirm_password": $('#password2').val(),
                   };
        ajax_call("POST", "/signup", data, signup_response);
    });
});

function signup_response(response){
    if (response.success){
        $('#modalSignup').modal('hide');
        document.getElementById('display_error').innerHTML = `<div class="alert alert-success alert-dismissible fade show mt-2" role="alert">
              Successfully Signup
              <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`;
        $('#modalSignin').modal('show');
    }
    else{
        json_error = JSON.parse(response);
        for (let resp in json_error){
            var x = document.getElementById(resp);
            setError(x, json_error[resp][0]['message']);
        }
    }
}

// Forgot Password
$('#btn_forgot_password').click(function(){
    var username = document.getElementById('login_email');
    if(username.value == null || username.value == ""){
        setError(username, "Please enter your username");
    }
    else{
        ajax_call("POST", "/forgot-password", {'username': username.value}, forgotPasswordResp);
    }
});

function forgotPasswordResp(response){
    if(response.error){
        var field = document.getElementById("login_email");
        setError(field, response.error);
    }
    else{
        $('#modalSignin').modal('hide');
        $('#otp_key').val(response.key);
        $('#modalForgotPassword').modal('show');
    }
}

$('#VerifyOtpForm').bind('submit', function(e){
    e.preventDefault();
    var data = {
        "otp": this.otp_num.value,
        "otp_key": this.otp_key.value,
        "new_password1": this.new_password1.value,
        "new_password2": this.new_password2.value,
    }
    ajax_call("POST", "/verify-otp", data, otpResponse)
});

function otpResponse(response){
    if(response.error){
        json_err = JSON.parse(response.error)
        for(let err in json_err){
            var field = document.getElementById(err);
            let err_msg = json_err[err][0]['message'];
            setError(field, err_msg);
        }
    }
    else if(response.otp){
        let field = document.getElementById("otp_num");
        let err_msg = "Invalid otp number.";
        setError(field, err_msg);
    }
    else{
        $('#modalForgotPassword').modal('hide');
        document.getElementById('display_error').innerHTML = `<div class="alert alert-success alert-dismissible fade show mt-2" role="alert">
              Password reset successfully.
              <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`;
        $('#modalSignin').modal('show');
    }
}

function setError(field, message){
    field.classList.add('error');
    field.parentNode.querySelector('small').innerHTML = message;
    field.setAttribute('onclick', 'removeError(this)');
}

function removeError(textField){
     textField.classList.remove('error');
     textField.parentNode.querySelector('small').innerText = "";
     textField.removeAttribute('onclick');
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//Profile Edit
$("#btn_edit").click(function(){
    let form = $('#ProfileForm');
    let input_fields = form.find('.form-control');
    console.log(input_fields.length);
    for(let field=0; field<input_fields.length;field++){
        if(input_fields[field].hasAttribute('disabled')){
            input_fields[field].removeAttribute('disabled');
        }
    }
    $(this).hide();
    $('#btn_profile_submit').removeAttr('hidden');
});