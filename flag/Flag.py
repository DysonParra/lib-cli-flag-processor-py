"""
@fileoverview    {Flag}

@version         2.0

@author          Dyson Arley Parra Tilano <dysontilano@gmail.com>

@copyright       Dyson Parra
@see             github.com/DysonParra

History
@version 1.0     Implementation done.
@version 2.0     Documentation added.
"""
class Flag:
	"""
	TODO: Description of {@code Flag}.

	@author Dyson Parra
	@since Python 3.11
	"""


	def __init__(self, name, value, required):
		"""
		Constructor.
		"""
		if not isinstance(name, str):
			raise Exception('name must be string')
		elif not isinstance(value, str) and value != None:
			raise Exception('value must be string')
		elif not isinstance(required, bool):
			raise Exception('required must be bool')
		self.name = name
		self.value = value
		self.required = required


	def __str__(self):
		"""
		Obtiene el valor en {String} del objeto actual.

		Return:
		- {String} con la representación del objeto.
		"""
		result = ""
		if self.required:
			result += "*"
		else:
			result += " "
		if self.value == None:
			result += self.name
		else:
			result += self.name + " = " + self.value
		return result
