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
        window.location = window.location;
    }
    else{
        json_error = JSON.parse(response)
        for (let resp in json_error){
            var x = document.getElementById(resp).parentNode;
            x.querySelector('small').innerHTML = json_error[resp][0]['message'];
        }
    }
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
