//upload user's photo

$(".photo-upload-input").change(function(){
    var e = document.createElement("div");
    $(e).attr("id", "photo-loading-div");
    var load = document.createElement("img");
    load.src = "/static/img/loading.gif";
    $(load).attr("id", "photo-loading-gif");
    $(e).html(load);
    $(".photo-upload").after(e);
    $.ajax({
        url:'/img/'+$('.photo-upload-input').attr('user-key'),
        data:new FormData($('.photo-upload')[0]),
        type:'POST',
        processData: false,
        contentType: false,
        datatype:'json',
        success: function(res) {
            $('.user-photo').attr('src','/img/'+res['img_key']+'?'+Date.now());
        },
        complete:function(){
            $("#photo-loading-div").remove();
        },
        timeout:5000,
    });
});
