import sys
sys.path.append('../500_common')
import lib_seq

a = "Chrome11"
b = "Profile 1"

path = "../504_kyoto01/data/result.html"

lib_seq.main(a, b, path, waitTime=10, preTime=20, check=True)