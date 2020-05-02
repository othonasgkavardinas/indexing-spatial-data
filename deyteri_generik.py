f = open("Beijing_restaurants.txt", "r")
f2 = open("test2", "w")

x_min = 39.7
x_max = 39.8
y_min = 116.4
y_max = 116.5

f.readline()
lineno = 1
for line in f:
    tokens = [ float(x) for x in line.split(" ") ]

    if tokens[0] >= x_min and tokens[0] <= x_max and tokens[1] >= y_min and tokens[1] <= y_max:
        f2.write(str(lineno) + " " +  str(tokens[0]) + " " + str(tokens[1]) + "\n")
    lineno += 1
f.close()
f2.close()


