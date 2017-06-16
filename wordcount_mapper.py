#!/usr/bin/env python
#
# q2_mapper.py:
# Reads whole lines stdin; writes key/value pairs to stdout
# http://docs.aws.amazon.com/emr/latest/ReleaseGuide/UseCase_Streaming.html

import sys

def main(argv):
    try:
        for line in sys.stdin:
            line = line.rstrip()
            words = line.split()
            for word in words:
                print("LongValueSum:" + word + "\t" + "1")
    except EOFError:
        return None


if __name__ == "__main__":
    main(sys.argv)

