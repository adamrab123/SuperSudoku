import cv2
import numpy as np
import Queue

im = cv2.imread("source.jpeg")

class Digit(object):
    '''
    Extracts the digit from a cell.
    Implements the classic `Largest connected component` algorithm.
    '''

    def __init__(self, image):
        self.graph = image.copy()
        self.W, self.H = self.graph.shape
        self.visited = [[False for _ in xrange(
            self.H)] for _ in xrange(self.W)]
        self.digit = [[None for _ in xrange(self.H)] for _ in xrange(self.W)]
        self.buildDigit()

    def buildDigit(self):
        componentId = 0
        A, C = self.H / 4, 3 * self.H / 4 + 1
        B, D = self.W / 4, 3 * self.W / 4 + 1
        for i in xrange(A, C):
            for j in xrange(B, D):
                if not self.visited[i][j]:
                    self.bfs(i, j, componentId)
                    componentId += 1
        componentSizes = [0 for _ in xrange(componentId)]
        for row in self.digit:
            for cell in row:
                if cell is not None:
                    componentSizes[cell] += 1
        largest = componentSizes.index(max(componentSizes))
        for i in xrange(self.H):
            for j in xrange(self.W):
                self.digit[i][j] = 255 if self.digit[i][j] == largest else 0
        self.digit = np.asarray(self.digit, dtype=np.uint8)

    def bfs(self, i, j, num):
        q = Queue.Queue()
        q.put((i, j))
        while not q.empty():
            i, j = q.get()
            inValidRow = i not in xrange(0, self.H)
            inValidCol = j not in xrange(0, self.W)
            invalidCell = inValidRow or inValidCol
            invalidPixel = invalidCell or self.graph[i][j] != 255
            if invalidPixel or self.visited[i][j]:
                continue
            self.digit[i][j] = num
            self.visited[i][j] = True
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    q.put((i + di, j + dj))

def thresholdify(img):
    img = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 3)
    return 255 - img

def show(img, windowName='Image'):
    screen_res = 1280.0, 720.0
    scale_width = screen_res[0] / img.shape[1]
    scale_height = screen_res[1] / img.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0] * scale)

    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windowName, window_width, window_height)

    cv2.imshow(windowName, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def Canny(image):
        edges = cv2.Canny(image, 100, 200)
        show(edges)
        return edges

def dilate(image, kernel):
        cv2.dilate(image, kernel)
        return image

def largestContour(image):
    contours, h = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return max(contours, key=cv2.contourArea)

def make_it_square(image, side_length=306):
    return cv2.resize(image, (side_length, side_length))

def cut_out_sudoku_puzzle(image, contour):
    x, y, w, h = cv2.boundingRect(contour)
    image = image[y:y + h, x:x + w]
    return make_it_square(image, min(image.shape))

def approx(cnt):
        peri = cv2.arcLength(cnt, True)
        app = cv2.approxPolyDP(cnt, 0.01 * peri, True)
        return app

def largest4SideContour(image):
    contours, h = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for cnt in contours[:min(5,len(contours))]:
        #im = image.copy()
        #cv2.drawContours(im, cnt, -1, (255,255,255), 5)
        #self.show(im,'contour')
        if len(approx(cnt)) == 4:
            return cnt
    return None

def get_rectangle_corners(cnt):
    pts = cnt.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point has the smallest sum whereas the
    # bottom-right has the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # compute the difference between the points -- the top-right
    # will have the minumum difference and the bottom-left will
    # have the maximum difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def warp_perspective(rect, grid):
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

    # ...and now for the height of our new image
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

    # take the maximum of the width and height values to reach
    # our final dimensions
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))

    # construct our destination points which will be used to
    # map the screen to a top-down, "birds eye" view
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # calculate the perspective transform matrix and warp
    # the perspective to grab the screen
    M = cv2.getPerspectiveTransform(rect, dst)
    warp = cv2.warpPerspective(grid, M, (maxWidth, maxHeight))
    return make_it_square(warp)

def clean(cell):
    contour = largestContour(cell.copy())
    x, y, w, h = cv2.boundingRect(contour)
    cell = make_it_square(cell[y:y + h, x:x + w], 28)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    cell = cv2.morphologyEx(cell, cv2.MORPH_CLOSE, kernel)
    cell = 255 * (cell / 130)
    return cell

def extractCells(sudoku):
    cells = []
    W, H = sudoku.shape
    cell_size = W / 9
    i, j = 0, 0
    for r in range(0, W, cell_size):
        row = []
        j = 0
        for c in range(0, W, cell_size):
            cell = sudoku[r:r + cell_size, c:c + cell_size]
            cell = make_it_square(cell, 28)
            #self.helpers.show(cell, 'Before clean')
            cell = clean(cell)
            digit = Digit(cell).digit
            #self.helpers.show(digit, 'After clean')
            digit = centerDigit(digit)
            #self.helpers.show(digit, 'After centering')
            row.append(digit // 255)
            j += 1
        cells.append(row)
        i += 1
    return cells

def centerDigit(digit):
    digit = centerX(digit)
    digit = centerY(digit)
    return digit

def getTopLine(image):
    for i, row in enumerate(image):
        if np.any(row):
            return i
    return None

def getBottomLine(image):
    for i in xrange(image.shape[0] - 1, -1, -1):
        if np.any(image[i]):
            return i
    return None

def getLeftLine(image):
    for i in xrange(image.shape[1]):
        if np.any(image[:, i]):
            return i
    return None

def getRightLine(image):
    for i in xrange(image.shape[1] - 1, -1, -1):
        if np.any(image[:, i]):
            return i
    return None

def rowShift(image, start, end, length):
    shifted = np.zeros(image.shape)
    if start + length < 0:
        length = -start
    elif end + length >= image.shape[0]:
        length = image.shape[0] - 1 - end

    for row in xrange(start, end + 1):
        shifted[row + length] = image[row]
    return shifted

def colShift(image, start, end, length):
    shifted = np.zeros(image.shape)
    if start + length < 0:
        length = -start
    elif end + length >= image.shape[1]:
        length = image.shape[1] - 1 - end

    for col in xrange(start, end + 1):
        shifted[:, col + length] = image[:, col]
    return shifted

def centerX(digit):
    topLine = getTopLine(digit)
    bottomLine = getBottomLine(digit)
    if topLine is None or bottomLine is None:
        return digit
    centerLine = (topLine + bottomLine) >> 1
    imageCenter = digit.shape[0] >> 1
    digit = rowShift(digit, start=topLine, end=bottomLine, length=imageCenter - centerLine)
    return digit

def centerY(digit):
    leftLine = getLeftLine(digit)
    rightLine = getRightLine(digit)
    if leftLine is None or rightLine is None:
        return digit
    centerLine = (leftLine + rightLine) >> 1
    imageCenter = digit.shape[1] >> 1
    digit = colShift(digit, start=leftLine, end=rightLine, length=imageCenter - centerLine)
    return digit

# preprocess
print('Preprocessing...')
image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
image2 = thresholdify(image)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
image3 = cv2.morphologyEx(image2, cv2.MORPH_CLOSE, kernel)
print('done.')

# cv2.imshow("After Preprocessing", image3)

# sudoku = self.cropSudoku()
print('Cropping out Sudoku...')
contour = largestContour(image3.copy())
sudoku = cut_out_sudoku_puzzle(image3.copy(), contour)
print('done.')

# cv2.imwrite("crop.jpg", sudoku)

# sudoku = self.straighten(sudoku)
print('Straightening image...')
largest = largest4SideContour(sudoku.copy())
app = approx(largest)
corners = get_rectangle_corners(app)
sudoku = warp_perspective(corners, sudoku)
print('done.')

# cv2.imwrite("straight.jpg", sudoku)

# self.cells = Cells(sudoku).cells

print('Extracting cells...')
cells = extractCells(sudoku)
print ('done.')

print(len(cells))

i = 0
for cell in cells:
	cv2.imwrite("test/image%d.jpg" % i, cell)
	i += 1

cv2.imwrite("image.jpg", sudoku)
cv2.waitKey()
cv2.destroyAllWindows()
