import sys
sys.path.append('../500_common')
import lib_reserve

a = "Chrome1res"
b = "Profile 1"

path = "../504_kyoto01/data/result.html"

lib_reserve.main(a, b, None, waitTime=10, preTime=20)
