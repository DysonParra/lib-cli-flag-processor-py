import sys
from flag.Flag import Flag
from flag.FlagProcessor import *

print("\n...START...")

requiredFlags = [
    ["-use", "--notUse", "--find"],
    ["-name", "--noName"],
    ["-encoder", "--noEncoder"]]

optionalFlags = [
    ["-flag", "--noFlag"],
    ["-test", "--noTest"]]

argsAux = [
    "--useDefault",
    "-uses",
    "MKV",
    "-noTest",
    "aac",
    "-use",
    "ffmpeg",
    "-name",
    "chromedriver.exe",
    "-test",
    "_urls.xml",
    "--aac",
    "--noEncoder"]

#for i in range(1, len(sys.argv)):
#    print (sys.argv[i])

#flags = validate_flags(argsAux, requiredFlags, optionalFlags, True)
flags = validate_flags(sys.argv[1:], requiredFlags, optionalFlags, True)
if (flags == None):
    print("...ERROR IN FLAGS...")
    sys.exit(0)

print_flags_array(flags, True)
print("...END...")
