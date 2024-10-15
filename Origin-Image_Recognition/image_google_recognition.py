#pip install google-cloud-vision
#https://mxxxn.tistory.com/9

import os
import io
from google.cloud import vision
from google.cloud.vision_v1 import types
from googletrans import Translator
translator = Translator()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'your token.json'

client = vision.ImageAnnotatorClient()
file_name = os.path.abspath(r'.\image\0.png')


#이미지 읽어오기
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()
image = vision.Image(content=content)

#이미지 feature label detection
response = client.label_detection(image=image)
labels = response.label_annotations


translated_label = []
for label in labels:
    translated_result = translator.translate(label.description, dest='ko')
    translated_label.append(translated_result.text)
print(translated_label)

