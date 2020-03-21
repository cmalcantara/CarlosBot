from fbchat import Client
from fbchat.models import *
from _deploymentv2.inference import inference
import os
import time

max_msg_per_min = 5
max_msg_per_hour = 50
second_level_counter = 0
reply_counter = 0

def get_message(message_text):
    #gets the neural net output and extracts only the text
    bot_output = inference(message_text)
    bot_message = bot_output['answers']
    bot_message = bot_message[0]
    return bot_message

class CarlosBot(Client):
    #def get_and_send_message(message_text, thread_id, thread_type):

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        #self.markAsDelivered(thread_id, message_object.uid)
        #self.markAsRead(thread_id)
        global second_level_counter
        global reply_counter
        global max_msg_per_min
        global max_msg_per_hour

        #Limits to 3 messages per minute with a max of 50 messages per hour
        if second_level_counter > max_msg_per_hour - 1:
            time.sleep(60*60)
            second_level_counter = 0

        if reply_counter > max_msg_per_min - 1: 
            time.sleep(60)
            reply_counter = 0
            
        # If you're not the author, use the chatbot
        if author_id != self.uid:
            message_text = message_object.text
            print('Input: {}'.format(message_text))

            # If it's a group, find '@CarlosBot'
            if thread_type == ThreadType.GROUP:
                if message_text.find("@Carlosbot") != -1:
                    #remove the '@CarlosBot Tensorflow'
                    message_text = message_text.replace('@Carlosbot Bob', '')
                    message_text = message_text.replace('@Carlosbot', '')
                    print(message_text)
                    #get_and_send_message(message_text, thread_id, thread_type)
                    bot_message = get_message(message_text)

                    #adds a counter for remaining messages left in the minute
                    bot_message = ' '.join([bot_message,remaining_message])

                    #sends the message and prints output
                    self.send(Message(bot_message), thread_id=thread_id, thread_type=thread_type)
                    print('Output: {}'.format(bot_message))
                    reply_counter += 1
                    second_level_counter += 1
                    print('Counter: {}'.format(second_level_counter))

            #If it's a user, reply immediately
            elif thread_type == ThreadType.USER:
                #get_and_send_message(message_text, thread_id, thread_type)
                bot_message = get_message(message_text)

                #adds a counter for remaining messages left in the minute
                msgs_left = max_msg_per_min - reply_counter
                remaining_message = '[Msgs Left: {}]'.format(msgs_left)
                bot_message = ' '.join([bot_message,remaining_message])

                #sends the message and prints output
                self.send(Message(bot_message), thread_id=thread_id, thread_type=thread_type)
                print('Output: {}'.format(bot_message))
                reply_counter += 1
                second_level_counter += 1
                print('Counter: {}'.format(second_level_counter))

while True:
    try:
        client = CarlosBot("bobcarlos545@gmail.com", "bobocarlos505")
        client.listen()
    except:
        pass
