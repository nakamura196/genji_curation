import sys
sys.path.append('../500_common')
import lib_reserve

a = "Chrome31"
b = "Profile 3"

lib_reserve.main(a, b,  True, waitTime=10)