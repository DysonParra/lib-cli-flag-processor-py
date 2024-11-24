from flag.Flag import Flag
from flag.FlagProcessor import *

def startTesting(args):
    requiredFlags = [
        ["-use", "--notUse", "--find"],
        ["-name", "--noName"],
        ["-encoder", "--noEncoder"]]

    optionalFlags = [
        ["-flag", "--noFlag"],
        ["-test", "--noTest"]]

    defaultArgs = [
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

    flags = convert_args_to_flags(args, defaultArgs, requiredFlags, optionalFlags, True)
    if (flags != None):
        print("Flags success processed")
    
    return flags != None

