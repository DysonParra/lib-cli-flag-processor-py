import sys
from datetime import datetime
from tester.AppTester import *

DATE_FORMAT ="%Y-%m-%d %H:%M:%S"

print(f"\nStart date: {datetime.now().strftime(DATE_FORMAT)}\n")
print(f"\nResult: {startTesting(sys.argv[1:])}")
print(f"\nEnd date:   {datetime.now().strftime(DATE_FORMAT)}")
