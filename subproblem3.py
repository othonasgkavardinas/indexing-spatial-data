from sys import argv


class PriorityQueue(object):
    def __init__(self):
        self.queue = [None]
        self.dict = {}
        self.blocks_used = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def isEmpty(self):
        return len(self.queue)-1 == 0

    def length(self):
        return len(self.queue)-1

    def insert(self, data, q, s):
        distance = -1

        if type(data) is tuple:
            distance = calc_block_dist(data, q, s)
        if type(data) is Point:
            distance = calc_eucl_dist(q, data)

        if distance not in self.dict:
            self.dict[distance] = []

        self.dict[distance].append(data)

        self.queue.append(distance)
        self.fixUp(len(self.queue)-1)

    def popMin(self, q, s):

        min1 = self.queue[1]
        result = self.dict[min1][0]
        self.swap(1, len(self.queue)-1)
        self.queue.pop()
        self.dict[min1].pop(0)
        self.fixDown(1)

        if type(result) is tuple:
            self.insert_neighbour_blocks(result, q, s)
            self.insert_block_points(s, result, q)
            return None

        return result

    def insert_neighbour_blocks(self, tuple1, q, s):
        if tuple1[0] == 0:
            if tuple1[1] == 0:
                self.check_insert((tuple1[0]+1, tuple1[1]), q, s)
                self.check_insert((tuple1[0], tuple1[1]+1), q, s)
                self.check_insert((tuple1[0]+1, tuple1[1]+1), q, s)
            elif tuple1[1] == 9:
                self.check_insert((tuple1[0]+1, tuple1[1]), q, s)
                self.check_insert((tuple1[0], tuple1[1]-1), q, s)
                self.check_insert((tuple1[0]+1, tuple1[1]-1), q, s)
            else:
                self.check_insert((tuple1[0]+1, tuple1[1]), q, s)
                self.check_insert((tuple1[0], tuple1[1]+1), q, s)
                self.check_insert((tuple1[0]+1, tuple1[1]+1), q, s)
                self.check_insert((tuple1[0], tuple1[1]-1), q, s)
                self.check_insert((tuple1[0]+1, tuple1[1]-1), q, s)
        elif tuple1[0] == 9:
            if tuple1[1] == 0:
                self.check_insert((tuple1[0]-1, tuple1[1]), q, s)
                self.check_insert((tuple1[0], tuple1[1]+1), q, s)
                self.check_insert((tuple1[0]-1, tuple1[1]+1), q, s)
            elif tuple1[1] == 9:
                self.check_insert((tuple1[0]-1, tuple1[1]), q, s)
                self.check_insert((tuple1[0], tuple1[1]-1), q, s)
                self.check_insert((tuple1[0]-1, tuple1[1]-1), q, s)
            else:
                self.check_insert((tuple1[0]-1, tuple1[1]), q, s)
                self.check_insert((tuple1[0], tuple1[1]+1), q, s)
                self.check_insert((tuple1[0]-1, tuple1[1]-1), q, s)
                self.check_insert((tuple1[0], tuple1[1]-1), q, s)
                self.check_insert((tuple1[0]-1, tuple1[1]+1), q, s)
        else:
            if tuple1[1] == 0:
                self.check_insert((tuple1[0]-1, tuple1[1]), q, s)
                self.check_insert((tuple1[0]+1, tuple1[1]), q, s)
                self.check_insert((tuple1[0]-1, tuple1[1]+1), q, s)
                self.check_insert((tuple1[0], tuple1[1]+1), q, s)
                self.check_insert((tuple1[0]+1, tuple1[1]+1), q, s)
            elif tuple1[1] == 9:
                self.check_insert((tuple1[0]-1, tuple1[1]), q, s)
                self.check_insert((tuple1[0]+1, tuple1[1]), q, s)
                self.check_insert((tuple1[0]-1, tuple1[1]-1), q, s)
                self.check_insert((tuple1[0], tuple1[1]-1), q, s)
                self.check_insert((tuple1[0]+1, tuple1[1]-1), q, s)
            else:
                self.check_insert((tuple1[0]-1, tuple1[1]-1), q, s)
                self.check_insert((tuple1[0]-1, tuple1[1]), q, s)
                self.check_insert((tuple1[0]-1, tuple1[1]+1), q, s)
                self.check_insert((tuple1[0], tuple1[1]-1), q, s)
                self.check_insert((tuple1[0], tuple1[1]+1), q, s)
                self.check_insert((tuple1[0]+1, tuple1[1]-1), q, s)
                self.check_insert((tuple1[0]+1, tuple1[1]), q, s)
                self.check_insert((tuple1[0]+1, tuple1[1]+1), q, s)

    def check_insert(self, tuple1, q, s):
        if tuple1 not in self.blocks_used:
            self.insert(tuple1, q, s)
            self.blocks_used.append(tuple1)

    def insert_block_points(self, s, tuple1, q):
        f = open("grid.grd", "r")

        f.seek(s.startPositions_dict[tuple1])

        for _ in range(s.numPoints_dict[tuple1]):
           line = f.readline()[:-1]
           tokens = line.split(" ")
           point = Point(float(tokens[1]), float(tokens[2]))
           self.insert(point, q, s)
        f.close()

    def fixUp(self, k):
        while k>1 and self.greater(k//2, k):
            self.swap(k, k//2)
            k = k//2

    def fixDown(self, k):
        while 2*k <= len(self.queue)-1:
            j = 2*k
            if j<len(self.queue)-1 and self.greater(j, j+1):
                j += 1
            if not self.greater(k, j):
                break
            self.swap(k, j)
            k = j

    def swap(self, x, y):
        temp = self.queue[x]
        self.queue[x] = self.queue[y]
        self.queue[y] = temp

    def greater(self, x, y):
        return self.queue[x] > self.queue[y]


class Structure:
   b_min = None
   b_max = None
   startPositions_dict = {}
   numPoints_dict = {}
   queue = PriorityQueue()

class Point:
   x = -1
   y = -1

   def __init__(self, x, y):
      self.x = x
      self.y = y 


def calc_eucl_dist(p1, p2):
    return pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2)

def calc_block_dist(tuple1, q, s):
    b_min, b_max = find_b_points(tuple1, s)

    flag1, flag2, flag3, flag4 = [ False for x in range(4) ]

    distance = 0

    if q.x > b_max.x:
        distance = pow(b_max.x - q.x, 2)
        flag1 = True
    elif q.x < b_min.x:
        distance = pow(b_min.x - q.x, 2)
        flag2 = True

    if q.y > b_max.y:
        distance = pow(b_max.y - q.y, 2)
        flag3 = True
    elif q.y < b_min.y:
        distance = pow(b_min.y - q.y, 2)
        flag4 = True

    if flag1 and flag4:
        distance = calc_eucl_dist(Point(b_max.x, b_min.y), q)
    elif flag2 and flag4:
        distance = calc_eucl_dist(Point(b_min.x, b_min.y), q)
    elif flag1 and flag3:
        distance = calc_eucl_dist(Point(b_max.x, b_max.y), q)
    elif flag2 and flag3:
        distance = calc_eucl_dist(Point(b_min.x, b_max.y), q)

    return distance

def find_b_points(tuple1, s):
    
    stepx = (s.b_max.x - s.b_min.x)/10
    stepy = (s.b_max.y - s.b_min.y)/10

    b_min = Point(s.b_min.x + tuple1[0]*stepx, s.b_min.y + tuple1[1]*stepy)
    b_max = Point(b_min.x + stepx, b_min.y + stepy)

    return b_min, b_max

def get_args(argv):
    if len(argv) != 4:
        print("Error: Wrong number of arguments!")
        print("Arguments: k q.x q.y")
        exit()

    q = Point(-1, -1)
    k = int(argv[1])
    q.x, q.y = [ float(x) for x in argv[2:]]

    return (k, q)

def read_grid_dir(s):
   f = open("grid.dir", "r")

   minx, maxx, miny, maxy = [ float(x) for x in f.readline().split(" ") ]
   s.b_min = Point(minx, miny)
   s.b_max = Point(maxx, maxy)

   for line in f:
      tokens = [ int(x) for x in line.split(" ") ]
      s.startPositions_dict[(tokens[0], tokens[1])] = tokens[2]
      s.numPoints_dict[(tokens[0],tokens[1])] = tokens[3]
   f.close() 

def init_queue(s, q):
    if q.x<s.b_max.x and q.x>s.b_min.x and q.y<s.b_max.y and q.y>s.b_min.y:
        q_blockID = find_q_block_inside(s, q)
    else:
        q_blockID = find_q_block_outside(s, q)

    s.queue.blocks_used.append(q_blockID)
    s.queue.insert(q_blockID, q, s)

def find_q_block_inside(s, q):

    stepx = (s.b_max.x - s.b_min.x)/10
    stepy = (s.b_max.y - s.b_min.y)/10

    place = Point(s.b_min.x, s.b_min.y)
    blockID = [-1, -1]
    for i in range(1,11):
        place.x += stepx
        if place.x > q.x:
            blockID[0] = i-1
            break

    for i in range(1,11):
        place.y += stepy
        if place.y > q.y:
            blockID[1] = i-1
            break
    return tuple(blockID)

def find_q_block_outside(s, q):

    min_dist = 1000000
    blockID = (-1, -1)

    for i in range(10):
        dist = calc_block_dist((i, 0), q, s)
        if min_dist > dist:
            min_dist = dist
            blockID = (i, 0)

    for i in range(10):
        dist = calc_block_dist((i, 9), q, s)
        if min_dist > dist:
            min_dist = dist
            blockID = (i, 9)

    for i in range(1, 9):
        dist = calc_block_dist((0, i), q, s)
        if min_dist > dist:
            min_dist = dist
            blockID = (0, i)

    for i in range(1, 9):
        dist = calc_block_dist((9, i), q, s)
        if min_dist > dist:
            min_dist = dist
            blockID = (0, i)
    return blockID

def find_nearest_k(s, q, k):
    results = []
    while k:
        results.append(next(find_nearest(s, q)))
        k -= 1
    return results

def find_nearest(s, q):

    while True:
        result = s.queue.popMin(q, s)
        if result:
            yield(result)

def save_results(results):
    f = open("results3", "w")

    for elem in results:
        f.write(str(elem.x) + " " + str(elem.y) + "\n")
    f.close()


def main(argv):

    k, q = get_args(argv)
    s = Structure() 
    read_grid_dir(s)
    init_queue(s, q)
    results = find_nearest_k(s, q, k)
    save_results(results)
    print(s.queue.blocks_used)

main(argv)
