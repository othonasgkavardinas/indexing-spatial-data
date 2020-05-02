from sys import maxsize
from time import time

class Structure:
    minPoint = (0.0, 0.0)
    maxPoint = (0.0, 0.0)
    x_block_boarder = 0.0
    y_block_boarder = 0.0
    list_x = []
    list_y = []


def find_grid_borders():
    f = open("Beijing_restaurants.txt", "r")

    maxX = maxY = 0
    minX = minY = maxsize

    f.readline()

    for line in f:
        coordinate = line.split(" ")

        if maxX < float(coordinate[0]):
            maxX = float(coordinate[0])

        if maxY < float(coordinate[1]):
            maxY = float(coordinate[1])

        if minX > float(coordinate[0]):
            minX = float(coordinate[0])

        if minY > float(coordinate[1]):
            minY = float(coordinate[1])
    f.close()

    return (minX, minY), (maxX, maxY)

def find_block_difference(s):
    x_border = s.maxPoint[0] - s.minPoint[0]
    y_border = s.maxPoint[1] - s.minPoint[1]

    x_block_border = x_border / 10
    y_block_border = y_border / 10

    return x_block_border, y_block_border

def init_dict(s):
    block_dict = {}
    for i in range(10):
        for j in range(10):
            block_dict[(s.minPoint[0] + (i+1)*s.x_block_border, s.minPoint[1] + (j+1)*s.y_block_border)] = []
    return block_dict

def make_lists(s):
    list_x = []
    list_y = []

    for i in range(10):
        list_x.append(s.minPoint[0] + (i+1)*s.x_block_border)
        list_y.append(s.minPoint[1] + (i+1)*s.y_block_border)

    return list_x, list_y

def fill_dict(s, block_dict):
    f = open("Beijing_restaurants.txt", "r")

    idNo = 1

    f.readline()
    for line in f:
        tokens = line.split(" ")
        a = binary_search(s.list_x, 0, len(s.list_x)-1, float(tokens[0]))
        b = binary_search(s.list_y, 0, len(s.list_y)-1, float(tokens[1])) 
        block_dict[(a,b)].append((float(tokens[0]), float(tokens[1]), idNo))
        idNo += 1

    f.close()


def binary_search(list1, left, right, x):
    if left <= right:
        mid = round(left + ((right - left)/2))
        if list1[mid] > x:
            return binary_search(list1, left, mid-1, x)
        elif list1[mid] < x:
            return binary_search(list1, mid+1,right, x) 
        else:
            return list1[right]
    else:
        return list1[right + 1]

def create_files(s, block_dict):
    f_grd = open("grid.grd", "w")
    f_dir = open("grid.dir", "w")

    f_dir.write(str(s.minPoint[0]) + " " + str(s.maxPoint[0]) + " " + str(s.minPoint[1]) + " " + str(s.maxPoint[1]) + "\n")

    placement = 0

    for i in range(len(s.list_x)):
        for j in range(len(s.list_y)):
            f_dir.write(str(i) + " " + str(j) + " " + str(placement) + " " + str(len(block_dict[(s.list_x[i],s.list_y[j])])) + "\n")
            for value in block_dict[(s.list_x[i],s.list_y[j])]:
                f_grd.write(str(value[2]) + " " + str(value[0]) + " " + str(value[1]) + "\n")
            placement = f_grd.tell()
    f_grd.close()
    f_dir.close()

def main():
    s = Structure()

    s.minPoint, s.maxPoint = find_grid_borders()
    s.x_block_border, s.y_block_border = find_block_difference(s)

    block_dict = init_dict(s)
    s.list_x, s.list_y = make_lists(s)
    fill_dict(s, block_dict)
    create_files(s, block_dict)

def test():
    #test1: check grid.grd lines
    f1 = open("grid.grd", "r")
    f2 = open("Beijing_restaurants.txt", "r")
    f3 = open("grid.dir", "r")

    lines = 0
    for line in f1:
        lines += 1
    if lines == 51970:
        print("SUCCESS 1")
    else:
         print("FAILURE 1")

    #test2: check if grid.grd contains the same points as Beijing file
    f1.seek(0, 0)
    li = []

    for line in f1:
        tokens = line.split(" ")
        li.append((float(tokens[1]), float(tokens[2])))

    f2.readline()
    for line in f2:
        tokens = line.split(" ")
        if (float(tokens[0]), float(tokens[1])) in li:
            li.remove((float(tokens[0]), float(tokens[1])))

    if not li:
        print("SUCCESS 2")
    else:
        print("FAILURE 2")

    #test3: check sum of points in grid.dir
    f3.readline()

    sum1 = 0
    for line in f3:
       sum1 += float(line.split(" ")[3])
    if sum1 == 51970:
        print("SUCCESS 3")
    else:
        print("FAILURE 3")

    f1.close()
    f2.close()
    f3.close()


start_time = time()
main()
#test()
print("Total time: %s" %(time() - start_time))
