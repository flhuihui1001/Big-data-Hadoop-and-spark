#!/usr/bin/env python
#
# This file has been provided as a starting point. You need to modify this file.
# Reads key/value pairs from stdin, writes key/value pairs to stdout
# --- DO NOT MODIFY ANYTHING ABOVE THIS LINE ---

import sys

def main(argv):
    try:
         olddate = None
         oldsum = 0
         for line in sys.stdin:
              (key,value) = line.rstrip().split('\t')
              if key.startswith('Date:'):
                  date = key [5:]
                  if date != olddate:
                       if olddate:
                           print("{} {}".format(olddate,oldsum))
                       olddate = date
                       oldsum = 0
                  oldsum += int(value)
    except EOFError:
        pass
    if olddate:
        print("{} {}".format(olddate,oldsum))
    return None

if __name__ == "__main__":
    main(sys.argv)




