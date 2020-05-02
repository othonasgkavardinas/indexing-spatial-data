#import natsort
from sys import argv
from time import time

class Structure:
   b_min = None
   b_max = None
   startPositions_dict = {}
   numPoints_dict = {}

class Point:
   x = -1
   y = -1

   def __init__(self, x, y):
      self.x = x
      self.y = y 

def get_user_window(argv):
   if len(argv) != 5:
      print("Error: Wrong number of arguments!")
      print("Arguments: xlow, xhigh, ylow, yhigh")
      exit()

   minx, maxx, miny, maxy = [ float(x) for x in argv[1:] ]
   return (Point(minx, miny), Point(maxx, maxy))

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

def collect_points(s, w_min, w_max):
   blocks = []

   f = open("grid.grd", "r")

   stepx = (s.b_max.x - s.b_min.x)/10
   stepy = (s.b_max.y - s.b_min.y)/10

   prevPlace = Point(s.b_min.x, s.b_min.y)
   place = Point(s.b_min.x + stepx, s.b_min.y + stepy)

   for i in range(10):
      prevPlace.y = s.b_min.y
      place.y = s.b_min.y + stepy
      for j in range(10):
         if check_overlap(prevPlace, place, w_min, w_max):
            if check_inside(prevPlace, place, w_min, w_max):
               put_block_points(blocks, (i, j), s, w_min, w_max, f, True)
            else:
               put_block_points(blocks, (i, j), s, w_min, w_max, f, False)
         prevPlace.y = place.y
         place.y += stepy
      prevPlace.x = place.x
      place.x += stepx

   f.close()
   return blocks

def check_overlap(bm, bM, wm, wM):
   if bm.x > wM.x or wm.x > bM.x:
      return False
   if bm.y > wM.y or wm.y > bM.y:
      return False
   return True

def check_inside(bm, bM, wm, wM):

   if wM.y>=bM.y and wm.y<=bm.y and wM.x>=bM.x and wm.x<=bm.x:
      return True
   return False

def put_block_points(list, tuple1, s, wm, wM, f, isWholeBlock):

   f.seek(s.startPositions_dict[tuple1])


   for _ in range(s.numPoints_dict[tuple1]):
      line = f.readline()[:-1]
      tokens = line.split(" ")

      point = Point(float(tokens[1]), float(tokens[2]))

      if not isWholeBlock:
         if not (point.x >= wm.x and point.x <= wM.x and point.y >= wm.y and point.y <= wM.y):
            continue
      list.append(line)

def write_results(l):
   f = open("results", "w")
   for line in l:
      f.write(line + "\n")
   f.close()


def main(argv):

   w_min, w_max = get_user_window(argv)
   s = Structure() 
   read_grid_dir(s)
   l = collect_points(s, w_min, w_max)
   write_results(l)
   
   
   '''
   f1 = open("test1", "w")
   for line in natsort.natsorted(l):
      f1.write(line + "\n")
   f1.close()
   '''  

t = time()
main(argv)
print("Total time: ", (time() - t))