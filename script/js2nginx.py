import sys

# geo $dollar {
#   default "$";
# }

print 'default_type application/javascript;'
sys.stdout.write('return 200 "')
for line in sys.stdin:
    line = line.replace('$', '$dollar')
    sys.stdout.write(line)
print('";')
