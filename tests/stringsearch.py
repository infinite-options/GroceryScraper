string = "product - 3 each"
unit = "each"

def before(value, substr):
    words = value.lower().split()
    if substr in words[1:]:
        return words[words.index(substr)-1]

if unit in string:
    print(before(string, unit))
else:
    print("no")
