<div class="frame st-chat">
    <div class="chats">
        <div class="title">ЧАТЫ</div>
        <div class="chat-actions">
            <form class="new-chat-form form ajax active" action="/chat/new" method="post">
                <input type="text" placeholder="Новый чат" name="chat_name"/>
                <button><span class="fa fa-plus-circle"></span></button>
            </form>
            <form class="search-chat-form form ajax" action="/chat/new" method="post">
                <button><span class="fa fa-search"></span></button>
                <input type="text" placeholder="Искать чат" name="chat_name"/>
            </form>
        </div>
        <div class="chats-list-wrapper">
            <div class="custom-scroll">
                <div class="no-chats-found" style="display: none">Ничего похожего не найдено...</div>
                <div class="other" style="{{'display: none' if not current_is_new }}">
                    <div class="separator" ><span>Другие чаты</span></div>
                    <div class="list">
                        {% if current_is_new %}
                        {{widget('chat.item', {'chat': current_chat, 'is_active': True})}}
                        {% endif %}
                    </div>
                </div>
                <div class="mine">
                    <div class="separator"><span>Мои чаты</span></div>
                    <div class="list">
                        <div class="no-chats" style="{{'display: none' if chats|length != 0 }}">Пока чатов нет</div>
                        {% for chat in chats %}
                        {{widget('chat.item', {'chat': chat, 'is_active': current_chat and chat.id == current_chat.id})}}
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="messages {{'no-chat-selected' if not current_chat}}">
        <div class="no-chat-selected-text">
            <span class="fa fa-arrow-left"></span> Выберите чат
        </div>
        <div class="list">
            {% if current_chat %}
            {{widget('chat.messages', {'chat_id': current_chat.id})}}
            {% endif %}
        </div>
    </div>
</div>