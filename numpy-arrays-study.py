import numpy

myfile = 'ML\\test1.csv'
dataset = numpy.genfromtxt(myfile, delimiter=',', usecols=(0,1), dtype=str, comments=None, encoding='utf-8')
data, labels = dataset[:, 0], dataset[:, 1]

lines = len(data)
cols = len(max(data, key=len))

print (lines)
print (cols)

data = numpy.array(data) # Or: data1 = data.copy()
data = data.view(numpy.uint32)
data = data.reshape(lines,cols)

print (data)
