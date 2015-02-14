/**
 * Created by mr.S on 04.01.15.
 */
(function($) {
    var __name__ = "st-scroll";
    var _this = this;
    var methods = {
        init : function(options) {
            this.each(function() {
                $(this).addClass(__name__).addClass('hide-scrollbar');
                var content = $('<div></div>').addClass(__name__+"-content");
                var content_wrapper = $('<div></div>').addClass(__name__+"-content-wrapper");
                var scrollbar = $('<div></div>').addClass(__name__+"-scrollbar");
                var track = $('<div></div>').addClass(__name__+"-track");
                var thumb = $('<div></div>').addClass(__name__+"-thumb");
                $(this).wrapInner(content);
                $(this).wrapInner(content_wrapper);
                $(this).append(scrollbar);
                scrollbar.append(track);
                track.append(thumb);
                content_wrapper = $(this).find('.'+__name__+'-content-wrapper');
                content = content_wrapper.find('.'+__name__+'-content');
                var d = $(this).css('display');
                if(d == 'none') $(this).css('display', 'block');
                content_wrapper.height($(this).height());
                if(content.height() > content_wrapper.height())$(this).removeClass('hide-scrollbar');
                thumb.height(Math.round(content_wrapper.height() / content.height() * 100)+'%');
                $(this).css('display', d);
            });
        },
        destroy: function(){
            this.each(function(){
                destroy($(this));
            });
        },
        update: function(){
            this.each(function(){
                destroy($(this));
                $(this).stScroll()
            });
        },
        setValue: function(value, speed){
            if(speed === undefined)speed = 200;
            this.each(function(){
                var cw =  $(this).find('.'+__name__+'-content-wrapper');
                var content = cw.find('.'+__name__+'-content');
                var track = $(this).find('.'+__name__+'-track');
                var thumb = $(this).find('.'+__name__+'-thumb');
                cw.animate({scrollTop: (content.outerHeight()-cw.height())*value/100}, speed);
                thumb.animate({'top': (track.height() - thumb.outerHeight()) * value/100}, speed);

            });
        },
        getValue: function(cb){
            this.each(function(){
                var cw =  $(this).find('.'+__name__+'-content-wrapper');
                var content = cw.find('.'+__name__+'-content');
                var track = $(this).find('.'+__name__+'-track');
                var thumb = $(this).find('.'+__name__+'-thumb');
                if(typeof cb == 'function') cb(cw.scrollTop() / (content.outerHeight() - cw.height())*100);
            });
        }
    };

    function destroy(el) {
        var content_wrapper = el.find('.'+__name__+'-content-wrapper');
        var content = el.find('.'+__name__+'-content');
        content.unwrap();
        content.find('> *:first-child').unwrap();
        el.find('.'+__name__+'-scrollbar').remove();
        content_wrapper.remove();
        el.removeClass(__name__);
        el.removeClass('hide-scrollbar');
    }
    $(document).on('mousewheel DOMMouseScroll', '.'+__name__, function(e){
        var content_wrapper = $(this).find('.'+__name__+'-content-wrapper');
        var content = content_wrapper.find('.'+__name__+'-content');
        var track = $(this).find('.'+__name__+'-track');
        var thumb = $(this).find('.'+__name__+'-thumb');
        var scrollTop = content_wrapper.scrollTop();
        var delta = -1+(e.originalEvent.wheelDelta > 0 || e.originalEvent.detail < 0)*2;
        content_wrapper.scrollTop( scrollTop - (delta * content_wrapper.height()/2));
        var dy = content_wrapper.scrollTop() / (content.height() - content_wrapper.height());
        if(dy < 0)dy = 0;
        if(dy > 1)dy = 1;
        thumb.css('top', (track.height() - thumb.height()) * dy+"px");
        e.preventDefault();
    });

    $(document).on('mousedown', '.'+__name__+' .'+__name__+'-thumb', function(e){
        var stScroll = $(this).closest('.'+__name__);
        var content_wrapper = stScroll.find('.'+__name__+'-content-wrapper');
        var content = content_wrapper.find('.'+__name__+'-content');
        var scrollbar = stScroll.find('.'+__name__+'-scrollbar');
        var track = stScroll.find('.'+__name__+'-track');
        var thumb = stScroll.find('.'+__name__+'-thumb');

        var x_start = e.pageX;
        var y_start = e.pageY;
        var max_y = track.height() - thumb.height();
        var thumb_pos = thumb.position().top;
        var max_scroll = content.height() - content_wrapper.height();
        $('body').disableSelection()

        $(document).on('mousemove.'+__name__ , function(e){
            var dy = e.pageY - y_start;
            thumb.css('top', thumb_pos + dy);
            var top = thumb.position().top;
            if(top < 0)thumb.css('top', '0px');
            if(top > max_y)thumb.css('top', max_y + 'px');
            content_wrapper.scrollTop(top/max_y * max_scroll);
        });

        $(document).on('mouseup.'+__name__, function(){
            $(document).off('mousemove.'+__name__);
            $(document).off('mouseup.'+__name__);
            $('body').enableSelection();
        });
    });



    $.fn.stScroll = function(methodOrOptions) {
        if ( methods[methodOrOptions] ) {
            return methods[ methodOrOptions ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof methodOrOptions === 'object' || ! methodOrOptions ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  methodOrOptions + ' does not exist on jQuery.tooltip' );
        }
    };
})(jQuery)
