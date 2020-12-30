import sys
sys.path.append('../500_common')
import lib_reserve

a = "Chrome13"
b = "Profile 1"

lib_reserve.main(a, b, False, waitTime=60)
