# -*- coding: utf-8 -*-
import os
import RPi.GPIO as GPIO
import tts
import ocr
import json
import time
from dotenv import load_dotenv
from slackclient import SlackClient
from watson_developer_cloud import ConversationV1
import sys
from stt import Stt
import concept_recog
reload(sys)
sys.setdefaultencoding('utf-8')


GPIO.setmode(GPIO.BOARD)
blue = GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
white = GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

os.system('source env.sh')

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
num = 0


# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    res = conversation_client.message(workspace_id=workspace_id,
                                      message_input={'text': command},
                                      context=context)
        
    ctx = res['context']
    print ctx
    
    slack_client.api_call("chat.postMessage", channel=channel,
                                  text=res['output']['text'][0], as_user=True)

    
    if 'find' in ctx.keys() and \
        ctx['find']:
        
        print "yes find sentence"
            
    if 'read_again' in ctx.keys() and \
        ctx['read_again']:
        f = open("Output{}.txt".format(num -1 if num != 0 else num), 'r')
        print "yes read again"
        os.system('mpg321 test{}.mp3 &'.format(num-1 if num != 0 else num))
        slack_client.api_call("chat.postMessage", channel=channel,
                                  text=str(f.read()), as_user=True)
        f.close()
        
    


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    context = {}
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    workspace_id = 'fc0578fa-591b-48d5-a3a4-7fcebfb9901e'
    conversation_client = ConversationV1(
                                         username="cc711d2c-bdd3-4d5f-aaed-beba07437e4e",
                                         password="rPSSfr2B2DPW",
                                         version='2017-05-26')
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            if(GPIO.input(3) == 0):
                print("Button 1 pressed")
                text = ocr.ocr(num)
                prev_str = text
                try:
                    tts.tts(text, num)
                    num += 1
                except:
                    print("error")
                    if num != 0: num -= 1
                    continue
        
            if(GPIO.input(5) == 0):
                print("Button 2 pressed")
                tts.tts("무엇을 도와드릴까요?")
                # interact white button
                time.sleep(5)
                trans_text = Stt.call("key_word.wav")
                print trans_text
                if trans_text == "다시 읽어 줘":
                    f = str(open("Output10.txt", 'r').read())
                    print "yes read again"
                    tts.tts(f)
                    #os.system('mpg321 test{}.mp3 &'.format(num-1 if num != 0 else num))
                    slack_client.api_call("chat.postMessage", channel=channel,
                                  text=f, as_user=True)
                    f.close()
                if trans_text == "이것 좀 읽어 줄래":
                    text = ocr.ocr(num)
                    prev_str = text
                    #try:
                    tts.tts(text, num)
                    num += 1
                    #except:
                        #print e
                     #   print("error")
                      #  if num != 0: num -= 1
                    
                if trans_text == "키워드 좀 뽑아줘":
                    print "concept"
                    anl_text = concept_recog.concept_recog()
                    print anl_text
                    #slack_client.api_call("chat.postMessage", channel=channel,
                    #              text=anl_text, as_user=True)
                    tts.tts(str(anl_text))
                
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")




GPIO.cleanup()
