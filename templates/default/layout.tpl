<!doctype html>
<head>
	<meta charset="utf-8"/>
    <title>JUSTaCHAT</title>
    <link rel="icon" type="image/png" href="/static/img/s/favicon.ico" />
    <link rel="stylesheet" type="text/css" href="/static/css/style.css">
    <link rel="stylesheet" type="text/css" href="/static/css/user.css">
    <link rel="stylesheet" type="text/css" href="/static/css/form.css">
    <link rel="stylesheet" href="/static/css/font-awesome.min.css" type="text/css">
    <script src="/static/js/lib/jquery-1.10.2.min.js"></script>
    <script src="/static/js/lib/socket.io.js"></script>
</head>
    <body>
        {{widget("main.popup")}}
        {% include 'header.tpl' %}
        <div class="main-wrapper content">{% block content %}{% endblock %}</div>
        {% include 'footer.tpl' %}
        <script src="/static/js/lib/history.js/html4+html5/native.history.js"></script>
        <script src="/static/js/lib/jquery.autosize.min.js"></script>
        <script src="/static/js/main.js"></script>
        <script src="/static/js/user.js"></script>
        <script src="/static/js/form.js"></script>
        <script src="/static/js/chat.js"></script>
        <script src="/static/js/st_dropdown.js"></script>
        <script src="/static/js/st_scroll.js"></script>
        <script src="http://connect.facebook.net/en_US/all.js"></script>
        <script type="text/javascript" src="//vk.com/js/api/openapi.js?97"></script>
    </body>
</html>