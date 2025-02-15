import cv2
import os
import yaml
# Initialize lists to store image paths and labels
label = [-1, -1]
zoom_factor = 1.0  # 初始缩放比例
zooming = False  # 是否正在缩放
def mouse_callback(event, x, y, flags, param):
    global img, zoom_factor, zooming
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Clicked at (x, y): ({x}, {y})")
        label[0] = x; label[1] = y
        cv2.circle(img, (label[0], label[1]), radius=2, color=(0, 0, 255), thickness=-1)
        cv2.imshow("Label Gauze", img)
    if event == cv2.EVENT_RBUTTONDOWN:
        cv2.destroyWindow("Label Gauze")
    if event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:  # 向上滚动，放大
            zoom_factor *= 1.1
        else:  # 向下滚动，缩小
            zoom_factor /= 1.1
        zooming = True

    # 右键点击：关闭窗口
    if event == cv2.EVENT_RBUTTONDOWN:
        cv2.destroyWindow("Label Gauze")
# Iterate through images in a folder
image_folder = "test_needle/images"
for img_name in os.listdir(image_folder):
    img_path = os.path.join(image_folder, img_name)
    img = cv2.imread(img_path)
    print(img.shape)
    # Create a window and set mouse callback
    cv2.namedWindow("Label Gauze")
    cv2.setMouseCallback("Label Gauze", mouse_callback)
    while True:
        if zooming:
            # 根据缩放比例调整图像大小
            h, w = img.shape[:2]
            resized_img = cv2.resize(img, (int(w * zoom_factor), int(h * zoom_factor)), interpolation=cv2.INTER_LINEAR)
            cv2.imshow("Label Gauze", resized_img)
            zooming = False

        key = cv2.waitKey(1)  # 等待按键

        if key == ord('q'):  # 按下 'q' 键退出标注
            break
    
    name = os.path.splitext(img_name)[0]
    label_data = dict(
        x= label[0],
        y= label[1]
    )
    with open(os.path.join("test_needle/labels/",f"{name}.yaml"), "w") as f:
        yaml.dump(label_data, f)


cv2.destroyAllWindows()