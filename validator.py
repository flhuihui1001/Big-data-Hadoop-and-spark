#!/usr/bin/env python
#
# validate and build a student submission
# Must run in Python 3.4+ because Python 3 is the future. (Unicode, etc.)

import sys
if sys.version < "3.4":
    raise RuntimeError("validator requires Pyton 3.4 or above")

ASSIGNMENT="ASSIGNMENT"
REQUIRED_FILES="REQUIRED_FILES"
OPTIONAL_FILES="OPTIONAL_FILES"

import sys,zipfile,os,os.path,sys
import configparser
import py_compile
optional = []
from subprocess import Popen,PIPE,call

def validate_username(username):
    if username=="pat":
        print("You must change the default username in the user.cfg file")
        exit(1)
    if not username[0:1].isalpha():
        print("email address must begin with a letter")
        exit(1)
    if not username[-1].isdigit():
        print("email address must end with a number before the @ sign")
        exit(1)
    return True

def ignore_filename(fname):
    """Returns true if this filename should be ignored. Useful if students make their own ZIP file
    and it contains junk."""
    if len(fname)==0: return True
    if fname.endswith("/"): return True # ignore an empty directory
    if fname[0] in "._": return True
    if fname.endswith("~"): return True
    if fname.endswith(".bak"): return True
    base = os.path.basename(fname)
    if base[0] in "._": return True
    return False

def validate_txt(text):
    """Returns true if what can be read in text is valid"""
    if "\r" in text: raise RuntimeError("carriage return found in text file; Please use Unix-format line endings.")
    for line in text:
        if line.startswith("PK\003\004"): raise RuntimeError("ZIP file provided")
        if line.startswith("{\\rtf"):  raise RuntimeError("RTF file provided")
    if not text.endswith("\n"): raise RuntimeError("Text files must end with a newline")
    return True

def validate_txtfile(fname):
    """Make sure that this is a valid text file"""
    try:
        return validate_txt(open(fname,"r").read())
    except UnicodeDecodeError as e:
        print(str(e),file=sys.stderr)
        print("{}: not a text file".format(fname),file=sys.stderr)
        return False
    except RuntimeError as e:
        print(str(e),file=sys.stderr)
        print("{}: not a valid text file".format(fname),file=sys.stderr)
        return False
    assert(False)

def validate_pyfile(fname):
    """Make sure that this python file is valid"""
    if not os.path.exists(fname):
        print("{} does not exist".format(fname),file=sys.stderr)
        return False
    if not fname.endswith(".py"):
        print("{} does not end with a '.py'".format(fname),file=sys.stderr)
        return False
    try:
        a = py_compile.compile(fname,doraise=True)
    except py_compile.PyCompileError as e:
        print("Compile error: {}".format(str(e)),file=sys.stderr)
        return False
    return True

class Validator:
    """The Validator class understands the problem set package and can
    validate the files that make up the ZIP file.  They can be
    validated before or after being put into the ZIP file."""
    def __init__(self,user_fname=None):
        """When we initialize, read a configuration.
        self.name - the name of the assignment.
        self.required - a set of the required file names in the assignment.
        self.optional - a set of the optional file names in the assignment
        self.user - configparser for the problemset user configuration.
        """
        self.validate_pyfiles = True
        self.user = configparser.ConfigParser()
        if user_fname:
            self.user.read(user_fname)
        try:
            self.name = os.environ[ASSIGNMENT]
        except KeyError:
            print("ASSIGNMENT environment variable not set. Normally this is set in the Makefile")
            exit(1)
        self.unpackdir = "unpack" # where to unpack
        self.required = set(os.environ[REQUIRED_FILES].replace(","," ").split())
        try:
            self.optional = set(os.environ[OPTIONAL_FILES].replace(","," ").split())
        except ConfigParser.NoOptionError:
            self.optional = set()

        self.optional.add("Makefile") # add it


    def validate_file(self,fn):
        if os.path.exists(fn) and validate_txtfile(fn):
            if fn.endswith(".py")==False or self.validate_pyfiles==False:
                return True
            if validate_pyfile(fn)==True:
                return True
        return False

    def check_files(self):
        """Check to make sure that all files are present in the current directory and correct"""
        errors = 0
        required_missing = set()
        for fn in self.required:
            if os.path.exists(fn)==False:
                required_missing.add(fn)
            if not self.validate_file(fn):
                errors += 1
        for fn in self.optional:
            if os.path.exists(fn):
                if not self.validate_file(fn):
                    errors += 1
        if errors:
            print("ERRORS: {}".format(errors))
        if required_missing:
            print("REQUIRED FILES MISSING: {0}".format(len(required_missing)))
            for fname in required_missing:
                print("   {}".format(fname))
        return errors

    def validate_zipfile(self,z,fname,hook=None):
        errors = 0
        # Get the file contents
        contents = z.open(fname).read()
        tempname = None

        # Unpack if the file is a .py or .txt file, or if we have a hook, create a file with the contents
        if fname.endswith(".py") or fname.endswith(".txt") or hook:
            tempname = os.path.join(self.unpackdir,os.path.basename(fname))
            with open(tempname,"wb") as fb:
                fb.write(contents)
        
        if self.validate_file(tempname)==False:
            errors += 1

        if hook:
            hook(tempname,error_msg="")
        return errors

    def validate_zip(self,zfilename,hook=None):
        """Validate a zip file. Make sure that the requested files exist
        and that everything properly compiles. Returns number of errors found."""
        found_required = set()
        found_optional = set()
        found_unwanted = set()
        
        os.mkdir(self.unpackdir)
        files_to_validate = []
        errors = 0
        print("Validating {0} ...\n".format(zfilename))
        z = zipfile.ZipFile(zfilename)
        for f in z.filelist:
            fname = f.orig_filename                    # the full filename
            print("fname=",fname)
            if ignore_filename(fname): continue   
            fbase = os.path.basename(fname)            # name without the directory
            if fbase in self.required:
                found_required.add(fbase)
                files_to_validate.append(fname)
                continue
            if fbase in self.optional:
                found_optional.add(fbase)
                files_to_validate.append(fname)
                continue
            found_unwanted.add(fbase)

        def print_file_list(title,files):
            if files:
                print("")
                print(title)
                for word in files:
                    print("\t"+word)

        print("")
        print_file_list("Found required files:",found_required)
        print_file_list("Found optional files:",found_optional)

        print_file_list("MISSING REQUIRED FILES:",self.required.symmetric_difference(found_required)) 
        print_file_list("MISSING OPTIONAL FILES:",self.optional.symmetric_difference(found_optional)) 

        print("Validating files...")
        # First validate the python files, then the non-python files
        for fname in filter(lambda f:f.endswith(".py"),files_to_validate):
            errors += self.validate_zipfile(z,fname,hook)

        for fname in filter(lambda f:not f.endswith(".py"),files_to_validate):
            errors += self.validate_zipfile(z,fname,hook)

        if errors:
            print("TOTAL ERRORS: {0}".format(errors))

        return(errors)

    def dirname(self):
        """The name is EMAIL(part)-ASSIGNMENT/"""
        import re
        email = self.user.get("USER","email")
        try:
            username = re.match("([^@]*)@.*",email).group(1)
            validate_username(username)
        except AttributeError as e:
            print("'{}' in ../user.cfg is not a valid email address".format(email),file=sys.stderr)
            exit(1)
        return username+"-"+self.name

    def build_zip(self):
        dirname = self.dirname()
        zipname = dirname+".zip"
        print("Building {0}".format(zipname))
        z = zipfile.ZipFile(zipname,"w",zipfile.ZIP_DEFLATED)
        required_missing = []
        for fn in self.required.union(self.optional):
            if os.path.exists(fn):
                z.write(fn,arcname=dirname+"/"+fn,compress_type=zipfile.ZIP_DEFLATED)
                print("Added {0}...".format(fn))
            else:
                if fn in self.required:
                    msg = "REQUIRED FILE"
                    required_missing.append(fn)
                else:
                    msg = "Optional file"
                print("{0} {1} not found...".format(msg, fn))
        z.close()
        if required_missing:
            print("FILES MISSING: {}".format(len(required_missing)))
            for fn in required_missing:
                print("   {}".format(fn))
            print("\n")
        print("Done!\n\n")
        call(['ls','-l',zipname])
        print("\n")
        call(['unzip','-l',zipname])
        return zipname

if __name__=="__main__":
    # Read the config file
    try:
        print("ASSIGNMENT: ",os.getenv("ASSIGNMENT"))
    except KeyError:
        print("ASSIGNMENT environment variable must be set")
        exit(1)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug",action="store_true")
    parser.add_argument("--check",action="store_true",help="Check for files")
    parser.add_argument("--user",default="../user.cfg",help="user config information")
    parser.add_argument("--zip",action="store_true",help="Make the ZIP file and validate it")
    parser.add_argument("--validate",help="Validate a ZIP file")
    parser.add_argument("--verbose",action="store_true")

    args = parser.parse_args()

    if not os.path.exists(args.user):
        raise IOError("User configuration file '{}' does not exist".format(args.user))

    # zipfile name created will be USERNAME-ASSIGNMENT.ZIP
    # all files will be put in a subdirectory with that name.

    v = Validator(user_fname=args.user)

    if args.check:
        r = v.check_files()
        if r==0:
            print("Everything checks out okay.")

    if args.zip:      v.build_zip()
    if args.validate: v.valdiate_zip(args.validate) 
    exit(0)

