f1 = open("test1", "r")
f2 = open("test2", "r")

for line in f2:
    if line != f1.readline():
        print("FAILURE")
        exit()

print("SUCCESS")

f1.close()
f2.close()