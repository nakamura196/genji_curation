import sys
sys.path.append('../500_common')
import lib_delete

a = "Chrome12"
b = "Profile 1"

manifests = ["https://kotenseki.nijl.ac.jp/biblio/100153620/manifest"]

lib_delete.main(a, b, manifests)

