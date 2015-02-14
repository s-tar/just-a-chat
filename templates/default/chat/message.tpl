<div class="message {{'system' if message.is_system}}" data-id="{{message.id}}">
    {% if message.is_system %}
        {{message.text}}
    {% endif %}
    {% if not message.is_system %}
    <div class="sender">{{widget('user.icon', {'user': message.sender})}}</div>
    <div class="info">
        <div class="fa fa-caret-left arrow"></div>
        <div class="datetime" title="{{message.datetime.strftime('%d.%m.%Y %H:%M:%S')}}">
            {{message.datetime.strftime('%H:%M') if (datetime.datetime.now() - message.datetime).days < 1 }}
            {{message.datetime.strftime('%d.%m.%y') if (datetime.datetime.now() - message.datetime).days >= 1 }}
        </div>
        <div class="text">{{url_html or message.text|e}}</div>
    </div>
    {% endif %}
</div>