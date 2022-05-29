
    function login(){
        let password_login =$("#password_login").val()
        let email_login = $("#email_login").val()
        let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();	
        if(password_login&&email_login) {

            var data = new FormData();  
            data.append("password",password_login)  
            data.append("email",email_login)  
            data.append("csrfmiddlewaretoken", csrf_token);
            $.ajax({
                url: '/polls/loginApi',
                method:'POST',
                data:data,
                cache: false,                                               //Upload files without caching
                processData:false,                                          //Do not serialize data
                contentType:false, 
                success: function (res) {
                    if(res===500) alert("Thông tin tài khoản không chính xác !")
                    else {
                        if(res[3]==="ADMIN") window.location.href="/polls/admin"
                        else if(res[3]==="TEACHER") window.location.href="/polls/"
                        else  alert("Tài khoản không có quyền truy cập !")
                        sessionStorage.setItem('userInfo', JSON.stringify(res))
                    }
                },
                error: function (res) {
                    console.log(res)
                // window.location.href="/polls/"
                }
            });
        }else alert("Nhập đầy đủ thông tin !")
}


(function ($) {
    "use strict";

    
    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit',function(){
        var check = true;
        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }
    
        
        return check;
    });

    

    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }
    
    

})(jQuery);