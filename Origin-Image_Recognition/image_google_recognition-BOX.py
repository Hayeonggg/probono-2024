#pip install matplotlib

import os
import io
from google.cloud import vision
from google.cloud.vision_v1 import types
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import random
from googletrans import Translator
translator = Translator()

# 구글 클라우드 인증 정보 설정
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'your token.json'

client = vision.ImageAnnotatorClient()

# 이미지 파일의 경로 설정
file_name = os.path.abspath('image/0.png')

# 이미지를 메모리에 로드
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)


# 객체 탐지 수행
response = client.object_localization(image=image)
objects = response.localized_object_annotations

im = Image.open(file_name)#이미지 불러오기
draw = ImageDraw.Draw(im)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]#색상 목록 
bounding_box_sizes = {} #바운딩박스 크기 비교(주체 찾기)
bounding_box_count = {}
output_object = []


print('Objects and bounding boxes:')
for object_ in objects:
    translated_name = translator.translate(object_.name, dest='ko')
    translated_name = translated_name.text
    
    vertices = [(vertex.x * im.width, vertex.y * im.height) for vertex in object_.bounding_poly.normalized_vertices]


    #임의의 색상을 선택
    color = random.choice(colors)
    draw.polygon(vertices, outline=color, width=2)#바운딩 박스 그리기
    
    #바운딩박스 크기 계산
    x_size = [vertex[0] for vertex in vertices]#x좌표 추출
    y_size = [vertex[1] for vertex in vertices]#y좌표 추출
    
    width = max(x_size)-min(x_size)
    height = max(y_size)-min(y_size)
    
    box_size = width * height#바운딩 박스 사이즈
    bounding_box_sizes[translated_name] = box_size
    
    #바운딩 개수 카운트
    if translated_name in bounding_box_count:
        bounding_box_count[translated_name] += 1
    else:
        bounding_box_count[translated_name] = 1
    
    print(f'\nName :  {object_.name}, {translated_name},  바운딩 박스 크기 : {box_size}')
    print('Bounding polygon:')
    for vertex in vertices:
        print(f' - ({vertex[0]}, {vertex[1]})')

#바운딩박스 차이 비교
sorted_objects = sorted(bounding_box_sizes, key=bounding_box_sizes.get, reverse=True)

#가장 큰 값과 두 번째로 큰 값
max_object = sorted_objects[0] if len(sorted_objects) > 0 else None  #객체가 한 개도 없을경우 None 처리
second_max_object = sorted_objects[1] if len(sorted_objects) > 1 else None  # 객체가 하나만 있을 경우 None 처리

#두 값의 차이
if second_max_object:#2개이상 객체일때
    difference = bounding_box_sizes[max_object] - bounding_box_sizes[second_max_object]
    #차이에 따라 결과 처리
    if difference is None or difference >= 20000:
        result = max_object  # 차이가 20000 이상이면 가장 큰 객체만 반환
        max_object_count = bounding_box_count.get(result, 0)
        output_object.extend([result, max_object_count])
    else:
        result = [max_object, second_max_object]  # 차이가 20000 미만이면 두 객체 모두 반환
        max_object_count = bounding_box_count.get(max_object, 0)
        second_max_object_count = bounding_box_count.get(second_max_object, 0)
        output_object.extend([max_object, max_object_count, second_max_object, second_max_object_count])
else: #단일 객체일때
    max_object_count = bounding_box_count.get(max_object, 0)
    output_object.extend([max_object, max_object_count])  
    

print(output_object)



#이미지 출력
plt.figure(figsize=(12, 8))
plt.imshow(im)
plt.axis('off')#축X
plt.show()
