from fbchat import Client
from fbchat.models import *
from _deploymentv1.inference import inference

class CarlosBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        # If you're not the author, use the chatbot
        if author_id != self.uid:
            message_text = message_object.text
            print('Input: {}'.format(message_text))

            # If it's a group, find '@CarlosBot'
            if thread_type == ThreadType.GROUP:
                if message_text.find("@CarlosBot") != -1:
                    #remove the @CarlosBot +/ Tensorflow
                    message_text = message_text.replace('@CarlosBot Tensorflow', '')
                    print(message_text)
                    bot_message = inference(message_text)
                    self.send(bot_message, thread_id=thread_id, thread_type=thread_type)
                    print('Output: {}'.format(bot_message))

            #If it's a user, reply immediately
            elif thread_type == ThreadType.USER:
                bot_message = inference(message_text)
                self.send(bot_message, thread_id=thread_id, thread_type=thread_type)
                print('Output: {}'.format(bot_message))

client = CarlosBot('fakecma00@gmail.com', '4akecmaisgreat')
client.listen()
