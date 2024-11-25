"""
@fileoverview    {Application}

@version         2.0

@author          Dyson Arley Parra Tilano <dysontilano@gmail.com>

@copyright       Dyson Parra
@see             github.com/DysonParra

History
@version 1.0     Implementation done.
@version 2.0     Documentation added.
"""
import sys
from datetime import datetime
from tester.AppTester import AppTester


def main():
	"""
	Entrada principal del sistema.
	"""
	DATE_FORMAT ="%Y-%m-%d %H:%M:%S"
	print(f"\nStart date: {datetime.now().strftime(DATE_FORMAT)}\n")
	print(f"\nResult: {AppTester.start_testing(sys.argv[1:])}")
	print(f"\nEnd date:   {datetime.now().strftime(DATE_FORMAT)}")

if __name__ == "__main__":
	main()
