"""
@fileoverview    {AppTester}

@version         2.0

@author          Dyson Arley Parra Tilano <dysontilano@gmail.com>

@copyright       Dyson Parra
@see             github.com/DysonParra

History
@version 1.0     Implementation done.
@version 2.0     Documentation added.
"""
from flag.Flag import Flag
from flag.FlagProcessor import *

class AppTester:
	"""
	TODO: Description of {@code AppTester}.
	
	@author Dyson Parra
	@since 3.11
	"""


	def start_testing(args: list):
	    """
	    Ejecuta las pruebas de la aplicación.
	    
	    @param args argumentos de la linea de comandos.
	    @return {@code true} si se ejecutan las pruebas correctamente, {@code false} caso contrario.
	    """
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
