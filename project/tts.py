# -*- coding: utf-8 -*-
import os
import sys
from six.moves import urllib



def tts(encText = "에러", num=0):
    client_id = "NzR96AKKrHbf8Pv4kn9N"
    client_secret = "lKqkMb_9iM"
    data = "speaker=jinho&speed=0&text=" + encText
    url = "https://openapi.naver.com/v1/voice/tts.bin"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()
    if(rescode==200):
        print("TTS mp3 저장")
        response_body = response.read()
        with open('test{}.mp3'.format(num), 'wb') as f:
            f.write(response_body)
        os.system('mpg321 test{}.mp3 &'.format(num))
    else:
        print("Error Code:" + rescode)
    
