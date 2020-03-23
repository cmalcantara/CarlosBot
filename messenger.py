from fbchat import Client
from fbchat.models import *
from _deploymentv2.inference import inference
import os
import time

introduction = 'Hi, I\'m Carlosbot, a neural network chatbot by Carlos A. if you want to chat, just @ me or pm directly. Though, I am still quite dumb and will be improved later on.'
max_msg_per_min = 15
max_msg_per_hour = 50
second_level_counter = 0
reply_counter = 0

def output(self, message_text, max_msg_per_min, reply_counter, thread_id, thread_type): 
    bot_message = get_message(message_text)
    #bot_message = add_a_counter(bot_message, max_msg_per_min, reply_counter)
    send_message(self, bot_message, thread_id, thread_type)

def add_a_counter(bot_message, max_msg_per_min, reply_counter):
    #adds a counter for remaining messages left in the minute
    msgs_left = max_msg_per_min - reply_counter - 1
    remaining_message = '[Msgs left this min: {}]'.format(msgs_left)
    bot_message = ' '.join([bot_message,remaining_message])
    return bot_message

def send_message(self, bot_message, thread_id, thread_type):
    global second_level_counter
    global reply_counter
    #sends the message and prints output
    self.send(Message(bot_message), thread_id=thread_id, thread_type=thread_type)
    time.sleep(1.5)
    print('Output: {}'.format(bot_message))
    reply_counter += 1
    second_level_counter += 1
    print('Counter: {}'.format(second_level_counter))

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
        global introduction

        #Limits to 3 messages per minute with a max of 50 messages per hour
        #if second_level_counter > max_msg_per_hour - 1:
        #    time.sleep(60*60)
        #    second_level_counter = 0

        #acutally 30 sec
        if reply_counter > max_msg_per_min - 1: 
            time.sleep(20)
            reply_counter = 0
            
        # If you're not the author, use the chatbot
        if author_id != self.uid:
            message_text = message_object.text
            print('Input: {}'.format(message_text))



            # If it's a group, find '@CarlosBot'
            if thread_type == ThreadType.GROUP:
                if message_text.find("@Carlosbot") != -1:
                    if message_text.find('introduce yourself') != -1:
                        self.send(Message(introduction), thread_id=thread_id, thread_type=thread_type)
                    else:
                        #remove the '@CarlosBot Tensorflow'
                        message_text = message_text.replace('@Carlosbot Bob', '')
                        message_text = message_text.replace('@Carlosbot', '')
                        print(message_text)

                        #gets bot_message, adds a counter, sends the message
                        output(self, message_text, max_msg_per_min, reply_counter, thread_id, thread_type)

            #If it's a user, reply immediately
            elif thread_type == ThreadType.USER:
                #gets bot_message, adds a counter, sends the message
                output(self, message_text, max_msg_per_min, reply_counter, thread_id, thread_type)

while True:
    client = CarlosBot("bobcarlos545@gmail.com", "bobocarlos505")
    client.listen()
