# -*- coding: utf-8 -*-
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1 as nlu
import watson_developer_cloud.natural_language_understanding.features.v1 \
  as Features


def concept_recog(path='./test.txt'):
    #with open(path, 'rt', encoding='utf-8') as f:
    #    inputs = f.read()
    with open(path, 'rb') as f:
        inputs = f.read().decode("UTF-8")
    
    natural_language_understanding = nlu(
        url=("https://gateway.aibril-watson.kr/" +
             "natural-language-understanding/api"),
        username="01fc633a-01c2-486e-a202-44a3b7653a1d",
        password="wwbFwHfLV4jK",
        version="2017-02-27")

    response = natural_language_understanding.analyze(
        text=inputs,
        features=[
            Features.Concepts(
                # Concepts options
                limit=3
                )
            ]
        )

    # print(json.dumps(response))
    texts = response['concepts']
    text_list = []
    for text in texts:
        text_list.append(text['text'])
    for text in text_list:
        print(text)
    return ' '.join(text_list)
if __name__ == '__main__':
    concept_recog()
