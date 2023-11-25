import cv2

# 加载视频
cap = cv2.VideoCapture("data/video/cut.mkv")
# 创建mog对象：去除图像的背景
mog = cv2.bgsegm.createBackgroundSubtractorMOG()
# 构造5×5的结构元素，结构为十字形
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
# 设定车辆外接矩形框的最小宽度和最小高度
min_w = 150
min_h = 140
# 设定计数线的高度
line_high = 500
# 偏移量
offset = 5
# 对车计数
carnum = 0

# 保存视频
# # 参数：（保存路径，编码器，帧率，画面尺寸，是否彩色）
# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取视频的宽度
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取视频的高度
# fps = cap.get(cv2.CAP_PROP_FPS)  # 获取视频的帧率
# fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))  # 视频的编码
#
# out = cv2.VideoWriter(".\\data\\cars1_final1.mp4", fourcc, fps, (width, height), True)

# 循环读取视频帧
while True:
    # 第一个参数ret 为True 或者False,代表有没有读取到图片
    # 第二个参数frame表示截取到一帧的图片
    ret, frame = cap.read()
    # 通过设置缩放比例对图像进行放大或缩小, (这里若对窗口的粗存更改，则会使矩形框的位置失真)
    # dst = cv2.resize(frame, None, fx=0.8, fy=0.8, interpolation=cv2.INTER_CUBIC)
    if ret is True:
        # 将原始帧灰度化
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 高斯滤波去噪：卷积核为3*3，
        blur = cv2.GaussianBlur(gray, (3, 3), 5)
        # 获取去背景后的数据
        mask = mog.apply(blur)
        # 腐蚀:卷积核对应的原图的所有像素值为1吗，那么中心元素像素值不变，否则变为0. ”扩大黑色部分，减小白色部分。“
        erode = cv2.erode(mask, kernel)
        # 膨胀：卷积核对应的与图像像素值中只要有一个是1，中心像素值就为1.
        dilate = cv2.dilate(erode, kernel, iterations=1)
        # 闭运算：先膨胀后腐蚀：用于填充白色物体内细小黑色空洞的区域（ 消除内部小块）
        close = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
        # 查找轮廓:
        # cv2.findContours(img, mode, method):cv2.RETR_EXTERNAL只检测外轮廓;cv2.RETR_LIST检测的轮廓不建立等级关系。
        contours, h = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 画出检测线
        cv2.line(frame, (0, line_high), (1280, line_high), (255, 255, 0), 2)
        # 画出所有检测出的轮廓
        for contour in contours:
            # 获得外接矩形的四个数据点：x轴坐标，y轴坐标，矩形的宽，矩形的高
            (x, y, w, h) = cv2.boundingRect(contour)
            # 通过外接矩形的宽高大小来过滤小矩形
            if not ((w >= min_w) and (h >= min_h)):
                continue
            if (w > min_w) and (h > min_h):  # 这里只计算正常的汽车
                # 画外接矩形的轮廓 ：(0, 255, 0)：颜色   2：线条的粗细
                cv2.rectangle(frame, (x, y), (x+w, y + h), (0, 0, 255), 1)
                # 把车抽象为一点，要通过外接矩形计算矩形的中心点
                cx = int(x + 0.5 * w)
                cy = int(y + 0.5 * h)
                # 画中心圆点
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                # 判断汽车是否过检测线
                if(line_high - offset) < cy < (line_high + offset):
                    carnum += 1  # 落入有效区间，计数+1
                    print(carnum)

        # cv2.imshow('video1', frame)
        # cv2.imshow('video2', dst)
        # cv2.imshow('video3', gray)
        # cv2.imshow('video4', blur)
        # cv2.imshow('video5', mask)
        # cv2.imshow('video6', erode)
        # cv2.imshow('video7', dilate)
        # cv2.imshow('video8', close)
        cv2.putText(frame, 'Vehicle Count:' + str(carnum), (420, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
        cv2.imshow('frame', frame)
        # 保存视频帧到视频容器
        # out.write(frame)
    key = cv2.waitKey(50)
    # 按ESC退出
    if key == 27:
        break
# 释放资源
cap.release()
cv2.destroyALLWindows()

