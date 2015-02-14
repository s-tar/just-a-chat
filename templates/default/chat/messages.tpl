{% if chat %}
<div class="chat current" data-id="{{chat.id}}">
    <div class="chat-messages custom-scroll">
        {% if not is_member %}
            <div class="chat-join">
                Пока еще Вы не являетесь учасником этого чата<br/>
                <input type="button" value="Присоединиться"/>
            </div>
        {% endif%}
        {% if is_member %}
            {% if chat.messages|length == 0 %}
                <div class="no-messages">Пока сообщений нет...</div>
            {% endif %}
            <div class="chat-messages-wrapper">
            {% for message in chat.messages %}
                {{widget('chat.message',{'message': message})}}
            {% endfor %}
            </div>
        {% endif%}
    </div>
    {% if is_member %}
    <div class="new-message">
        <div class="wrapper">
            <form  class="new-message-form form ajax" action="/chat/new_message" method="post">
                <input type="hidden" name="chat_id" value="{{chat.id}}"/>
                <textarea name="message" rows="1"></textarea>
                <button><span class="fa fa-send"></span></button>
            </form>
        </div>
    </div>
    {% endif%}
</div>
{% endif %}