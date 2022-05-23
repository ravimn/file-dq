import os
import glob
check = lambda x,y: type(x) == y
print( 'check returns ',check(2,int))

a = '1.2'
try:
    int(a)
except ValueError:
    print('Not an integer')

try:
    float(a)
except ValueError:
    print('Not an integer')

print('End of test')

files = glob.glob('test*')

print(files) 
