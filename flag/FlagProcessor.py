"""
@overview        {FlagProcessor}

@version         2.0

@author          Dyson Arley Parra Tilano <dysontilano@gmail.com>

@copyright       Dyson Parra
@see             github.com/DysonParra

History
@version 1.0     Implementation done.
@version 2.0     Documentation added.
"""
from flag.Flag import Flag


def print_flags_array(flags, printNone: bool):
	"""
	Muestra en consola el array indicado por {@code flags}

	@param flags     array de {@code Flag} que se va a imprimir en la consola.
	@param printNull indica si se van a imprimir las flags con valor de {@code null}
	"""
	print("\nFlags START")
	if flags is not None:
		for flag in flags:
			if printNone or flag != None:
				print(flag)
	print("Flags END\n")


def print_flags_matrix(flags, message):
	"""
	Muestra en consola la matriz indicada por {@code flags}

	@param flags   array de {@code String} que se va a imprimir en la consola.
	@param message mensaje que se mostrará antes de imprimir las flags.
	"""
	print(message)
	line = ""
	for flag in flags:
		line = flag[0]
		for i in range(1, len(flag)):
			line += " or " + flag[i]
		print(line)

	if (len(flags) == 0):
		print("Not specified.")
	print("")


def compare_required_and_optional_flags(requiredFlags: list, optionalFlags: list):
	"""
	Compara si hay {@code String} que están tanto en la matriz {@code requiredFlags} como en la
	matriz {@code optionalFlags}.

	@param requiredFlags una matriz con las flags requeridas; en cada fila se indican las flags y
	                     en cada columna indica cuales flags son excluyentes (si se incluye la
	                     flag de una columna no se pueden incluir las flags en las otras columnas
	                     de esa fila) al ser requeridas se debe incluir una y solo una flag de
	                     cada fila.
	@param optionalFlags una matriz con las flags opcionales; en cada fila se indican las flags y
	                     en cada columna indica cuales flags son excluyentes (si se incluye la
	                     flag de una columna no se pueden incluir las flags en las otras columnas
	                     de esa fila) al ser opcionales se pueden o no incluir una y solo una
	                     flag de cada fila.
	@return {@code null} si no hay flags repetidas, caso contrario {@code String} con un mensaje
	        que dice cuales flags se repiten.
	"""
	for reqValuesOr in requiredFlags:
		for reqFlag in reqValuesOr:
			for optValuesOr in optionalFlags:
				for optFlag in optValuesOr:
					if reqFlag== optFlag:
						return "Error: flag " + "'" + optFlag + "'" + " is defined as required flag and as optional flag."
	return None


def convert_args_to_flags_array(args: list, inputFlags: list):
	"""
	Analiza si el array {@code args} representa una secuencia válida de flags y en caso
	afirmativo almacena en {@code inputFlags} el equivalente en {@code Flag} del array.

	@param args       un array de {@code String} que se va a procesar para verificar si es una
	                  secuencia de flags válida.
	@param inputFlags el array de {@code Flag} donde se va a almacenar el equivalente en
	                  {@code Flag} del array {@code args}; se da por hecho que el array no es
	                  {@code null} ya que si lo es se generará un {@code NullPointerException}
	@return {@code null} si {@code inputFlags} representa una secuencia de flags válida, caso
	        contrario {@code String} con un mensaje que indica porque no es una secuencia válida
	        de flags.
	"""
	msg_Invalid_Flag = "Error: invalid flag "
	msg_Expect_Value_1 = "Error: expected a value for the flag "
	msg_Expect_Value_2 = " but found the flag "
	msg_Expect_Flag_1 = "Error: expected a flag or a flag withouth value after the value "
	msg_Expect_Flag_2 = " but found the value "
	msg_First_Arg_Not_Flag = "Error: expected a flag or a flag withouth value as first parameter but found the value "
	msg_Value_For_Flag_No_Value_1 = "Error: The flags started in '--' no need value, but found the value "
	msg_Value_For_Flag_No_Value_2 = " for the flag "
	msg_Last_Arg_Flag = "Error: Not found a value for the flag "

	flagNumber = 0
	flag = ""
	value = ""
	oldState = ""
	state = "value"
	for i in range(0, len(args)):
		oldState = state
		arg = args[i]
		if arg[0] == '-' and ((arg[1] == 0 or (arg[1] == '-' and (arg[2] == 0 or arg[2] == '-')))):
			return msg_Invalid_Flag + "'" + arg + "'"
		elif arg[0] == '-' and arg[1] == '-':
			state = "flagNoValue"
		elif arg[0] == '-':
			state = "flag"
		else:
			state = "value"

		if state == "flag":
				if oldState == "flag":
					return msg_Expect_Value_1 + "'" + args[i - 1] + "'" + msg_Expect_Value_2 + "'" + arg + "'"
				elif oldState == "value" or oldState == "flagNoValue":
					flag = arg

		elif state == "value":
				if oldState == "flag":
					value = arg
					inputFlags[flagNumber] = Flag(flag, value, False)
					flagNumber+=1
				elif oldState == "value":
					if i != 0:
						return msg_Expect_Flag_1 + "'" + args[i - 1] + "'" + msg_Expect_Flag_2 + "'" + arg + "'"
					else:
						return msg_First_Arg_Not_Flag + "'" + arg + "'"
				elif oldState == "flagNoValue":
					return msg_Value_For_Flag_No_Value_1 + "'" + arg + "'" + msg_Value_For_Flag_No_Value_2 + "'" + args[i - 1] + "'"

		elif state == "flagNoValue":
				if oldState == "flag":
					return msg_Expect_Value_1 + "'" + args[i - 1] + "'" + msg_Expect_Value_2 + "'" + arg + "'"
				elif oldState == "value" or oldState == "flagNoValue":
					flag = arg
					inputFlags[flagNumber] = Flag(flag, None, False)
					flagNumber+=1

	if state == "flag":
		return msg_Last_Arg_Flag + "'" + flag + "'"
	return None


def compare_input_flags(inputFlags: list, outputFlags: list, acceptedFlags: list, required: bool):
	"""
	Verifica si el array {@code inputFlags} contiene las flags indicadas por
	{@code acceptedFlags} de tal modo que si {@code required} es {@code true} significa que las
	flags son requeridas entonces {@code args} deben incluir todas las flags indicadas por
	{@code acceptedFlags}, caso contrario si {@code required} es {@code false} {@code args} puede
	incluir cero o más flags indicadas por {@code acceptedFlags}.

	@param inputFlags    es el array de {@code Flag} que se va a procesar.
	@param outputFlags   es un array donde se almacenarán las flags indicada por
	                     {@code acceptedFlags} que estén en {@code inputFlags}
	@param acceptedFlags son las flags que se revisará que estén o no en {@code inputFlags}
	@param required      indica si las flags indicadas por {@code acceptedFlags} son requeridas u
	                     opcionales.
	@return {@code null} si no ocurre ningún inconveniente al procesar {@code inputFlags}, caso
	        contrario {@code String} con un mensaje que indica porque no es posible procesar
	        {@code inputFlags}
	"""
	found: bool
	flagNumber = 0
	for flag in outputFlags:
		if flag == None:
			break
		else:
			flagNumber+=1

	errorMessage: str
	for reqValuesOr in acceptedFlags:
		found = False
		for reqFlag in reqValuesOr:
			#print(reqFlag)
			for i in range (0, len(inputFlags)):
				if inputFlags[i] != None:
					#print(" -> " + inputFlags[i].name)
					if reqFlag == inputFlags[i].name:
						if not found:
							#print("\nAdded " + inputFlags[i].name + " in " + flagNumber)
							outputFlags[flagNumber] = inputFlags[i]
							if required:
								inputFlags[i].required = True
							flagNumber+=1
							inputFlags[i] = None
							found = True
							#print("\n")
							#print("Again?")
							for j in range (0, len(inputFlags)):
								if inputFlags[j] != None:
									#print(" -> " + inputFlags[j].name)
									if reqFlag == inputFlags[j].name:
										#println("\nFound again!")
										errorMessage = "found the flag '" + reqFlag + "' more that one times"
										return errorMessage
							break
						else:
							#println("\nFound invalid combination")
							errorMessage = "Error: specified more that one of the flags"
							for aux in reqValuesOr:
								errorMessage += " " + aux
							return errorMessage
			#println("")
		if not found:
			#println("Not found")
			if required:
				errorMessage = "Not found required flag "
				errorMessage += reqValuesOr[0]
				for i in range (1, len(reqValuesOr)):
					errorMessage += " or " + reqValuesOr[i]
				#println(errorMessage)
				return errorMessage
		#println("")
	return None


def validate_specifed_flags(inputFlags: list , outputFlags: list, requiredFlags: list, optionalFlags: list, allowUnknownFlags: bool):
	"""
	Verifica el array {@code inputFlags} cuales de las flags indicadas por {@code requiredFlags}
	y por {@code optionalFlags} contiene y si {@code allowUnknownFlags} es {@code true} acepta
	que hayan flags que no estén ni en {@code requiredFlags} ni en {@code optionalFlags}.

	@param inputFlags        es el array de {@code Flag} que se va a procesar.
	@param outputFlags       es un array donde se almacenarán las flags indicada por
	                         {@code requiredFlags} y por {@code optionalFlags} que estén en
	                         {@code inputFlags}
	@param requiredFlags     una matriz con las flags requeridas; en cada fila se indican las
	                         flags y en cada columna indica cuales flags son excluyentes (si se
	                         incluye la flag de una columna no se pueden incluir las flags en las
	                         otras columnas de esa fila) al ser requeridas se debe incluir una y
	                         solo una flag de cada fila.
	@param optionalFlags     una matriz con las flags opcionales; en cada fila se indican las
	                         flags y en cada columna indica cuales flags son excluyentes (si se
	                         incluye la flag de una columna no se pueden incluir las flags en las
	                         otras columnas de esa fila) al ser opcionales se pueden o no incluir
	                         una y solo una flag de cada fila.
	@param allowUnknownFlags si {@code true} se aceptan flags que no estén en el array
	                         {@code requiredFlags} ni en el array {@code optionalFlags}, caso
	                         contrario si se encuentra una flag que no esté en los arrays
	                         devuelve {@code String} con mensaje de error.
	@return {@code null} si no ocurre ningún inconveniente al procesar {@code inputFlags}, caso
	        contrario {@code String} con un mensaje que indica porque no es posible procesar
	        {@code inputFlags}
	"""
	result = None
	result = compare_input_flags(inputFlags, outputFlags, requiredFlags, True)
	if result == None:
		result = compare_input_flags(inputFlags, outputFlags, optionalFlags, False)
		if result == None:
			flagQuantity = 0
			for outputFlag in outputFlags:
				if outputFlag != None:
					flagQuantity+=1
				else:
					break

			for inputFlag in inputFlags:
				if inputFlag != None:
					if not allowUnknownFlags:
						if result == None:
							result = "Error: unknown flags found"
						result += "  " + inputFlag.name
						#println(result)
					else:
						outputFlags[flagQuantity] = inputFlag
						flagQuantity+=1
	return result


def validate_flags(args: list, requiredFlags: list, optionalFlags: list, allowUnknownFlags: bool):
	"""
	Analiza si el array {@code args} representa una secuencia válida de flags, verifica que las
	flags requeridas {@code requiredFlags} estén todas especificadas allí, revisa que se incluyan
	cero o más flags opcionales {@code optionalFlags} y si {@code allowUnknownFlags} es
	{@code true} se aceptan flags que no sean opcionales ni requeridas caso afirmativo.

	@param args              un array de {@code String} que se va a procesar para verificar si es
	                         una secuencia de flags válida.
	@param requiredFlags     una matriz con las flags requeridas; en cada fila se indican las
	                         flags y en cada columna indica cuales flags son excluyentes (si se
	                         incluye la flag de una columna no se pueden incluir las flags en las
	                         otras columnas de esa fila) al ser requeridas se debe incluir una y
	                         solo una flag de cada fila.
	@param optionalFlags     una matriz con las flags opcionales; en cada fila se indican las
	                         flags y en cada columna indica cuales flags son excluyentes (si se
	                         incluye la flag de una columna no se pueden incluir las flags en las
	                         otras columnas de esa fila) al ser opcionales se pueden o no incluir
	                         una y solo una flag de cada fila.
	@param allowUnknownFlags si {@code true} se aceptan flags que no estén en el array
	                         {@code requiredFlags} ni en el array {@code optionalFlags}, caso
	                         contrario si se encuentra una flag que no esté en los arrays se
	                         devuelve {@code null} y se mostrará mensaje de error.
	@return array de {@code Flag} si se puede procesar {@code args} utilizando
	        {@code requiredFlags} y {@code optionalFlags} sin ningún inconveniente, caso
	        contrario {@code null} y se mostrará en consola porqué no fue posible procesar
	        {@code args}.
	"""
	result: str
	argsQuantity = len(args)
	inputFlags = []
	outputFlags = []

	result = compare_required_and_optional_flags(requiredFlags, optionalFlags)
	if result != None:
		print(result)
		return None

	inputFlags = [None]*argsQuantity
	result = convert_args_to_flags_array(args, inputFlags)
	if result != None:
		print(result)
		return None

	flagQuantity = 0
	for flag in inputFlags:
		if flag != None:
			flagQuantity+=1
	outputFlags = [None]*flagQuantity

	result = validate_specifed_flags(inputFlags, outputFlags, requiredFlags, optionalFlags, allowUnknownFlags)
	if (result != None):
		print(result)
		return None
	return outputFlags


def convert_args_to_flags(args: list, defaultArgs: list, requiredFlags: list, optionalFlags: list, allowUnknownFlags: bool):
	"""
	Analiza si el array {@code args} representa una secuencia válida de flags, verifica que las
	flags requeridas {@code requiredFlags} estén todas especificadas allí, revisa que se incluyan
	cero o más flags opcionales {@code optionalFlags} y si {@code allowUnknownFlags} es
	{@code true} se aceptan flags que no sean opcionales ni requeridas caso afirmativo.

	@param args              un array de {@code String} que se va a procesar para verificar si es
	                         una secuencia de flags válida.
	@param defaultArgs       un array de {@code String} que se va a procesar para verificar si es
	                         una secuencia de flags válida en caso de {@code  args} se encuentre
	                         vacío.
	@param requiredFlags     una matriz con las flags requeridas; en cada fila se indican las
	                         flags y en cada columna indica cuales flags son excluyentes (si se
	                         incluye la flag de una columna no se pueden incluir las flags en las
	                         otras columnas de esa fila) al ser requeridas se debe incluir una y
	                         solo una flag de cada fila.
	@param optionalFlags     una matriz con las flags opcionales; en cada fila se indican las
	                         flags y en cada columna indica cuales flags son excluyentes (si se
	                         incluye la flag de una columna no se pueden incluir las flags en las
	                         otras columnas de esa fila) al ser opcionales se pueden o no incluir
	                         una y solo una flag de cada fila.
	@param allowUnknownFlags si {@code true} se aceptan flags que no estén en el array
	                         {@code requiredFlags} ni en el array {@code optionalFlags}, caso
	                         contrario si se encuentra una flag que no esté en los arrays se
	                         devuelve {@code null} y se mostrará mensaje de error.
	@return array de {@code Flag} si se puede procesar {@code args} utilizando
	        {@code requiredFlags} y {@code optionalFlags} sin ningún inconveniente, caso
	        contrario {@code null} y se mostrará en consola porqué no fue posible procesar
	        {@code args}.
	"""
	flags: list
	requiredFlags = requiredFlags if not requiredFlags == None else {}
	optionalFlags = optionalFlags if not optionalFlags == None else {}
	if ((defaultArgs == None or len(defaultArgs) == 0)
			and (args == None or len(args) == 0)):
		print("Flags and default flags not specified...")
		flags = None
	elif (args != None and len(args) != 0):
		print("Validating specified flags...")
		flags = validate_flags(args, requiredFlags, optionalFlags, allowUnknownFlags)
	else:
		print("No flags specified, validating default flags...")
		flags = validate_flags(defaultArgs, requiredFlags, optionalFlags, allowUnknownFlags)

	if (flags == None):
		print("")
		print_flags_matrix(requiredFlags, "Required flags:")
		print_flags_matrix(optionalFlags, "Optional flags:")
		System.out.println("Error in flags")
	else:
		print_flags_array(flags, True)
	return flags
