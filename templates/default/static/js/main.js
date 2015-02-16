/**
 * Created by mr.S on 04.09.14.
 */

var base_url = '';
var site_title = 'JUSTaCHAT';
var window_is_active = true;
var History = window.History;
$(window).focus(function() {
    window_is_active = true;
});

$(window).blur(function() {
    window_is_active = false;
});

var socket = io.connect(base_url+'/main');
socket.on('connect', function(){});
socket.on('message', function(data){
    console.log(data);
});

$(document).ready(function(){
    console.log('Ready')
    $.get("/config/sn", function(config){
        FB.init({
            appId      : config.fb.app_id,
            status     : true,
            cookie     : true,
            xfbml      : true
        });

        VK.init({
            apiId: config.vk.app_id,
            onlyWidgets: true
        });
    } );
});

widget = {}
widget.update = function(name, cb){
    var widget = (typeof name == 'string') ? $('div[widget="'+name+'"]') : name;
    var attr = {}

    if(widget.length)
        $(widget[0].attributes).each(function() {
            attr[this.nodeName] = this.value;
        });
        $.ajax({
            type: "POST",
            url: base_url + "/widget/"+widget.attr('widget'),
            data: attr,
            dataType: 'html',
            success: function(data) {
//                widget.fadeOut(100,function(){
                    widget.html(data);
//                    widget.fadeIn(100);
                    if(typeof cb == 'function')cb()
//                });

            }
        });
}
widget.get = function(name, attr,  cb){
    $.ajax({
        type: "POST",
        url: base_url + "/widget/"+name,
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({"data": attr}),
        dataType: 'html',
        success: function(html) {
            cb(html);
        }
    });
}

popup = {}
popup.show = function(options) {
    var _popup = $(".main-popup")
    var container = _popup.find(".container");
    var content = _popup.find(".popup-content");
    _popup.find(".popup-header").removeClass('non-close');
    if(!!options.title) _popup.find(".popup-header .text").html(options.title);
    if(!!options.text) content.html('<div class="text">'+options.text+'</div>');
    if(!!options.html) content.html(options.html);
    if(options.close === false)
        _popup.find(".popup-header").addClass('non-close');

    if(!!options.buttons){
        var btn_container = $('<div class="buttons"></div>');
        var left = $('<div class="buttons-left"></div>');
        var right = $('<div class="buttons-right"></div>');
        btn_container.append(left);
        btn_container.append(right);
        for(var i in options.buttons) {
            (function(index) {
                var b = options.buttons[index];
                var button = $('<input type="button" value="'+ b.caption+'"/>');
                if(typeof(b.action) == 'function'){
                    button.on("click", function(){
                        if($(this).attr('processing') == 'true') return;
                        $(this).attr('processing', 'true')
                        b.action();
                    });
                }
                if(b.left == true) left.append(button); else right.append(button);
            })(i);
        }
        content.append(btn_container);
    }

    _popup.css("display","block");
    _popup.css("visibility","hidden");
    popup.center();
    _popup.css("display","none");
    _popup.css("visibility","");
    _popup.fadeIn();

}
popup.hide = function(cb) {
    var popup = $(".main-popup")
    var _cb = function(){}
    if(typeof(cb) == 'function') _cb = cb
    popup.fadeOut(_cb)
}
popup.center = function(){
    var popup = $(".main-popup")
    var container = popup.find(".container");
    container.css("margin-left", Math.round(-container.width()/2));
    container.css("margin-top", Math.round(-container.height()/2));
}

$(function() {
    if ( !History.enabled ) { return false;}
    History.Adapter.bind(window,'statechange',function(e) {
    });
});

$(document).on('focus', 'textarea.autosize',  function(){
    $(this).autosize();
});

$(document).ready(function(){
    $('.custom-scroll').stScroll();
});

(function($){
    $.fn.disableSelection = function() {
        return this
        .attr('unselectable', 'on')
        .css('user-select', 'none')
        .css('-moz-user-select', 'none')
        .css('-khtml-user-select', 'none')
        .css('-webkit-user-select', 'none')
        .on('selectstart', false)
        .on('contextmenu', false)
        .on('keydown', false)
        .on('mousedown', false);
    };

    $.fn.enableSelection = function() {
        return this
        .attr('unselectable', '')
        .css('user-select', '')
        .css('-moz-user-select', '')
        .css('-khtml-user-select', '')
        .css('-webkit-user-select', '')
        .off('selectstart', false)
        .off('contextmenu', false)
        .off('keydown', false)
        .off('mousedown', false);
    };

})(jQuery);


function updateContent(){
    window.location.reload();
//
//    var content = $('.content');
//    $.get('', function(data){
//        content.fadeOut(function(){
//            data = data.substr(data.indexOf("<body>"), data.indexOf("</body>"));
//            console.log($('<div>'+data+'</div>').find('.content').html());
//            content.html($('<div>'+data+'</div>').find('.content').html()).fadeIn();
//            setTimeout(function(){init();},1);
//        });
//    })
}