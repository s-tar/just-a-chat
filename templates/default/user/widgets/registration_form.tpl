<form class="user-registration-form form ajax" action="/user/registrate" method="post" style="padding-top: 10px">
    <div style="float: right; width: 300px">
        <div class="row user-photo" style="width: 200px; padding: 0px;margin: auto;">
            <div style="width: 200px;height: 200px;margin-bottom: 7px" class="image-loader" name="_photo" >
                <div class="source-wrapper">
                    <input type="file" name="photo" value=""/>
                </div>
                <div class="source" style="background-image: url('')"></div>
                <div class="no-photo">Загрузить фотографию</div>
                <span class="loading"></span>
            </div>
        </div>
        <div class="row">
            <div style="width: 49%;float: left"><input type="text" placeholder="Имя" name="first_name" value="" /></div>
            <div style="width: 49%;float: right"><input type="text" placeholder="Фамилия" name="last_name" value=""/></div>
        </div>
        <div class="row">
            <input type="text" autocomplete="off" placeholder="Электронная почта" name="email" value=""/>
        </div>
        <div class="row">
            <input type="password" autocomplete="off" placeholder="Пароль" name="password" value=""/>
            <input type="password" autocomplete="off" placeholder="Повтор пароля" name="repassword" value=""/>
        </div>
    </div>
    <div class="row" style="clear: both">
        <input type="button" class="submit" value="Регистрация" style="width: 49%;"/>
    </div>
</form>