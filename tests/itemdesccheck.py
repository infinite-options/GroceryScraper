stringName = "vines on the tomato"
checkString = "tomato vines"

a1 = stringName.lower().split()
a2 = checkString.lower().split()
a1.sort()
a2.sort()
print(a1)
print(a2)
print(len(a1))
if all(item in a1 for item in a2):
    print("iden")
