{% if user == None %}
<div class="header-login">
    <div class="links"><a href="javascript: user.registration()" >Регистрация</a> | <a href="javascript: user.login.native()">Вход</a></div>
    <div class="icon login-fb" onclick="user.login.fb()"><img src="/static/img/facebook-icon.png" alt=""/></div>
    <div class="icon login-vk" onclick="user.login.vk()"><img src="/static/img/vk.jpg" alt=""/></div>
</div>
{% else %}
<div class="profile">
    <div class="user-icon small">
        <a style="display: none" href="/profile/id{{user.usr_id}}"><img src="{{user.usr_photo_s or '/static/admin/img/user-no-photo.png'}}"/></a>
        <div class="photo"><img src="{{user.usr_photo_s or '/static/img/user-no-photo.png'}}"/></div>
    </div>
    <div class="info">
        {{user.usr_firstname or ''}} {{user.usr_lastname or ''}}<br/>
        <a href="javascript: user.logout()">Выход</a>
    </div>
</div>
{% endif %}