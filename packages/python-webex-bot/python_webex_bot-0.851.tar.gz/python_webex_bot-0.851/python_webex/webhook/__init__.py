from flask import Flask, request
from pprint import pprint
import inspect

app = Flask(__name__)
bot = None

@app.route("/", methods=[ 'GET', 'POST' ])
def index():
    json_data = request.get_json()
    message_id = json_data[ "data" ][ "id" ]
    message_info = bot.get_message_details( message_id=message_id ).json()
    if message_info[ "personId" ] == bot.get_own_details().json()[ 'id' ]:
        return "cannot respond to my own messages"
    

    if 'files' in message_info:
        if 'text' in message_info:
            message_text = message_info['text']

            if message_info['text'] in bot.hears_file_to_function:
                files = message_info['files']

                if 'message_info' in bot.hears_to_function[message_text].__code__.co_varnames:
                    bot.hears_file_to_function[message_text](files=message_info['files'], room_id=message_info['roomId'], message_info=message_info)
                else:
                    bot.hears_file_to_function[message_text](files=message_info['files'], room_id=message_info['roomId'])

                return "Works"

            elif '*' in bot.hears_file_to_function:
                if 'message_info' in bot.hears_to_function["*"].__code__.co_varnames:
                    bot.hears_file_to_function['*'](files=message_info['files'], room_id=message_info['roomId'], message_info=message_info)
                else:
                    bot.hears_file_to_function['*'](files=message_info['files'], room_id=message_info['roomId'])

                return "Default file action"
            else:
                print("Default response for file sent with text not set")

        elif bot.default_attachment is not None:

            if 'message_info' in bot.default_attachment.__code__.co_varnames:
                bot.default_attachment(files=message_info['files'], room_id=message_info['roomId'], message_info=message_info)
            else:
                bot.default_attachment(files=message_info['files'], room_id=message_info['roomId'])
            return "Works"
        else:
            print("No action set for receiving the file")

    elif message_info[ "text" ].strip() != "" and message_info[ "text" ] in bot.hears_to_function:
        message_text = message_info[ "text" ]
        if 'message_info' in bot.hears_to_function[message_text].__code__.co_varnames:
            bot.hears_to_function[ message_text ](room_id=message_info["roomId"], message_info=message_info)
        else:
            bot.hears_to_function[ message_text ](room_id=message_info["roomId"])
        

    elif message_info["text"].strip() != "" and  message_info[ "text" ] not in bot.hears_to_function:
#        if 'message_info' in bot.hears_to_function[message_text].__code__.co_varnames:
        if 'message_info' in bot.hears_to_function["*"].__code__.co_varnames:
            bot.hears_to_function[ "*" ]( room_id=message_info["roomId"], message_info=message_info)
        else:
            bot.hears_to_function[ "*" ]( room_id=message_info["roomId"])
        
        
    return "successfully responded"



@app.route("/attachment-response", methods=["GET", "POST"])
def attachment_response():
    json_data = request.get_json()
    message_id = json_data['data']['messageId']
    message_dict = bot.get_attachment_response(json_data['data']['id'])
    if message_id in bot.attachment_response_to_function:
        response = bot.attachment_response_to_function[message_id](message_dict)
    else:
        room_id = message_dict['roomId']
        bot.send_message(room_id=room_id, text='The form could not be submitted. You may need to request for the form again then submit. Sorry for the inconvenience :)')

    return "attachment response received"
