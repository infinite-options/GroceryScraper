#from flask import Flask

keyword = ['($','']
files = ['samplesafeway.txt','sampleraleys.txt']
#before and after line

with open(files[0], 'r') as f:
    line = f.readline()
    before = ''
    count = 1
    while line:
        # code
        if (line.find(keyword[0]) != -1):
            print(before)
            print(line)
        before = line
        line = f.readline()
        count += 1

#@app.route("/")
#def home():
#    return "<h1>page</h1>"
