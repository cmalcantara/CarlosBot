from fbchat import Client
from fbchat.models import *
from _deploymentv2.inference import inference
import os
import time

class CarlosBot(Client):
    def get_and_send_message(message_text, thread_id, thread_type):
        #gets the neural net output and extracts only the text
        bot_output = inference(message_text)
        bot_message = bot_output['answers']
        bot_message = bot_message[0]

        #sends the message and prints output
        self.send(Message(bot_message), thread_id=thread_id, thread_type=thread_type)
        print('Output: {}'.format(bot_message))

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        #self.markAsDelivered(thread_id, message_object.uid)
        #self.markAsRead(thread_id)

        #Limits to 3 messages per minute with a max of 60 messages per hour
        if second_level_counter > 59:
            time.sleep(60*60)
            second_level_counter = 0

        if reply_counter > 2: 
            time.sleep(60)
            reply_counter = 0
            
        # If you're not the author, use the chatbot
        if author_id != self.uid:
            message_text = message_object.text
            print('Input: {}'.format(message_text))

            else
                # If it's a group, find '@CarlosBot'
                if thread_type == ThreadType.GROUP:
                    if message_text.find("@CarlosBot") != -1:
                        #remove the '@CarlosBot Tensorflow'
                        message_text = message_text.replace('@CarlosBot Tensorflow', '')
                        print(message_text)
                        get_and_send_message(message_text, thread_id, thread_type)
                        reply_counter += 1
                        second_level_counter += 1

                #If it's a user, reply immediately
                elif thread_type == ThreadType.USER:
                    get_and_send_message(message_text, thread_id, thread_type)
                    reply_counter += 1
                    second_level_counter += 1

second_level_counter = 0
reply_counter = 0
client = CarlosBot('fakecma00@gmail.com', '4akecmaisgreat')
client.listen()
