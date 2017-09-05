# [START import_libraries]
import argparse
import io
import os

from google.cloud import speech

#import record

# [END import_libraries]


class Stt(object):
    @staticmethod
    def call(path='test.wav'):
        #stt.record_wav(path)
        path = os.path.join(os.getcwd(), path)
        final = Stt.transcribe_file(path)
        return final

    #@staticmethod
    #def record_wav(name='test.wav'):
    #   print("please speak a word into the microphone")
    #    record.record_to_file('test.wav')
    #    print("done - result written to test.wav")

    @staticmethod
    def transcribe_file(speech_file):
        client = speech.Client()
        # sample = client.sample(source_uri='gs://komodocloud/test.flac',
        #                        encoding=speech.Encoding.FLAC,
        #                        sample_rate_hertz=44100)
        with io.open(speech_file, 'rb') as audio_file:
            content = audio_file.read()
        sample = client.sample(content=content,
                               encoding=speech.Encoding.LINEAR16,
                               sample_rate_hertz=44100)
        results = sample.recognize(
            language_code='ko-KR', max_alternatives=2)
        str_list = []
        for i, result in enumerate(results):
            print("reslut", i)
            for alternative in result.alternatives:
                print('=' * 20)
                print('transcript: ' + alternative.transcript)
                print('confidence: ' + str(alternative.confidence))
                str_list.append(alternative.transcript)
        print str_list[0]
        return str_list[0]


if __name__ == '__main__':
    sst.call()
