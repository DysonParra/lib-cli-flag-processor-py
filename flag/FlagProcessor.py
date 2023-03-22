from flag.Flag import Flag

def print_flags_array(flags, printNone: bool):
	print("\nSTART Flags:")
	for flag in flags:
		if printNone or flag != None:
			print(flag)
	print("END Flags\n")

def printFlagsMatrix(flags, message):
	print(message)
	line = ""
	for valueOr in flags:
		line = valueOr[0]
		for i in range(1, len(valueOr)):
			line += " or " + valueOr[i]
		print(line)

	if (len(flags) == 0):
		print("Not specified.")
	print("")

def compare_required_and_optional_flags(requiredFlags: list, optionalFlags: list):
	for reqValuesOr in requiredFlags:
		for reqFlag in reqValuesOr:
			for optValuesOr in optionalFlags:
				for optFlag in optValuesOr:
					if reqFlag== optFlag:
						return "Error: flag " + "'" + optFlag + "'" + " is defined as required flag and as optional flag."
	return None

def convertArgsToFlagsArray(args: list, inputFlags: list):
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
	result: str
	argsQuantity = len(args)
	inputFlags = []
	outputFlags = []

	result = compare_required_and_optional_flags(requiredFlags, optionalFlags)
	if result != None:
		print(result)
		return None

	inputFlags = [None]*argsQuantity
	result = convertArgsToFlagsArray(args, inputFlags)
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
		printFlagsMatrix(requiredFlags, "Required flags:")
		printFlagsMatrix(optionalFlags, "Optional flags:")

	return flags
