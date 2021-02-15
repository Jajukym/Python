#!/usr/bin/env python3

#this is just some incline profile builders

# this defines the movement, each line is (seconds, position)
# seconds is the time since the start of the routine, position is olympus reckoning
#routine = ((0,0),
#           (3,1),
#           (6,2),
#           (9,3),
#           (12,4),
#           (15,5),
#           (18,6),
#           (21,7),
#           (24,7),
#           (27,7),
#           (30,7),
#           (31,7),
#           (31,7),
#           (41,7),
#           (41,7),
#           (41,7),
#           (51,7),
#           (51,7),
#           (51,7),
#           (61,7),
#           (61,7),
#           (61,7),
#           (71,7),
#           (71,7),
#           (71,7),
#           (81,7),
#           (81,7),
#           (81,7),
#           (91,7),
#           (91,7),
#           (91,7),
#           (21,7),
#           (21,7),
#          )
#build it with for loops!


# step by step every  10s between 1 and 36
routine = ((3,1),)
for i in range(2,37):
	routine += ((i*10,i),)
for i in range(36):
	routine += ((i*10+36*10,36-i),)


# up 2 down 1 etc between 1 and 36
routine = ((3,1),)
dt = 10
t = dt
for i in range(2,36):
    routine += ((t,i+1),)
    t += dt
    routine += ((t,i),)
    t += dt
routine += ((t,36),)
t += dt
for i in range(35):
    routine += ((t,36-i-1),)
    t += dt
    routine += ((t,36-i),)
    t += dt
routine = ((t,1),)

#jump by 3 step every  10s between 1 and 36
routine = ((3,1),)
for i in range(3,37,3):
	routine += ((i*10,i),)
for i in range(0,36,3):
	routine += ((i*10+36*10,36-i),)
routine = ((700,1),)

# up 2 down 1 etc between 1 and 36, only just arrives before down
routine = ((0,1),)
dt = 10
st = 10
t = dt
for i in range(2,36):
    routine += ((t,i+1),)
    t += dt
    routine += ((t,i),)
    t += st
routine += ((t,36),)
t += dt
for i in range(35):
    routine += ((t,36-i-1),)
    t += dt
    routine += ((t,36-i),)
    t += st
