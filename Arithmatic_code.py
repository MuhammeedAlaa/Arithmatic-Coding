import numpy as np
import cv2


def Arithmetic_coding_decode(codes, input_prob):
    size = int(n * m / block_size) + int(n * m % block_size)
    out_code = np.zeros(
        (size, block_size))
    for i in range(len(codes)):
        for j in range(block_size):
            high_index = np.argmax(input_prob > codes[i])

            high = input_prob[high_index]
            if high_index != 0:
                low_index = high_index - 1
                low = input_prob[low_index]
            else:
                low = 0
            out_code[i, j] = high_index
            current_range = high - low
            if current_range != 0:
                codes[i] = (codes[i] - low) / current_range
    return out_code


def Arithmetic_coding_encode(input_codes, input_prob):
    low = 0
    high = 1
    range = 1
    for code in input_codes:
        high = low + range * input_prob[code]
        if code != 0:
            low = low + range * input_prob[code - 1]
        else:
            low = low
        range = high - low
    return (high + low)/2


img = cv2.imread('baboon.bmp', cv2.IMREAD_GRAYSCALE)
n = len(img)
m = len(img[0])
block_size = int(input("Please enter the block size: "))
type_num = int(
    input("Please enter '0' for float16 '1' for float32 '2' for float64 (default is float16): "))
type = np.float16
if type_num == 1:
    type = np.float32
elif type_num == 2:
    type = np.float64
flattened_img = img.flatten()
flattened_size = int((n * m) % block_size) + int((n * m) / block_size)
prob = np.zeros(256, type)

for greylevel in flattened_img:
    prob[greylevel] = prob[greylevel] + 1
prob = [freq / (n * m) for freq in prob]
for pixel in range(0, len(prob)):
    if pixel != 0:
        prob[pixel] += prob[pixel - 1]
codes = np.zeros(flattened_size, type)
start = 0
end = block_size
for index in range(0, flattened_size):
    if end < len(flattened_img):
        code = Arithmetic_coding_encode(
            flattened_img[(start):(end)], prob)
        end += block_size
        start += block_size
        codes[index] = code
    else:
        code = Arithmetic_coding_encode(
            flattened_img[start:(flattened_size)], prob)
        break
encoded = np.array(codes, type)
# encode
np.save('encoded.npy', encoded)
np.save('prob.npy', prob)
# decode
probb = np.load('prob.npy')
codess = np.load('encoded.npy')
decoded = Arithmetic_coding_decode(codess, prob)
if (len(decoded) * len(decoded[0])) == n * m:
    decoded = decoded.reshape(n, m)
    cv2.imwrite('output.bmp', decoded)
else:
    out = np.zeros(n * m, type)
    decoded = decoded.flatten()
    for i in range(len(out)):
        out[i] = decoded[i]
    out = out.reshape(n, m)
    cv2.imwrite('output.bmp', out)
