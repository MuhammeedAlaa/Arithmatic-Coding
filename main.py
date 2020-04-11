import numpy as np
import cv2
import math


def Arithmetic_coding(input_codes, input_prob):
    low = 0.0
    high = 1.0
    rang = 1.0
    for code in input_codes:
        if code != 0:
            low = low + rang * input_prob[code - 1]
            high = low + rang * (input_prob[code] - input_prob[code - 1])
        else:
            high = low + rang * input_prob[code]
        rang = high - low
    return (low + high) / 2


img = cv2.imread('test.jpg', cv2.IMREAD_GRAYSCALE)
n = len(img)
m = len(img[0])
block_size = 13
flattened_img = img.flatten()
flattened_size = int((n * m) % block_size) + int((n * m) / block_size)
prob = np.array([0] * 255)

for greylevel in flattened_img:
    prob[greylevel] = prob[greylevel] + 1
prob = [freq / (n * m) for freq in prob]
for pixel in range(0, len(prob)):
    if pixel != 0:
        prob[pixel] += prob[pixel - 1]
codes = ([0] * flattened_size)
start = 0
end = 16
for index in range(0, flattened_size):
    if end < len(flattened_img):
        code = Arithmetic_coding(
            flattened_img[(start):(end)], prob)
        end += block_size
        start += block_size
        codes[index] = code
    else:
        code = Arithmetic_coding(flattened_img[start:(flattened_size)], prob)
        break
encoded = np.array(codes)
np.save('encoded.npy', encoded)
cv2.imshow('test', img)
