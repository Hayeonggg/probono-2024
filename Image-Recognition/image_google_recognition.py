#pip install google-cloud-vision
#https://mxxxn.tistory.com/9

import os
import io
from google.cloud import vision
from google.cloud.vision_v1 import types
from googletrans import Translator

def label_img(file_name):
    # Translator 객체 생성
    translator = Translator()

    # Google Vision API 사용을 위한 설정
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'your token.json'

    # Vision API 클라이언트 생성
    client = vision.ImageAnnotatorClient()

    # 이미지 읽어오기
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # 이미지에서 feature label detection 수행
    response = client.label_detection(image=image)
    labels = response.label_annotations

    # 번역된 label 저장
    translated_label = []
    for label in labels:
        translated_result = translator.translate(label.description, dest='ko')
        translated_label.append(translated_result.text)
    
    # 번역된 label 출력
    #print(translated_label)
    return translated_label
