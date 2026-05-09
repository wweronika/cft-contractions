from entropy_graph_2 import EntropyGraph2
from pairing_picker import PairingPicker

g = EntropyGraph2(2)
picker = PairingPicker(g, outdir="pairings")
picker.show()