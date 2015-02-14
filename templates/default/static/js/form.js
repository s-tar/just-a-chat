/**
 * Created by mr.S on 18.09.14.
 */
$(document).ready(function(){
    var processing = false;
    if(typeof(tinymce) != "undefined")
        tinymce.init({
            selector: ".editor",
            language : 'ru',
            plugins: [
                "advlist autolink lists link image charmap print preview anchor",
                "searchreplace visualblocks code fullscreen",
                "insertdatetime media table contextmenu paste"
            ],
            setup: function (editor) {
                editor.on('change', function () {
                    tinymce.triggerSave();
                });
            },
            toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image"
        });
});
$(document).on("click", "input.submit, button.submit", function(){
    if($(this).attr('processing') == "true")return;
    $(this).attr('processing', "true");
    $(this).closest("form").submit();
});

$(document).on("submit", "form.ajax", function(e){
    e.preventDefault();
});

$(document).on("ajax_submit", "form", function(e, cb){
    var formData = new FormData($(this)[0]);
    var url = $(this).attr("action");
    var method = $(this).attr("method");
    var _this = $(this);
    $.ajax({
        url: url,
        type: method,
        data: formData,
        async: false,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            if(response.status == "fail"){
                _this.find(".submit").attr("processing", "");
            }
            if(typeof(cb) == 'function')cb(response);
        }
    });
    e.preventDefault();
    return false;
});

$(document).on("submit", "form.ajax_submit", function(e){
var form = $(this);
form.trigger("ajax_submit", function(response){
    if(response.status == 'ok') {
        if(!!response.redirect)
            window.location.href=response.redirect
        else if(!!response.reload)
            window.location.reload()
    }else if(response.status == 'fail') {
        showErrors(form, response.errors);
    }
})
e.preventDefault();
return false;
});
function showErrors(form , errors) {
    $(form).find(".error").remove();
    for(key in errors){
        if (errors.hasOwnProperty(key)) {
            $(form).find("[name='"+key+"']").each(function(i){
                if(!!errors[key][i]){
                    var error = $('<span class="error"><div class="text">'+errors[key][i][0]['message']+'</div></span>');
                    $(this).after(error);
                    error.css("display", "block")
                    var text = error.find(".text");
                    if(error.find(".text").outerWidth() > $(this).outerWidth()){
                        text.css("white-space", "normal");
                        text.outerWidth($(this).outerWidth());
                    }
                    error.css("display", "none")
                    $(this).change(function(){
                        error.fadeOut();
                    })
                    $(this).focus(function(){
                        error.css('opacity','0.3')
                    });
                    $(this).blur(function(){
                        error.css('opacity','')
                    })
                    error.fadeIn();
                }

            });

        }
    }
}


//$(document).on('keydown', 'textarea.autoresize', function (e){
//    $(this).css("height","");
//    var height = $(this).height();
//    if(e.which == 13) {
//        $(this).css("padding-top",'1.145em')
//    }
//    var fontSize = $(this).css('font-size');
//    var lineHeight = Math.floor(parseInt(fontSize.replace('px','')) * 1.5);
//    var new_height = this.scrollHeight - lineHeight;
//    new_height = (new_height > height) ? new_height : height;
//    $(this).height(new_height);
//});
//
//
//$(document).on('keyup', 'textarea.autoresize', function (e){
//    $(this).css("height","");
//    var height = $(this).height();
//    var maxheight = parseInt($(this).css('max-height').replace("px", ""));
//
//    if(e.which == 13) {
//        $(this).css("padding-top",'')
//    }
//    var fontSize = $(this).css('font-size');
//    var lineHeight = Math.floor(parseInt(fontSize.replace('px','')) * 1.5);
//    var new_height = this.scrollHeight - lineHeight;
//    new_height = (new_height > height) ? new_height : height;
//    $(this).height(new_height);
//    if(new_height > maxheight)
//        $(this).css('overflow-y', 'scroll');
//    else
//        $(this).css('overflow-y', '');
//    popup.center();
//});

$(document).on('keydown keyup change', 'input, textarea', function (e){
    $(this).removeClass('has-value');
    if($(this).val() != "")
        $(this).addClass('has-value');
});

$(document).ready(function(){
    autosize_reinit()
//    $('textarea.autoresize:not(.noinit)').keydown();
});

function preview(input, cb) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            if(typeof(cb) == "function") cb(e.target.result)
        }

        reader.readAsDataURL(input.files[0]);
    }
}

function preview(input, cb) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            if(typeof(cb) == "function") cb(e.target.result)
        }

        reader.readAsDataURL(input.files[0]);
    }
}
$(document).on("change", ".image-loader input[type=file]", function(){
    var container = $(this).closest(".image-loader");
    container.addClass("loading");
    if($(this).val() == ''){
        container.removeClass("loading");
        container.removeClass("has-image");
        container.find(".source").css("background-image", "none");
    } else {

        preview(this, function(src){
            container.removeClass("loading");
            container.addClass("has-image");
            container.find(".source").css("background-image", "url('"+src+"')");
        });
    }
});

function autosize_reinit(){
    $('textarea.autoresize').autosize()
}

$(document).on('click', '.dropdown-list > .current', function(){
    var dropdown = $(this).parent();
    var list = dropdown.find('.list')
    list.stop(true).slideToggle();
});