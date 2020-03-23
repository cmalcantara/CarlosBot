from fbchat import Client
from fbchat.models import *
from _deploymentv2.inference import inference
import os
import time

group_introduction = 'Hi, I\'m Carlosbot, a neural network chatbot by Carlos A. if you want to chat, just @ me or pm directly. Though, I am still quite du b and will be improved later on.'
user_introduction = 'Hi, I\'m Carlosbot, a neural network chatbot by Carlos A. I\'m here if you want to chat. Though, I am still quite dumb and will be improved later on.'

sleep_period = 20
per_msg_delay = 1.5
max_msg_per_30s = 15
reply_counter = 0

def output(self, message_text, max_msg_per_30s, reply_counter, thread_id, thread_type): 
    bot_message = get_message(message_text)
    #bot_message = add_a_counter(bot_message, max_msg_per_30s, reply_counter)
    send_message(self, bot_message, thread_id, thread_type)

def add_a_counter(bot_message, max_msg_per_30s, reply_counter):
    #adds a counter for remaining messages left in the minute
    msgs_left = max_msg_per_30s - reply_counter - 1
    remaining_message = '[Msgs left this min: {}]'.format(msgs_left)
    bot_message = ' '.join([bot_message,remaining_message])
    return bot_message

def send_message(self, bot_message, thread_id, thread_type):
    global second_level_counter
    global reply_counter
    global per_msg_delay
    #sends the message and prints output
    self.send(Message(bot_message), thread_id=thread_id, thread_type=thread_type)
    time.sleep(per_msg_delay)
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
    
    def onPendingMessage(self, thread_id, thread_type, metadata, msg):
        global user_introduction
        """Called when the client is listening, and somebody that isn't
         connected with you on either Facebook or Messenger sends a message.
         After that, you need to use fetchThreadList to actually read the message.

         Args:
            thread_id: Thread ID that the message was sent to. See :ref:`intro_threads`
            thread_type (ThreadType): Type of thread that the message was sent to. See :ref:`intro_threads`
            metadata: Extra metadata about the message
            msg: A full set of the data received
        """
        #log.info("New pending message from {}".format(thread_id))
        #threads = self.fetchThreadList(thread_location=ThreadLocation.PENDING)
        #for thread in threads:
        self.send(Message(user_introduction), thread_id=thread_id, thread_type=thread_type)


    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        #self.markAsDelivered(thread_id, message_object.uid)
        #self.markAsRead(thread_id)
        global second_level_counter
        global reply_counter
        global max_msg_per_30s
        global group_introduction
        global sleep_period

        #Limits to max_msg_per_30sec
        if reply_counter > max_msg_per_30s - 1: 
            time.sleep(sleep_period)
            reply_counter = 0
            
        # If you're not the author, use the chatbot
        if author_id != self.uid:
            message_text = message_object.text
            print('Input: {}'.format(message_text))

            # If it's a group, find '@CarlosBot'
            if thread_type == ThreadType.GROUP:
                if message_text.find("@Carlosbot") != -1:
                    if message_text.find('introduce yourself') != -1:
                        self.send(Message(group_introduction), thread_id=thread_id, thread_type=thread_type)
                    else:
                        #remove the '@CarlosBot Tensorflow'
                        message_text = message_text.replace('@Carlosbot Bob', '')
                        message_text = message_text.replace('@Carlosbot', '')
                        print(message_text)

                        #gets bot_message, adds a counter, sends the message
                        output(self, message_text, max_msg_per_30s, reply_counter, thread_id, thread_type)

            #If it's a user, reply immediately
            elif thread_type == ThreadType.USER:
                #gets bot_message, adds a counter, sends the message
                output(self, message_text, max_msg_per_30s, reply_counter, thread_id, thread_type)

while True:
    client = CarlosBot("bobcarlos545@gmail.com", "bobocarlos505")
    client.listen()
