import cv2
from configparser import ConfigParser
import numpy

class MagniParams:
    levels: int
    alpha: int
    minFrequency: float
    maxFrequency: float
    bufferSize: int
    bufferIndex: int

    def __init__(self, levels, alpha, minFrequency, maxFrequency, bufferSize):
        self.levels = levels
        self.alpha = alpha
        
        self.minFrequency = minFrequency
        self.maxFrequency = maxFrequency

        self.bufferSize = bufferSize
    
    def __init__(self, cfg: ConfigParser):
        self.load_config(cfg)
    
    def load_config(self, cfg: ConfigParser):
        section = "ColorMagnification"

        self.levels = cfg.getint(section, "levels")
        self.alpha = cfg.getint(section, "alpha")
        
        self.minFrequency = cfg.getfloat(section, "minFrequency")
        self.maxFrequency = cfg.getfloat(section, "maxFrequency")

        self.bufferSize = cfg.getint(section, "bufferSize")
        self.bufferIndex = 0

class HeartRate:
    bpmCalculationFrequency: int
    bpmBufferIndex: int
    bpmBufferSize: int

    bpmBuffer: numpy.array

    def __init__(self, bpmCalculationFrequency, bpmBufferSize):
        self.bpmCalculationFrequency = bpmCalculationFrequency
        self.bpmBufferIndex = 0

        self.bpmBufferSize = bpmBufferSize
        self.bpmBuffer = numpy.zeros((self.bpmBufferSize))

    def __init__(self, cfg: ConfigParser):
        self.load_config(cfg)
    
    def load_config(self, cfg: ConfigParser):
        section = "CalculationParameters"

        self.bpmCalculationFrequency = cfg.getint(section, "bpmCalculationFrequency")
        self.bpmBufferIndex = 0

        self.bpmBufferSize = cfg.getint(section, "bpmBufferSize")
        self.bpmBuffer = numpy.zeros((self.bpmBufferSize))

class CalculationParams:
    firstFrame: numpy.array
    firstGauss: numpy.array
    videoGauss: numpy.array
    
    fourierTransformAvg: numpy.array
    frequencies: numpy.array
    mask: bool

    def __init__(self, video_size, magni_params, cfg):
        self.calculate(video_size, magni_params, cfg)

    def calculate(self, video_size: tuple, magni_params: MagniParams, cfg: ConfigParser):
        videoChannels = cfg.getint("Capture", "videoChannels")
        videoFrameRate = cfg.getint("Capture", "videoFrameRate")

        firstFrame = numpy.zeros((
            int(video_size[1]),
            int(video_size[0]),
            videoChannels
        ))
        firstGauss = buildGauss(firstFrame, magni_params.levels + 1)[magni_params.levels]
        videoGauss = numpy.zeros((magni_params.bufferSize, firstGauss.shape[0], firstGauss.shape[1], videoChannels))
        fourierTransformAvg = numpy.zeros((magni_params.bufferSize))

        frequencies = (1.0 * videoFrameRate) * numpy.arange(magni_params.bufferSize) / (1.0 * magni_params.bufferSize)
        mask = (frequencies >= magni_params.minFrequency) & (frequencies <= magni_params.maxFrequency)

        self.firstFrame = firstFrame
        self.firstGauss = firstGauss
        self.videoGauss = videoGauss

        self.fourierTransformAvg = fourierTransformAvg
        self.frequencies = frequencies
        self.mask = mask



def buildGauss(frame, levels):
    pyramid = [frame]

    for level in range(levels):
        frame = cv2.pyrDown(frame)
        pyramid.append(frame)
    
    return pyramid

def reconstructFrame(pyramid, index, levels):
    filteredFrame = pyramid[index]

    for level in range(levels):
        filteredFrame = cv2.pyrUp(filteredFrame)

    # probably the filter is this
    # filteredFrame = filteredFrame[:videoHeight, :videoWidth]

    return filteredFrame


def calculateBpm(frame: numpy.array, real_size: tuple, video_size: tuple, scale: float, calc_params: CalculationParams, magni_params: MagniParams, heart_rate: HeartRate):
    detectionFrame = frame[
        video_size[1] // 2:real_size[1] - video_size[1] // 2,
        video_size[0] // 2:real_size[0] - video_size[0] // 2, :
    ]

    # Construct Gaussian Pyramid
    calc_params.videoGauss[magni_params.bufferIndex] = buildGauss(detectionFrame, magni_params.levels + 1)[magni_params.levels]
    fourierTransform = numpy.fft.fft(calc_params.videoGauss, axis=0)

    fourierTransform[calc_params.mask == False] = 0

    if magni_params.bufferIndex % heart_rate.bpmCalculationFrequency == 0:
        for buf in range(magni_params.bufferSize):
            calc_params.fourierTransformAvg[buf] = numpy.real(fourierTransform[buf]).mean()
        
        hz = calc_params.frequencies[numpy.argmax(calc_params.fourierTransformAvg)]
        bpm = 60.0 * hz

        heart_rate.bpmBuffer[heart_rate.bpmBufferIndex] = bpm
        heart_rate.bpmBufferIndex = (heart_rate.bpmBufferIndex + 1) % heart_rate.bpmBufferSize

    magni_params.bufferIndex = (magni_params.bufferIndex + 1) % magni_params.bufferSize

    return heart_rate.bpmBuffer.mean()