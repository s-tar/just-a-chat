/**
 * Created by mr.S on 31.12.14.
 */
(function($) {
    var __name__ = "st-dropdown";
    var speed = 200;
    var tabindex = 0;
    var z_index = 999;
    var _this = this;
    var methods = {
        init : function(options) {
            var settings = $.extend({
                name: 'value',
                item: '> li',
                onChange: function(){}
            }, options );
            this.each(function() {
                var dropdown = $('<div></div>').addClass(__name__).addClass('unselectable');
                dropdown.attr('class', dropdown.attr('class') +' '+$(this).attr('class'));
                var input = $('<input type="hidden" value=""/>').attr('name', settings.name);
                var current = $('<div></div>').addClass(__name__+'-current');
                var list = $('<ul></ul>').addClass(__name__+'-list');
                var text = $('<span class="text"></span>');
                var loading = $('<span class="loading"></span>');
                dropdown.attr('tabindex', -1);
                current.append(loading);
                current.append(text);
                current.append('<span class="fa fa-angle-down arrow"></span>');
                dropdown.append(input);
                dropdown.append(current);
                dropdown.append(list);
                var items = $(this).find(settings.item);
                if(items.length < 2)dropdown.addClass('no-dropdown');
                items.each(function(){
                    addItem(dropdown, $(this).val(), $(this).html(), $(this).is('[selected]'));
                });
                $(this).after(dropdown);
                $(this).remove();
                var current_width = current.outerWidth();
                var list_width = list.outerWidth();
                if(current_width > list_width) list.width(current_width);
                if(current_width < list_width) current.width(list_width);
                list.width(list.width());
                current.width(current.width());
                list.hide();
                list.css('position', 'absolute');
                list.stScroll();
                dropdown.on('click', '.'+__name__+'-current', function(){
                    if(dropdown.hasClass('loading') || dropdown.hasClass('no-dropdown'))return false;
                    dropdown.trigger('focus');
                    if(dropdown.hasClass('opened')) {
                        list.stop(true).slideUp(speed, function(){
                            dropdown.removeClass('opened');
                            dropdown.css('z-index','');
                            z_index--;
                        });
                    }else{
                        dropdown.css('z-index', z_index++);
                        dropdown.addClass('opened');
                        list.stop(true).slideDown(speed, function(){});
                    }
                });

                dropdown.on('blur', function(e){
                    setTimeout(function(){
                        var n = $(document.activeElement);
                        if(n.parents("."+__name__).length == 0){
                            list.slideUp(speed,function(){
                                dropdown.removeClass('opened');
                                dropdown.css('z-index','');
                                z_index--;
                            });
                        }else{
                            dropdown.focus();
                        }
                    },10);
                });

                dropdown.on('click', '.'+__name__+'-list .item', function(){
                    selectItem($(this));
                    input.val($(this).attr('value')).trigger('change');
                    settings.onChange($(this).attr('value'), dropdown);
                });

            });
        },
        clear : function() {
            this.each(function() {
                if($(this).hasClass(__name__)){
                    $(this).find('.'+__name__+'-list').html('');
                }
            });
        },
        addItem : function(value, text, selected){
            this.each(function() {
                if($(this).hasClass(__name__)){
                    addItem($(this), value, text, selected);
                }
                var list = $(this).find('.'+__name__+'-list');
                list.stScroll('destroy');
                list.stScroll();
                $(this).removeClass('no-dropdown');
                if(list.find('.item').length < 2)
                    $(this).addClass('no-dropdown');
            });

        },
        addItems : function(items){
            this.each(function() {
                if($(this).hasClass(__name__)){
                    for(var i in items){
                        if(i == 0) items[i][2] = true;
                        addItem($(this), items[i][0], items[i][1], items[i][2]);
                    }
                }
                var list = $(this).find('.'+__name__+'-list');
                list.stScroll('destroy');
                list.stScroll();
                list.find('.selected').trigger('click');
                $(this).removeClass('no-dropdown');
                if(list.find('.item').length < 2)
                    $(this).addClass('no-dropdown');
            });

        },
        loading : function(unload) {
            this.each(function() {
                if($(this).hasClass(__name__)){
                    $(this).addClass('loading');
                    if(unload === false) $(this).removeClass('loading');
                }
            });
        },
        update : function( content ) {  }
    };

    function addItem(dropdown, value, text, selected) {
        var list = dropdown.find('.'+__name__+'-list');
        var current = dropdown.find('.'+__name__+'-current');
        var item = $('<li></li>');
        item.attr('value', value);
        item.html(text);
        item.addClass('item');
        if(!!selected) item.addClass('selected');
        list.append(item);
        if(!current.is('[value]') || !!selected) selectItem(item);
        list.css('height', '');
    }

    function selectItem(item){
        var dropdown = item.closest('.'+__name__);
        var list = dropdown.find('.'+__name__+'-list');
        var current = dropdown.find('.'+__name__+'-current');
        current.find('.text').html(item.html());
        current.attr('value', item.attr('value'));
        list.stop(true).slideUp(speed, function(){
            dropdown.removeClass('opened');
            list.find('.item').removeClass('selected');
            item.addClass('selected');
        });
        dropdown.find('> input[type=hidden]').val(item.attr('value'))
//        if(typeof onChange == 'function')onChange();
    }

    $.fn.stDropDown = function(methodOrOptions) {
        if ( methods[methodOrOptions] ) {
            return methods[ methodOrOptions ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof methodOrOptions === 'object' || ! methodOrOptions ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  methodOrOptions + ' does not exist on jQuery.tooltip' );
        }
    };
})(jQuery)
