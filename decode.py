import numpy as np
import cv2

block_size = 8
n = 426
m = 640
prob = np.load('prob.npy')
codess = np.load('encoded.npy')


def Arithmetic_coding(codes, input_prob):
    out_code = np.zeros((int(n * m / block_size), block_size))
    for i in range(len(codes)):
        for j in range(block_size):
            high_index = np.argmax(input_prob > codes[i])
            high = prob[high_index]
            if high_index != 0:
                low_index = high_index - 1
                low = input_prob[low_index]
            else:
                low = 0
            out_code[i, j] = high_index
            current_range = high - low
            codes[i] = (codes[i] - low) / current_range
    return out_code


img = Arithmetic_coding(codess, prob)
img = img.reshape(n, m)
cv2.imwrite('output.jpg', img)
