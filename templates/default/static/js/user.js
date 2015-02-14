/**
 * Created by mr.S on 04.09.14.
 */
socket.on('user.online', function(data){
    var user = data.user;
//    user.online(user)
    $('.user-icon[user_id='+user.id+']').addClass('online')
});
socket.on('user.offline', function(data){
    var user = data.user;
    $('.user-icon[user_id='+user.id+']').removeClass('online')
});

socket.on('user.logout', function(data){
    updateContent();
    widget.update('user.header');
    History.pushState({state: 'main'}, 'JustAChat', '/');
});

socket.on('user.login', function(data){
    updateContent();
    widget.update('user.header');
});

user = {}
user.processing = false;
user.login = function() {
    function sendUserData(sn, data){
        $.ajax({
            type: "POST",
            url: base_url + "/user/login/"+sn,
            data: {
                data: JSON.stringify(data)
            },
            success: function(data) {
                if(data.status == 'ok') {
                    //widget.update("user.header");
                    socket.emit('user.login');
                    //window.location.reload();
                    user.processing = false;
                }
            }
        });
    }

    function vk() {
        if(!user.processing){user.processing = true;}else{return false}
        VK.Auth.getLoginStatus(function(response) {
            response.session = ''; // force VK.Auth.login
            if (response.session) {
                sendUserData('vk',response.session);
            } else {
                VK.Auth.login(function(response) {
                    if (response.session) {
                        sendUserData('vk',response.session);
                    } else {
                        user.processing = false;
                        console.log('User cancelled login or did not fully authorize.');
                    }
                });
            }
        });
    }

    function fb() {
        if(!user.processing){user.processing = true;}else{return false}
        FB.getLoginStatus(function(response) {
            if (response.status === 'connected') {
                sendUserData('fb',response);
            } else {
                FB.login(function(response) {
                    if (response.authResponse) {
                        sendUserData('fb',response);
                    } else {
                        user.processing = false;
                        console.log('User cancelled login or did not fully authorize.');
                    }
                }, {scope: 'email,user_likes'});
            }
        });
    }

    function native(data){
        if(!data) {
            widget.get('user.login.form',{}, function(html){
                popup.show({title: 'Авторизация', html: html});
            });
        } else {
            $.ajax({
                type: "POST",
                url: base_url + "/user/login/native",
                data: {
                    email: data.email,
                    password: data.password
                },
                dataType: 'json',
                success: function(data) {
                    socket.emit('user.login');
                    //popup.hide();
                    //widget.update("user.header");
                }
            });
        }

    }

    return {
        processing: user.processing,
        vk: vk,
        fb: fb,
        native: native
    }
}();

user.logout = function(){
    socket.emit('user.logout');

//    $.ajax({
//        type: "POST",
//        url: base_url + "/user/logout",
//        data: {},
//        dataType: 'json',
//        success: function(data) {
//            //widget.update("user.header");
//            window.location.reload()
//        }
//    });
}
user.registration = function() {
    widget.get('user.registration.form',{}, function(html){
        popup.show({title: 'Новый пользователь', html: html});
    });
}

$(document).on('submit', '.user-login-form', function(e){
    var form = $(this);
    form.trigger("ajax_submit", function(response){
        if(response.status == 'ok') {
            socket.emit('user.login');
            popup.hide()
        }else if(response.status == 'fail') {
            showErrors(form, response.errors);
        }
    })
    e.preventDefault();
    return false;
});

$(document).on('submit', '.user-registration-form', function(e){
    var form = $(this);
    form.trigger("ajax_submit", function(response){
        if(response.status == 'ok') {
            popup.hide();
//            window.location.reload()
        }else if(response.status == 'fail') {
            showErrors(form, response.errors);
        }
    })
    e.preventDefault();
    return false;
});

user.online = function(user){
    console.log(user.usr_firstname +" "+ user.usr_lastname);
}