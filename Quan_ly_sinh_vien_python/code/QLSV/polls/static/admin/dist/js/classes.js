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

function addLesson(){
    let timeStart=$("#timeStart").val()
    let timeEnd=$("#timeEnd").val()
    let teacher=$("#teacher").val()
    let subject=$("#subject").val()
    let classes=$("#classes").val()
    let listIdStudent = getListIdStudent()
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();	
    if(vadidateAddLesson(timeStart,timeEnd,teacher,subject,classes)){
        if(vadidateTime(timeStart,timeEnd)){
           if(listIdStudent.length>0){
                var data = new FormData();  
                // data.append("timeStart",convertToDatetimeLocal(new Date(timeStart)))  
                // data.append("timeEnd",convertToDatetimeLocal(new Date(timeEnd))) 
                data.append("timeStart",timeStart)  
                data.append("timeEnd",timeEnd)   
                data.append("teacher",teacher) 
                data.append("subject",subject)  
                data.append("classes",classes) 
                data.append("listIdStudent",listIdStudent) 
                data.append("csrfmiddlewaretoken", csrf_token);
                for (var pair of data.entries()) {
                    console.log(pair[0]+ ', ' + pair[1]); 
                }
                $.ajax({
                    url: '/polls/addNewLessonApi',
                    method:'Post',
                    data:data,
                    cache: false,                                            
                    processData:false,                                       
                    contentType:false, 
                    success: function (res) {
                        if(res=="500") alert("Thêm mới thất bại!")
                        else alert("Thêm tiết học thành công !")
                        location.reload()
                    },
                        error: function (res) {
                        console.log(res)
                    }
                });
           }else alert("Vui lòng thêm sinh viên vào tiết học!")
        }else {
            alert("Thời gian bắt đầu phải nhỏ hơn thời gian kết thúc !")
        }
    }
}

function vadidateAddLesson(timeStart,timeEnd,teacher,subject,classes){
    if(timeStart && timeEnd && teacher!=0 && subject!=0 && classes!=0) {
         $("#timeStart").css("border","1px solid  #ced4da") ; 
         $("#timeEnd").css("border","1px solid  #ced4da") ; 
         $("#teacher").css("border","1px solid  #ced4da") ; 
         $("#subject").css("border","1px solid  #ced4da") ; 
         $("#classes").css("border","1px solid  #ced4da") ; 
         return true ;
    }else{
         if(timeStart)    $("#timeStart").css("border","1px solid #ced4da")
         else {
             $("#timeStart").css("border","1px solid red") ; 
         }
 
         if(timeEnd)  $("#timeEnd").css("border","1px solid #ced4da")
         else {
             $("#timeEnd").css("border","1px solid red")
         }
 
         if(teacher!=0) $("#teacher").css("border","1px solid #ced4da")
         else {
             $ ("#teacher").css("border","1px solid red")
         }

         if(subject!=0) $("#subject").css("border","1px solid #ced4da")
         else {
             $ ("#subject").css("border","1px solid red")
             
         }

         if(classes!=0) $("#classes").css("border","1px solid #ced4da")
         else {
             $ ("#classes").css("border","1px solid red")
             
         }
         return false
    }
 }

function vadidateTime(timeStart,timeEnd){
    var dateStart = new Date(timeStart);
    var dateEnd = new Date(timeEnd);
    return (dateStart<dateEnd)
}

function convertToDatetimeLocal(time){  // example : 2022-05-27 05:14:07
    var dateStr =
    ("00" + (time.getFullYear() + 1)).slice(-2) + "-" +
    ("00" + time.getMonth()).slice(-2) + "-" +
    time.getDate() + " " +
    ("00" + time.getHours()).slice(-2) + ":" +
    ("00" + time.getMinutes()).slice(-2) + ":" +
    ("00" + time.getSeconds()).slice(-2);
    return dateStr ;
}

function getListIdStudent(){
    var selected = [];
    $('input.cb-element:checked').each(function() {
        selected.push($(this).attr('id'));
    });
    return selected;
}

function filterByDate(e){
    timeSelect = $(e).val()
    classtimeVadidate = $(e).attr("classtimeVadidate")
    timeVadidate=$(classtimeVadidate).val()
    if(timeVadidate){
        $(classtimeVadidate).css("border","1px solid #ced4da")
        $(e).css("border","1px solid #ced4da")
        let timeStart = convertToDatetimeLocal(new Date($("#timeStart").val()))
        let timeEnd = convertToDatetimeLocal(new Date($("#timeEnd").val()))
        $.ajax({
            url:'/polls/getIdTeacherAndIdClassByDateApi?timeStart='+timeStart+"&timeEnd="+timeEnd,
            method:'get',
            dataType: 'json',
            contentType: "application/json",
            success:function (res ) {
                let listClasses = `<option value="0">- Chọn lớp học -</option>`
                let listTeachers = `<option value="0">- Chọn giáo viên -</option>`
                $(res.listClass).each(function(i,v) {
                    let listClassEle  =`<option value="${v[0]}">${v[1]}</option>` 
                    listClasses+=listClassEle
                });
                $(res.listTeacher).each(function(i,v) {
                    let ele  =`<option value="${v[0]}">${v[1]}</option>` 
                    listTeachers+=ele
                });
                $("#classes").html(listClasses)
                $("#teacher").html(listTeachers)
            },
            error: function (res) {
                console.log(res)
            }
        })
    }
    else {
        $(classtimeVadidate).css("border","1px solid red")
    }
}