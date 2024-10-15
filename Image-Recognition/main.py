from image_google_recognition import label_img
from image_BLIP_description import description_img
from image_google_recognition_BOX import bounding_box_img
import time

# 파일 경로 설정
#file_name = 'image/0.png'
for i in range(0,23):  # 0부터 21까지 반복
    file_name = f'image/{i}.png'


    start_time = time.perf_counter()#타이머시작
    ### 함수 호출
    label = label_img(file_name)
    BoundingBox = bounding_box_img(file_name)
    Description = description_img(file_name)
    ###
    end_time = time.perf_counter()#타이머 종료


    print(f'\n===RESULT {i}===')
    print(label)
    print(BoundingBox)
    print(Description)

    #소요 시간 계산
    elapsed_time = end_time - start_time
    print(f"코드 실행 시간: {elapsed_time:.6f}초\n")
