function registerClasses(){
    let name =  $("#name").val()
    let description=$("#description").val()
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();	
    if(name) {
        var data = new FormData();  
        data.append("name",name)  
        data.append("description",description)  
    	data.append("csrfmiddlewaretoken", csrf_token);
        $.ajax({
            url: '/polls/registerClassesApi',
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
    }else alert("Tên lớp học không được bỏ trống !")
}

function editClasses(){
    let idClass =  $("#idClass_").val()
    let name =  $("#name_edit").val()
    let description = $("#description_edit").val()
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();	
    if(name) {
        var data = new FormData();  
        data.append("name",name)  
        data.append("description",description)  
        data.append("idClass",idClass)  
    	data.append("csrfmiddlewaretoken", csrf_token);
        $.ajax({
            url: '/polls/editClassesApi',
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
    }else alert("Tên lớp học không được bỏ trống !")
}


function showDetailClasses(e){
    let idClass = $(e).attr("idClass")
    $.ajax({
        url:'/polls/detailClassesApi?idClass='+idClass,
        type:'GET',
        cache: false,                                         
        processData:false,                                     
        contentType:false, 
        success:function (res ) {
            console.log(res)
            $("#name_edit").val(res[0])
            $("#description_edit").val(res[1])
            $("#idClass_").val(res[2])
            $("#editClasses").modal("show")
        },
        error: function (res) {
            console.log(res)
        }
    })
}
