/**
 * Created by mr.S on 12.02.15.
 */


socket.on('chat.new', function(data){
    var html = $(data.chat_item);
    var chats = $('.chats');
    var chats_container = chats.find('.mine .list');
    html.css('display', 'none');
    chats.find('.mine').css('display','');
    chats_container.prepend(html);
    chats.find('.no-chats').css('display', 'none');
    if(window_is_active) setTimeout(function(){html.trigger('click')}, 0)
    var scroller = chats.find('.custom-scroll');

    scroller.stScroll('getValue', function(new_val){
        html.slideDown(function(){
            scroller.stScroll('update');
            scroller.stScroll('setValue', new_val, 0);
         });
    });


});

socket.on('chat.join', function(data){
    var chat_item = $(data.chat_item);
    var chat_id = data.chat.id;
    var chats = $('.chats');
    var other = chats.find('.other');
    var mine = chats.find('.mine');

    var scroller = chats.find('.custom-scroll');

    function add_chat(){
        chat_item.css('display', 'none');
        mine.find('.list').prepend(chat_item);
        mine.find('.list .no-chats').css('display', 'none');
        mine.css('display', '');
        if(window_is_active) setTimeout(function(){chat_item.trigger('click')}, 0)

        scroller.stScroll('getValue', function(new_val){
        chat_item.slideDown(function(){
            scroller.stScroll('update');
            scroller.stScroll('setValue', new_val, 0);
         });
        });
    }

    var other_chat = chats.find('.other .chat[data-id='+chat_id+']');
    if(other_chat.length) {
        chats.find('.other .chat[data-id='+chat_id+']').slideUp(function(){
            $(this).remove();
            if(other.find('.chat').length == 0) other.css('display', 'none');
            add_chat();
        });
    }else{
        add_chat();
    }




});

socket.on('chat.new_message', function(data){
    var chat_id = data.message.chat_id;
    var chat = $('.messages .chat[data-id='+chat_id+']');
    $('.chats .chat[data-id='+chat_id+']:not(.active)').addClass('message');
    if(chat.length){
        var scroller = chat.find('.custom-scroll');
        var was_hidden = scroller.find('.st-scroll-scrollbar').css('display') == 'none';
        scroller.stScroll('getValue', function(val){
            var html = $(data.message_item);
            chat.find('.chat-messages-wrapper').append(html);
            chat.find('.no-messages').remove();
            scroller.stScroll('getValue', function(new_val){
                scroller.stScroll('update');
                scroller.stScroll('setValue', new_val, 0);
                if(val > 99 || was_hidden) scroller.stScroll('setValue', 100);
            });
        });
    }
});

$(document).on("click", ".chat-join input", function(){
    var chat = $(this).closest('.chat');
    var chat_id = chat.attr('data-id');
    $('.messages').addClass('loading');
    chat.remove();
    $.ajax({
        type: "POST",
        url: base_url + "/chat/"+ chat_id + "/join",
        dataType: 'json',
        success: function(data) {
            if(data.status == "ok") {

            }else{
                popup.show({
                    title: "Ошибка",
                    text: "Произошла ошибка при удалении..."
                })
            }
        }
    });
});

$(document).on("click", ".chat .delete", function(e){
    var _this = $(this);
    var chat = $(this).closest('.chat');
    var chat_id = chat.attr('data-id');
    e.preventDefault();
    popup.show({
        close: false,
        title: "Выход из чата",
        text: "Вы уверены, что хотите выйти из чата?",
        buttons: [{caption: "Да",
                   left: true,
                    action: function(){
                        $.ajax({
                            type: "POST",
                            url: base_url + "/chat/"+ chat_id + "/leave",
                            dataType: 'json',
                            success: function(data) {
                                if(data.status == "ok") {
                                    History.pushState({state: 'main'}, site_title, '/');
                                    $('.messages').addClass('no-chat-selected');
                                    $('.messages .chat[data-id="'+chat_id+'"]').remove();
                                    chat.slideUp(function(){
                                        var list = $(this).closest('.list');
                                        $(this).remove();
                                        if(list.find('.chat').length == 0) {
                                            list.find('.no-chats').css('display','');
                                        }
                                    });
                                    popup.hide()
                                }else{
                                    popup.show({
                                        title: "Ошибка",
                                        text: "Произошла ошибка при удалении..."
                                    })
                                }
                            }
                        });
                    }
            },{
                caption: "Нет",
                action: function(){popup.hide()}
            }]
    });
});

$(document).on('click', '.chats .chat', function(){
    var id = $(this).attr('data-id');
    var messages = $('.messages');
    $(this).closest('.chats').find('.chat.active').removeClass('active');
    $(this).addClass('active');
    $(this).removeClass('message');
    var link = '/chat/'+id;
    if(History.enabled) {
        History.pushState({state: 'main'}, site_title+': '+$(this).attr('data-name'), link);
        var chat = messages.find('.chat[data-id='+id+']');
        var list = messages.find('.list');
        messages.addClass('loading');
        messages.removeClass('no-chat-selected');
        list.find('.chat').removeClass('current');
        if(chat.length == 0) {
            widget.get('chat.messages',{'chat_id': id}, function(data){
                data = $(data);
                list.append(data);
                var scroller = data.find('.custom-scroll');
                scroller.stScroll('update');
                scroller.stScroll('setValue', 100, 0);
                messages.removeClass('loading');
            });
        }else{
            var scroller = chat.find('.custom-scroll');
            chat.addClass('current');
            scroller.stScroll('update');
            scroller.stScroll('setValue', 100, 0);
            messages.removeClass('loading');
        }
    } else {
        window.location.href = link;
    }

});

$(document).on("submit", "form.new-chat-form", function(e){
    var form = $(this);
    if(!form.hasClass('disabled')) {
        form.addClass('disabled');
        form.trigger("ajax_submit", function(response){
            form.removeClass('disabled');
            if(response.status == 'ok') {
                form.find('input').val('');
            }else if(response.status == 'fail') {
                showErrors(form, response.errors);
            }
        })
    }

    e.preventDefault();
    return false;
});

$(document).on("submit", "form.new-message-form", function(e){
    var form = $(this);
    if(form.find('textarea').val().trim() == '')return false;
    form.trigger("ajax_submit", function(response){
        if(response.status == 'ok') {
            form.find('textarea').val('').trigger('autosize.resize');
        }
    })
    e.preventDefault();
    return false;
});

$(document).on('keydown', 'form.new-message-form textarea', function (e){
    if(e.which == 13) {
        if(e.ctrlKey){
            $(this).val($(this).val()+'\n');
        }else {
            $(this).closest('form').submit();
            return false;
        }

    }
});

$(document).on('click', '.chat-actions .form:not(.active) button', function(e){
    var ca = $(this).closest('.chat-actions');
    ca.find('.form').removeClass('active').find('input').val('');
    ca.find('.error').remove();
    $(this).closest('.form').addClass('active');
    $('.search-chat-form input').trigger('keyup');
    e.preventDefault();
    return false;
})

var search_delay = null;
$(document).on('keyup', '.search-chat-form input', function(e){
    var text = $(this).val();
    var container = $('.chats');
    var other = container.find('.other');
    var mine =  container.find('.mine');
    var chats = mine.find('.chat');
    var no_chats_found = container.find('.no-chats-found');
    no_chats_found.css('display','none');
    mine.css('display', 'none');
    chats.css('display', '');
    if(text == ''){
        container.removeClass('loading');
        mine.css('display', '');
    }else{
        var hidden_count = 0;
        chats.each(function(){
            var name = $(this).attr('data-name');
            $(this).css('display', '');
            if(name.substr(0, text.length).toLowerCase() != text.toLowerCase()){
                hidden_count++;
                $(this).css('display', 'none');
            }else{
                mine.css('display', '');
            }
        });
        container.addClass('loading');
        clearTimeout(search_delay);
        search_delay = setTimeout(function(){
            $.post('/chat/search', { text: text }, function(data){
                var list = other.find('.list');
                list.html('');
                other.css('display','none');
                if(data.chat_items.length > 0)other.css('display','');
                for(var i in data.chat_items){
                    list.append(data.chat_items[i]);
                }
                if(other.css('display') == 'none' && mine.css('display') == 'none')
                    no_chats_found.css('display','');
                $('.chats .custom-scroll').stScroll('update');
                container.removeClass('loading');
            })
        }, 500);
    }
    $('.chats .custom-scroll').stScroll('update');
})

$(document).ready(function(){
    init();
});
$(window).resize(function(){
    init();
});

$(document).on('focus', '.new-message textarea', function(){
    $(this).autosize({callback: function(){
        var _this = $(this);
        var chat = _this.closest('.chat');
        var scroller = chat.find('.custom-scroll');

        scroller.stScroll('getValue', function(val){
            chat.css('padding-bottom', _this.closest('.new-message').outerHeight(true));
            scroller.stScroll('update');
            scroller.stScroll('setValue', val, 0);
        });
    }});
});
function init(){
    $('.new-message textarea').trigger('focus').trigger('blur');
    $('.custom-scroll').stScroll('update');
    $('.messages .custom-scroll').stScroll('setValue', 100, 0);

}