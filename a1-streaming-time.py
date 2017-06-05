#!/usr/bin/python3.5
#
# generate the streaming time report


if __name__=="__main__":
    import argparse,os

    parser = argparse.ArgumentParser()
    parser.add_argument("s3",help="S3 URL")
    parser.add_argument("output",help="Output filename")
    
    args = parser.parse_args()

    instance_type="HOW DO WE GET THE INSTANCE TYPE???"

    if os.path.exists(args.output):
        raise RuntimeError("{} exists".format(args.output))
    
    # Create the output file
    with open(args.output,"w") as f:
        f.write("# streaming to a {}\n".format(instance_type))

    
