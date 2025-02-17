import cv2
from utils.camera_utils import get_cam_by_index, set_cam_size

from configparser import ConfigParser
from utils.gauss_helper import MagniParams, CalculationParams, HeartRate, calculateBpm

class HRMonitor:
    cam: cv2.VideoCapture
    real_size: tuple
    video_size: tuple
    scale: float

    magni_params: MagniParams
    calculation_params: CalculationParams
    heart_rate: HeartRate

    current_bpm: int

    def __init__(self, cfg: ConfigParser):
        self.load_config(cfg)
    
    def load_config(self, cfg: ConfigParser):
        cameraIndex = cfg.getint("Capture", "CameraIndex")
        cam = get_cam_by_index(cameraIndex)
        scale = cfg.getfloat("Capture", "ScaleCameraBy")

        real_size = (int(cam.get(cv2.CAP_PROP_FRAME_WIDTH) * scale), int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale))

        set_cam_size(cam, real_size[0], real_size[1])

        video_size = (int(real_size[0] * scale * 2), int(real_size[1] * scale * 2))

        self.cam = cam
        self.real_size = real_size
        self.video_size = video_size
        self.scale = scale

        self.magni_params = MagniParams(cfg)
        self.calculation_params = CalculationParams(video_size, self.magni_params, cfg)
        self.heart_rate = HeartRate(cfg)
        self.current_bpm = -1
    
    def update(self):
        ret, frame = self.cam.read()
        if ret == False:
            return

        self.current_bpm = calculateBpm(frame, self.real_size, self.video_size, self.scale, self.calculation_params, self.magni_params, self.heart_rate)