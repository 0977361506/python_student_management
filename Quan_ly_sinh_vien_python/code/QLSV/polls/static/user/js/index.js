function filterLessonByDate(e){
    let dateFormat = convertDate($(e).val())
    console.log(dateFormat)
    $.ajax({
        url: '/polls/filterLessonByDateApi?date='+dateFormat,
        method:'GET',
        cache: false,                                               
        processData:false,                                         
        contentType:false, 
        success: function (res) {
            let rows = ``
            if(res.length>0){
                $( res ).each(function( index,value ) {
                    let dateStartConvert = convertDateTime(value[5])
                    let dateEndConvert = convertDateTime(value[6])
                    let row = `<div class="mix col-lg-3 col-md-4 col-sm-6 ">
                                    <a href="/polls/lesson/${value[7]}">
                                        <div class="course-item">
                                            <div class="course-thumb set-bg" style="background-image: url(/static/user/img/courses/1.jpg)">
                                            </div>
                                            <div class="course-info">
                                                <div class="course-text">
                                                    <h5 class="mb-3">${value[3]}</h5>
                                                    <h5 class="mb-3" style="color: #d82a4e;">Lớp: ${value[2]}</h5> 
                                                    <p>
                                                        <span>
                                                            Thời gian bắt đầu:
                                                        &nbsp;  ${dateStartConvert}
                                                        </span>
                                                        <br/>
                                                        <span>
                                                            Thời gian kết thúc:
                                                            &nbsp;   ${dateEndConvert}
                                                        </span>
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    </a>
                                </div>`;
                    rows+=row
                });
                $(".course-items-area").html(rows)
            }else {
                $(".course-items-area").html(`<p style="font-size: 32px;">Không có lịch học nào!</p>`)
            }
        },
        error: function (res) {
            console.log(res)
        // window.location.href="/polls/"
        }
    });
}

function convertDate(dateInput){
    let arrayElementTime = dateInput.split("-")
    return arrayElementTime[0]+"/"+arrayElementTime[1]+"/"+arrayElementTime[2];
}

function convertDateTime(datetime){
    dateConvert = new Date(datetime)
    var dateStr =
    ("00" + (dateConvert.getMonth() + 1)).slice(-2) + "/" +
    ("00" + dateConvert.getDate()).slice(-2) + "/" +
    dateConvert.getFullYear() + " " +
    ("00" + dateConvert.getHours()).slice(-2) + ":" +
    ("00" + dateConvert.getMinutes()).slice(-2)
    return dateStr
}