#pip install matplotlib

import os
import io
from google.cloud import vision
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import random
from googletrans import Translator

translator = Translator()

# 구글 클라우드 인증 정보 설정
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'your token.json'
client = vision.ImageAnnotatorClient()


def bounding_box_img(file_name):
    # 이미지를 메모리에 로드
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # 객체 탐지 수행
    response = client.object_localization(image=image)
    objects = response.localized_object_annotations

    im = Image.open(file_name)  # 이미지 불러오기
    draw = ImageDraw.Draw(im)

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]  # 색상 목록
    bounding_box_info = {}  # 객체 이름과 바운딩 박스 크기 저장
    output_object = []

    for object_ in objects:
        translated_name = translator.translate(object_.name, dest='ko').text

        vertices = [(vertex.x * im.width, vertex.y * im.height) for vertex in object_.bounding_poly.normalized_vertices]

        # 임의의 색상을 선택
        color = random.choice(colors)
        draw.polygon(vertices, outline=color, width=2)  # 바운딩박스 그리기

        # 바운딩 박스 크기 계산
        x_size = [vertex[0] for vertex in vertices]  # x좌표 추출
        y_size = [vertex[1] for vertex in vertices]  # y좌표 추출

        width = max(x_size) - min(x_size)
        height = max(y_size) - min(y_size)

        box_size = width * height  # 바운딩 박스 사이즈

        # 현재 이름이 딕셔너리에 있는지 확인
        if translated_name in bounding_box_info:
            # 크기가 중복되는지 확인
            if box_size not in bounding_box_info[translated_name]:
                # 이름은 같지만 크기가 다르면 리스트에 추가
                bounding_box_info[translated_name].append(box_size)
            else:
                # 이름과 크기가 모두 같으면 추가하지 않음 (중복 방지)
                continue
        else:
            # 이름이 처음 등장하거나 이름이 다를 경우 리스트로 바운딩 박스 크기 저장
            bounding_box_info[translated_name] = [box_size]
        """
        # 출력go
        print(f'\nName: {object_.name}, {translated_name}, 바운딩 박스 크기: {box_size}')
        print('Bounding polygon:')
        for vertex in vertices:
            print(f' - ({vertex[0]}, {vertex[1]})')
        print(bounding_box_info)"""

    # 바운딩 박스 차이 비교
    sorted_objects = sorted(bounding_box_info, key=lambda x: max(bounding_box_info[x]), reverse=True)

    # 가장 큰 값과 두 번째로 큰 값
    max_object = sorted_objects[0] if len(sorted_objects) > 0 else None  # 객체가 한 개도 없을경우 None 처리
    second_max_object = sorted_objects[1] if len(sorted_objects) > 1 else None  # 객체가 하나만 있을 경우 None 처리
    #print(bounding_box_info)
    # 두 값의 차이
    if second_max_object:
        difference = max(bounding_box_info[max_object]) - max(bounding_box_info[second_max_object])
        # 차이에 따라 결과 처리
        if difference is None or difference >= 20000:#1개 객체 반환
            result = max_object  # 차이가 20000 이상이면 가장 큰 객체만 반환
            max_object_count = len(bounding_box_info[max_object])
            output_object.extend([max_object, max_object_count])
        else:#2개 객체 반환
            result = [max_object, second_max_object]  # 차이가 20000 미만이면 두 객체 모두 반환
            max_object_count = len(bounding_box_info[max_object])
            second_max_object_count = len(bounding_box_info[second_max_object])
            output_object.extend([max_object, max_object_count, second_max_object, second_max_object_count])
    elif max_object:  #단일 객체일 때
        max_object_count = len(bounding_box_info[max_object])
        output_object.extend([max_object, max_object_count])
    else:#None일 때
        output_object.extend([max_object, 0])  
    
    """
    # 이미지 출력
    plt.figure(figsize=(12, 8))
    plt.imshow(im)
    plt.axis('off')  # 축 X
    plt.show()"""

    return output_object
