import sys

print 'default_type text/css;'
sys.stdout.write("return 200 '")
for line in sys.stdin:
    sys.stdout.write(line)
print("';")
