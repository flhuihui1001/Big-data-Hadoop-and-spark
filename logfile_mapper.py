#!/usr/bin/env python
#
# This file has been provided as a starting point. You need to modify this file.
# Reads whole lines stdin; writes key/value pairs to stdout
# http://docs.aws.amazon.com/emr/latest/ReleaseGuide/UseCase_Streaming.html
# --- DO NOT MODIFY ANYTHING ABOVE THIS LINE ---

import sys
import re
import datetime
import calendar

def main(argv):
    abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
    for line in sys.stdin:
        line = re.split(r"\b:\b",line, 1)[0]
        line = line.split("[",1)[1]
        month = abbr_to_num[line[3:6]]
<<<<<<< HEAD
        print('Date:'+ line[7:] + "-" + '{:02}'.format(month) + "\t" + "1")
=======
        print('Date:'+'{:02}'.format(month) + "-" + line[7:]+ "\t" + "1")
>>>>>>> 00ced8fd42a3e2318e0d2d6de804889b3f33353e
        
if __name__ == "__main__":
    main(sys.argv)


<<<<<<< HEAD
=======

>>>>>>> 00ced8fd42a3e2318e0d2d6de804889b3f33353e
