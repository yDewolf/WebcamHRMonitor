import cv2

def get_cam_by_index(i):
    cam = cv2.VideoCapture(i)

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
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def check_multiple():
    for i in range(-1,10):
        try:
            print(f'checking camera #{i}')
            check_cam_by_index(i)
        except:
            continue

def set_cam_size(cam, width, height):
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)