from tts.modules.tracker import track
from tts.modules.compute import compute

def tracker(args):
    track.solve_comp(args.champs, args.i, args.mc, args.cs)

def computer(args):
    compute.run_computation(args.c, args.t)