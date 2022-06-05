/**
 * Plug-In name: jquery.codeStyle.js
 * Versions: 1.0.7
 * Modify time: 2017/04/01
 * Created by TomnTang on 2016/11/16
 * Website: http://www.lovevivi.com/plugin/jquery.codestyle.js/
 */

;(function($, win){
    $.fn.codeStyle = function(options){
        var defaults = {
            type: 'javascript',
            title: '',
            skin: 'default',
            fontsize: '12px',
            encode: true,
            toggle: true,
            show: true,
            about: 'http://www.lovevivi.com/plugin/jquery.codestyle.js/'
        };

        var settings = $.extend({}, defaults, options),
            codeKeyword = {
                javascript: 'function|var|return|true|false|this|switch|case|break|default|if|else|null|typeof|instanceof|new|this|call|window|prototype|do|while|continue|for|try|catch|throw|delete|with|const|let|export|import|super|console',
                html: 'html|head|title|meta|link|body|div|a|img|form|button|input|select|table|span|ul|li|ol|br|pre|p|script',
                css: 'display|position|overflow|top|right|bottom|left|margin|padding|border|color|font-size|font-family|font-weight|font|text-align|vertical-align|content|cursor|width|height|line-height|background|word-break|word-wrap|list-style|-radius|-top|-right|-bottom|-left|-color'
            };

        function getBoolean(value) {
            return (value === 'true') ? true : false;
        }

        return this.each(function(){
            var that = $(this), html = that.html(), set = {};

            set.type = that.attr('code-style-type') ? that.attr('code-style-type') : settings.type;
            set.title = that.attr('code-style-title') ? that.attr('code-style-title') : (that.attr('code-style-type') ? that.attr('code-style-type') : settings.type);
            set.encode = that.attr('code-style-encode') !== undefined ? getBoolean(that.attr('code-style-encode')) : settings.encode;
            set.toggle = that.attr('code-style-toggle') !== undefined ? getBoolean(that.attr('code-style-toggle')) : settings.toggle;
            set.show = that.attr('code-style-show') !== undefined ? getBoolean(that.attr('code-style-show')) : settings.show;
            set.fontSize = that.attr('code-style-fontsize') ? that.attr('code-style-fontsize') : settings.fontsize;
            set.height = that.attr('code-style-height') ? that.attr('code-style-height') : settings.height;
            set.skin = that.attr('code-style-skin') ? that.attr('code-style-skin') : settings.skin;

            that.addClass('code-style-'+ set.skin); // 添加皮肤

            // 转义符号
            if (set.encode) {
                html = html.replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;');
            }

            // 格式化代码
            switch (set.type) {
                case 'javascript':
                    var keyword = codeKeyword[set.type];
                    html = html.replace(/([\'\"]([^\'\"]*)[\'\"])/g, '<span class="code-style-string">$1</span>') // 属性值
                        .replace(new RegExp('\\b('+ keyword +')\\b', 'g'), '<span class="code-style-keyword">$1</span>') // 关键字
                        .replace(new RegExp('(\/\/.*)', 'g'), '<span class="code-style-comment">$1</span>'); // 单行注释
                    break;
                case 'html':
                    var tag = codeKeyword[set.type];
                    html = html.replace(/([\'\"]([^\'\"]*)[\'\"])/g, '<span class="code-style-string">$1</span>') // 属性值
                        .replace(/(&lt;!--)(.*)(--&gt;)/g, '<span class="code-style-comment">$1$2$3</span>') // 多行行注释
                        .replace(new RegExp('(&lt;\/)('+ tag +')(&gt;)', 'g'), '<span class="code-style-keyword">$1$2$3</span>') // 结束标签
                        .replace(new RegExp('(&gt;)', 'g'),'<span class="code-style-keyword">$1</span>') // 起始标签结束符
                        .replace(new RegExp('(&lt;)('+ tag +')(&gt;)?', 'g'), '<span class="code-style-keyword">$1$2$3</span>'); // 起始标签
                    break;
                case 'css':
                    var prop = codeKeyword[set.type];
                    html = html.replace(new RegExp('('+ prop +')', 'g'), '<span class="code-style-keyword">$1</span>') // 属性名称
                        .replace(/(:)( )?([^;^\n\r\t]*)/g, '$1$2<span class="code-style-string">$3</span>') // 属性值
                        .replace(/(\/\*(\s|.)*?\*\/)/g, '<span class="code-style-comment">$1</span>'); // 注释
                    break;
                default:
            }
            $('.code-style-comment').find('*').addClass('code-style-comment'); // 处理注释内的样式

            // 生成代码区域
            that.html('<ol class="code-style-ol code-style-'+ set.type +' code-style-'+ (set.show ? 'show' : 'hidden') +'"><li><span>'
                + html.replace(/[\r\n\t]+/g, '</span></li><li><span>')
                + '</span></li></ol>'
            ).css('fontSize', set.fontSize); // 设置代码字体大小

            var ol = that.find('ol.code-style-ol');
            ol.find('li:nth-child(odd)').addClass('odd'); // 设置奇数行样式
            ol.find('li:nth-child(even)').addClass('even'); // 设置偶数行样式
            ol.find('li:last-child').remove(); // 移除最后多余的一行

            // 设置标题
            if (!that.find('.code-style-title')[0]) {
                that.prepend('<div class="code-style-title">['+ set.title +']'
                    + (settings.about ? '<a href="'+ settings.about +'" target="_blank" title="jquery.codeStyle.js">?</a>' : '')
                    +'</div>'
                );
            }

            // 设置代码区域伸缩功能
            if (set.toggle) {
                that.find('.code-style-title').on('click', function(){
                    $(this).siblings('ol.code-style-ol').slideToggle();
                }).addClass('code-style-toggle');
            }

            // 设置代码区域显示高度
            if (set.height) {
                ol.css('maxHeight', set.height);
            }
        });

    }
})(jQuery, window);