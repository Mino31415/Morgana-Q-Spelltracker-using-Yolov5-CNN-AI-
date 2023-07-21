import torch, win32con, win32gui, win32ui, os
import numpy as np
from time import time

model = torch.hub.load('ultralytics/yolov5', 'custom', path="model.pt", force_reload=True)
os.system("cls")

def windowCapture():
    w = 1920
    h = 1080
    
    hwnd = win32gui.FindWindow(None, 'winnable')

    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)

    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (h,w,4)


    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    img = img[...,:3]
    img = np.array(img)
    return img

cooldown = 10

while True:
    conf = 0
    used = 0

    results = model(windowCapture())
    try:
        x1, y1, x2, y2, conf = float(results.pandas().xyxy[0]['xmin']), float(results.pandas().xyxy[0]['ymin']), float(results.pandas().xyxy[0]['xmax']), float(results.pandas().xyxy[0]['ymax']), float(results.pandas().xyxy[0]['confidence'])
    except:
        pass

    if conf > 0.65:
        used = time()

    while time() < used + 10:
        print(round(used+10 - time(), 3))

    os.system("cls")
    print("Morgana Q ready")