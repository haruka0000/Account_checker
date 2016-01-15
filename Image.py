import cv2

def matching(self):

    im = cv2.imread('/to/image/path/image.jpg', cv2.IMREAD_GRAYSCALE) # 比較するImageFile
    image_hist = cv2.calcHist([im], [0], None, [256], [0, 256])

    target = self.compare_target_hist(image_hist)

    result = []

    while True:
        try:
            result.append(target.next())

        except StopIteration:
            break

    result.sort(reverse=True)

    return result[0][1]

# 比較されるImageFile
def gen_target(self):
    yield "to/image/path/4.jpg"
    yield "to/image/path/3.jpg"
    yield "to/image/path/5.jpg"
    yield "to/image/path/2.jpg"
    yield "to/image/path/1.jpg"

def compare_target_hist(self, image_hist):

    target_files = self.gen_target()

    while True:
        try:
            target_file = target_files.next()
            im = cv2.imread(target_file, cv2.IMREAD_GRAYSCALE)
            target_hist = cv2.calcHist([im], [0], None, [256], [0, 256])
            yield (self.compare_hist(image_hist, target_hist), target_file)

        except StopIteration:
            break

# ヒストグラムを比較の計算をしている
def compare_hist(self, hist1, hist2):
    total = 0
    for i in range(len(hist1)):
        total += min(hist1[i], hist2[i])
    return float(total) / sum(hist1)


if __name__ == '__main__':
    matching()
