
x = 0
y = 0
z = ""

x = int(input("enter number: \n"))

while y < x:
        print(y + 1)
        print("yo!")
        y += 1
        z = input("Enter To Continue or 'n' to end?: \n")
        if z == "n":
                print("Bye-Bye!")
                break
print("Test Done")
print((y), "Samples Completed")
