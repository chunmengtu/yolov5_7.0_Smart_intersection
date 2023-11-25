import cv2
import numpy as np


def add_line(video_path, output_path, x1, y1, x2, y2, color, thickness=1):
    """
    给视频添加线条

    参数:
        video_path: 输入视频的路径
        output_path: 输出视频的路径
        x1, y1: 线条的起点坐标
        x2, y2: 线条的终点坐标
        color: 线条的颜色，例如(0, 255, 0)表示绿色
        thickness: 线条的粗细
    """
    # 读取视频
    video = cv2.VideoCapture(video_path)

    # 获取视频的基本信息，例如帧率和分辨率
    fps = int(video.get(cv2.CAP_PROP_FPS))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 创建一个黑色背景的图像，用于绘制线条
    line_img = np.zeros((height, width, 3), dtype=np.uint8)

    # 循环遍历每一帧
    while True:
        ret, frame = video.read()
        if not ret:
            break  # 读取完毕

        # 在当前帧上绘制线条
        cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)

        # # 保存或显示结果
        # cv2.imshow('Frame', line_img)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # 保存结果为视频
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    for i in range(len(line_img)):
        out.write(line_img[i])
    out.release()


# 使用示例
video_path = r'E:\PycharmProjects\yolov5_7.0_cp\demo\rec_result\cut.mp4'
output_path = r'E:\PycharmProjects\yolov5_7.0_cp\demo\rec_result\cuts.mp4'
add_line(video_path, output_path, 2, 1099, 2007, 901, (0, 255, 255), thickness=2)
