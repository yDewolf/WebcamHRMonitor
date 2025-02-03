import configparser
import cv2

from utils.hr_monitor import HRMonitor

CONFIG_PATH = "config.ini"

cfg = configparser.ConfigParser()
cfg.read(CONFIG_PATH)

heart_rate_monitor = HRMonitor(cfg)

fps = 15
loop_delta = 1./fps

frequency = int(cfg.get("CalculationParameters", "bpmCalculationFrequency"))

i = 0
while True:
    heart_rate_monitor.update()
    i = i + 1

    if i >= frequency:
        print(heart_rate_monitor.current_bpm)
        i = 0

heart_rate_monitor.cam.release()
cv2.destroyAllWindows()