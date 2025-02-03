import cv2 as cv

def get_cam_by_index(i):
    cam = cv.VideoCapture(i)
    cam.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    if not cam.isOpened():
        print("Cannot open camera")
        exit()

    return cam

def check_cam_by_index(i):
    cap = get_cam_by_index(i)
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        cv.imshow('frame',frame)
        if cv.waitKey(1) == ord('q'):
            break
    
    cap.release()
    cv.destroyAllWindows()

def check_multiple():
    for i in range(-1,10):
        try:
            print(f'checking camera #{i}')
            check_cam_by_index(i)
        except:
            continue