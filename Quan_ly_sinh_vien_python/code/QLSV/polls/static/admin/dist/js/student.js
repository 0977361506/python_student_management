function register(){
    let username =  $("#username").val()
    let password=$("#password").val()
    let email = $("#email").val()
    let phone=$("#phone").val()
    let address = $("#address").val()
    let fullname=($("#fullname").val())?$("#fullname").val():username
    let codeStudent =  $("#codeStudent").val()
    var image = ($("#avatar").get(0).files[0])?$("#avatar").get(0).files[0].name :"2.jpg"
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();	
    console.log(username+"-"+password+"-"+email+"-"+csrf_token+"-"+phone+"-"+address)
    if(checkLogin(email,username,password)) {
        var data = new FormData();  
        data.append("username",username)  
        data.append("password",password)  
        data.append("email",email)  
        data.append("image",image)  
        data.append("fullname",fullname) 
        data.append("phone",phone)  
        data.append("address",address) 
    	data.append("csrfmiddlewaretoken", csrf_token);
        data.append("codeStudent",codeStudent)
        $.ajax({
            url: '/polls/registerStudentApi',
            method:'Post',
            // headers: { "X-CSRFToken": getCookie("csrftoken") },
            data:data,
            cache: false,                                            
            processData:false,                                       
            contentType:false, 
            success: function (res) {
                alert("Thêm mới thành công !")
                location.reload()
            },
                error: function (res) {
                console.log(res)
            }
        });
    }
}

function editStudent(){
    let idStudent = $("#idStudent_").val()
    let idUser = $("#idUser_").val()
    let username =  $("#username_edit").val()
    // let password=$("#password_edit").val()
    let email = $("#email_edit").val()
    let phone=$("#phone_edit").val()
    let address = $("#address_edit").val()
    let fullname=($("#fullname_edit").val())?$("#fullname_edit").val():username
    let codeStudent =  $("#codeStudent_edit").val()
    var image = ($("#avatar_edit").get(0).files[0])?$("#avatar_edit").get(0).files[0].name :"2.jpg"
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();	
    if(checkLogin(email,username,password)) {
        var data = new FormData();  
        data.append("username",username)  
        // data.append("password",password)  
        data.append("email",email)  
        data.append("image",image)  
        data.append("fullname",fullname) 
        data.append("phone",phone)  
        data.append("address",address) 
        data.append("idStudent",idStudent)  
        data.append("idUser",idUser) 
    	data.append("csrfmiddlewaretoken", csrf_token);
        data.append("codeStudent",codeStudent)
        $.ajax({
            url: '/polls/editStudentApi',
            method:'Post',
            // headers: { "X-CSRFToken": getCookie("csrftoken") },
            data:data,
            cache: false,                                            
            processData:false,                                       
            contentType:false, 
            success: function (res) {
                alert("Cập nhật thông tin thành công !")
                location.reload()
            },
                error: function (res) {
                console.log(res)
            }
        });
    }
}


function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }
function checkLogin(email,username,password){
   if(username && password && email) {
        $("#username").css("border","1px solid  #ced4da") ; 
        $("#email").css("border","1px solid  #ced4da") ; 
        $("#password").css("border","1px solid  #ced4da") ; 
        return true ;
   }else{
    // $("#username").css("border","1px solid red")
    // $("#email").css("border","1px solid red");
    // $("#password").css("border","1px solid red");
        if(username)    $("#username").css("border","1px solid #ced4da")
        else {
            $("#username").css("border","1px solid red") ; 
        }

        if(email)  $("#email").css("border","1px solid #ced4da")
        else {
            $("#email").css("border","1px solid red")
        }

        if(password) $("#password").css("border","1px solid #ced4da")
        else {
            $ ("#password").css("border","1px solid red")
            
        }
        return false
   }
}

function uploadAvatar(nameImage,nameAppendImage){
    var f_obj = $(nameImage).get(0).files[0];
    // console.log("File object:",f_obj);
    // console.log("The file name is:",f_obj.name);
    // console.log("The file size is:",f_obj.size);
    var data = new FormData();                                      //Create formdata objects to facilitate file transfer to the back end
    data.append("file",f_obj)                                        //To add (encapsulate) a file object to a formdata object
	let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();				
	console.log(csrf_token);				
	data.append("csrfmiddlewaretoken", csrf_token);
    $.ajax({
        url:'/polls/uploadFileApi',
        type:'POST',
        data:data,
        cache: false,                                               //Upload files without caching
        processData:false,                                          //Do not serialize data
        contentType:false, 
        // enctype: 'multipart/form-data',
        // beforeSend: function (xhr) {
        //     xhr.setRequestHeader('X-CSRFToken', '{{csrf_token}}');
        // },                                         //No special connection type defined
        success:function (res ) {
            $(nameAppendImage).attr("src",res)
            console.log(res)
        },
        error: function (res) {
            console.log(res)
        }
    })
 
}

function showDetailStudent(e){
    let idStudent = $(e).attr("idStudent")
    let idUser = $(e).attr("idUser")
    $.ajax({
        url:'/polls/detailStudentApi?idUser='+idUser+"&idStudent="+idStudent,
        type:'GET',
        cache: false,                                         
        processData:false,                                     
        contentType:false, 
        success:function (res ) {
            console.log(res)
            $("#username_edit").val(res[0])
            $("#email_edit").val(res[2])
            $("#phone_edit").val(res[4])
            $("#address_edit").val(res[5])
            $("#fullname_edit").val(res[1])
            $("#codeStudent_edit").val(res[6])
            $("#idStudent_").val(res[7])
            $("#idUser_").val(res[8])
            $(".img_upload_edit").attr("src","/static/"+res[3])
            $("#editStudent").modal("show")
        },
        error: function (res) {
            console.log(res)
        }
    })
}
