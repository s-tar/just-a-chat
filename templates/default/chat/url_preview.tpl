<div class="site-url">
    {% if og.image %}<div  class="site-image"><a href="{{url}}" target="_blank"><img src="{{og.image}}"/></a></div>{% endif %}
    <div class="site-info">
        <div class="site-title"><a href="{{url}}" target="_blank">{{og.title or url}}</a></div>
        <div class="site-description">{{og.description or ''}}</div>
    </div>
</div>