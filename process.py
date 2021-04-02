import numpy as np
import cv2
import imageio

np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=1500)

global height
global width


def process_image():
    global scale
    scale = 30
    # read the image, the width & the length
    x, y = cv2.imread('static/pic/Original.png'), imageio.imread('area.png')
    x, y = np.asarray(x), np.asarray(y)
    global height, width
    height, width = x.shape[0], x.shape[1]

    y = y.reshape(-1, 4)
    a1, a2, a3, area = np.hsplit(y, 4)
    area = area.reshape(height, -1)
    r, g, b = cv2.split(x)
    r = process(r, area)
    g = process(g, area)
    b = process(b, area)

    img = cv2.merge([r, g, b])
    cv2.imwrite('static/pic/output.png', img)


def process(matrix: np, area: np):
    print(np.array(find_location(area)).shape)
    for location in find_location(area):
        print(location)
        mosaic(matrix, location[0], location[1])
    return matrix


def find_location(matrix: np):
    my_list = []
    for v_pt in range(height // scale + 1):
        for h_pt in range(width // scale + 1):
            if matrix[min((v_pt * scale + scale // 2, height - 2))][min((h_pt * scale + scale // 2), width - 2)] == 255:
                my_list.append([v_pt, h_pt])
    return my_list


def mosaic(matrix: np, v_pt, h_pt):
    sum, count = 0, 0
    for i in range(v_pt * scale, min((v_pt + 1) * scale, height)):
        for j in range(h_pt * scale, min((h_pt + 1) * scale, width)):
            sum += matrix[i][j]
            count += 1
    # exception handler
    if count == 0:
        result = 0
    else:
        result = sum // count
    for i in range(v_pt * scale, min((v_pt + 1) * scale, height)):
        for j in range(h_pt * scale, min((h_pt + 1) * scale, width)):
            matrix[i][j] = result
    return matrix
