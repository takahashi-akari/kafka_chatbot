/*
@title main.js
@author: Takahashi Akari <akaritakahashioss@gmail.com>
@date: 2022/07/23
@version: 1.1.0
@description: This application is a chatbot that uses Kafka as a message broker.
@license: MIT License Copyright (c) 2022 Takahashi Akari <akaritakahashioss@gmail.com>
*/
(function() {
    var Message, url;
    Message = function(arg) {
        (this.text = arg.text), (this.message_side = arg.message_side);
        this.draw = (function(_this) {
            return function() {
                var $message;
                $message = $(
                    $('.message_template')
                        .clone()
                        .html()
                );
                $message
                    .addClass(_this.message_side)
                    .find('.text')
                    .html(_this.text);
                if (this.message_side === 'left') {
                    url = '/static/images/bot.png';
                } else {
                    url = '/static/images/user.png';
                }
                $message
                    .find('.avatar')
                    .css('background-image', 'url(' + url + ')');
                $('.messages').append($message);
                return setTimeout(function() {
                    return $message.addClass('appeared');
                }, 0);
            };
        })(this);
        return this;
    };

    $(function() {
        var getMessageText, sendMessage;
        var socket = io.connect("https://kafkabot.akari.mn:3306/kafka")
        socket.on('connect', function() {
            console.log('connected');
        }
        );
        socket.on("connect",() => {
            console.log("connected");
        }
        );
        socket.on("disconnect",() => {
            console.log("disconnected");
        }
        );
        // socket on kafka_message
        socket.on("kafka_message",(data) => {
            console.log(data);
            var message = new Message({
                text: data.message,
                message_side: 'left'
            });
            message.draw();
            $('.messages').animate({ scrollTop: $('.messages')[0].scrollHeight }, 300);
        }
        );
        getMessageText = function() {
            return $('.message_input').val();
        };
        sendMessage = function(text) {
            var message;
            if (text.trim() === '') {
                return;
            }
            message = new Message({
                text: text,
                message_side: 'right'
            });
            message.draw();
            // emit kafka_message
            socket.emit('kafka_message', {
                message: text
            });
            $('.messages').animate({ scrollTop: $('.messages')[0].scrollHeight }, 300);
            return $('.message_input').val('');
        };
        $('.send_message').click(function() {
            return sendMessage(getMessageText());
        });
        $('.message_input').keyup(function(e) {
            if (e.which === 13) {
                return sendMessage(getMessageText());
            }
        });
        var message_greetings = new Message({
            text: "Hello, I'm KafkaBot. How can I help you?",
            message_side: 'left'
        });
        message_greetings.draw();
    });
}.call(this));
