import math

MaxValue = 220
startingRange = 31
highLowRange = 3
levels = 18
maxRange = int(MaxValue) - int(startingRange) - int(highLowRange)
interval = maxRange / (int(levels) - 1);
for i in range(levels):
    lowerlimit = int(startingRange + (interval * i))
    upperLimit = int(startingRange + highLowRange + (interval * i))
    print("low:" + str(lowerlimit) + " high:" + str(upperLimit))
