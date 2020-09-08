#right shifting counting byte
print ("shifting bits right")
x = 128.0
for i in range (18):
   print (int(x))
   if x == 1:
       x = 129
       print (int(x))
       x = 128
       print (int(x))
   x = (x + x - (x/2))
   print (int(x))
   x = (x /3)
   
#left shifting counting byte
print ("Shifting bits left")
y = 1.0
for i in range(18):
   print (int(y))
   y = y * 3
   print (int(y))
   y = (y / 3 * 2)
   if y == 384:
       y = 129.0
       print (int(y))
       y = 1.0
