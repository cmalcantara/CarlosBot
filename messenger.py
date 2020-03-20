from fbchat import Client
from fbchat.models import *
from _deploymentv1.inference import inference
import time
import os

# Fetches a list of all users you're currently chatting with, as `User` objects
#users = client.fetchAllUsers()
#
#print("users' IDs: {}".format([user.uid for user in users]))
#print("users' names: {}".format([user.name for user in users]))
#
#
## If we have a user id, we can use `fetchUserInfo` to fetch a `User` object
#user = client.fetchUserInfo("<user id>")["<user id>"]
## We can also query both mutiple users together, which returns list of `User` objects
#users = client.fetchUserInfo("<1st user id>", "<2nd user id>", "<3rd user id>")
#
#print("user's name: {}".format(user.name))
#print("users' names: {}".format([users[k].name for k in users]))
#
#
## `searchForUsers` searches for the user and gives us a list of the results,
## and then we just take the first one, aka. the most likely one:
#user = client.searchForUsers("<name of user>")[0]
#
#print("user ID: {}".format(user.uid))
#print("user's name: {}".format(user.name))
#print("user's photo: {}".format(user.photo))
#print("Is user client's friend: {}".format(user.is_friend))
#
#
## Fetches a list of the 20 top threads you're currently chatting with
#threads = client.fetchThreadList()
## Fetches the next 10 threads
#threads += client.fetchThreadList(offset=20, limit=10)
#
#print("Threads: {}".format(threads))
#
#
## Gets the last 10 messages sent to the thread
#messages = client.fetchThreadMessages(thread_id="<thread id>", limit=10)
## Since the message come in reversed order, reverse them
#messages.reverse()
#
## Prints the content of all the messages
#for message in messages:
#    print(message.text)
#
#
## If we have a thread id, we can use `fetchThreadInfo` to fetch a `Thread` object
#thread = client.fetchThreadInfo("<thread id>")["<thread id>"]
#print("thread's name: {}".format(thread.name))
#print("thread's type: {}".format(thread.type))
#
#
## `searchForThreads` searches works like `searchForUsers`, but gives us a list of threads instead
#thread = client.searchForThreads("<name of thread>")[0]
#print("thread's name: {}".format(thread.name))
#print("thread's type: {}".format(thread.type))

#Sample Thread Message
#[Message(text="Hi, it's actually working", mentions=[], emoji_size=None, uid='mid.$cAAAACmFTDQV3J2vTDVw9iaJgPTft', author='100048725596490', timestamp='1584677686029', is_read=True, read_by=['100004185035855', '100048725596490'], reactions={}, sticker=None, attachments=[], quick_replies=[], unsent=False, reply_to_id=None, replied_to=None, forwarded=False)]
#reactions={'100004185035855': MessageReaction.WOW} (ANGRY, SAD, SMILE, HEART)

#Extract text from message thread which contain other data from message

def read_last_saved_message(message_file):
    #https://stackoverflow.com/questions/46258499/read-the-last-line-of-a-file-in-python 
    with open(message_file, 'rb') as f:
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR) 
        last_line = f.readline().decode()
    return last_line

def get_user_text(user_id):
    #lim = 2
    #while 1:
        thread_message = client.fetchThreadMessages(thread_id=user_id, limit = 2)
        for messages in thread_message:
            if messages.author == user_id:
                return messages.text
            #else:
            #    lim += 1

def append_text(message_file, message):
    f=open(message_file, "a+")
    if message is None:
        pass

    f.write('\n')
    f.write(message)

def background_waiting(user_id, message_file):

    old_message = None

    while 1:
        current_message = get_user_text(user_id)
        #old_message = read_last_saved_message(message_file)
        if current_message == old_message:
            time.sleep(10)
        elif current_message == 'logout':
            client.logout()
        else:
            #append_text(message_file, current_message)
            print("\nInput: {}".format(current_message))
            bot_output = inference(current_message)
            bot_message = bot_output['answers']
            print("\nOutput: {}".format(bot_message))
            client.send(Message(bot_message), thread_id=user_id, thread_type=ThreadType.USER)
            old_message = current_message

message_file = 'messages.txt'

if __name__ == '__main__':
    #Login
    client = Client('fakecma00@gmail.com', '4akecmaisgreat')
    
    #Find a user
    user = client.searchForUsers("Adam")[0]
    user_id = user.uid
    print(user_id)

    background_waiting(user_id, message_file)
