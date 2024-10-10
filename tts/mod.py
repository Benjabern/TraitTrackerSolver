from tts.modules.tracker import track
from tts.modules.compute import compute
from tts.modules.analyse import analyse

def tracker(args):
    track.solve_comp(args.champs, args.i, args.mc, args.cs)

def computer(args):
    compute.run_computation(args.c, args.t, args.e, args.nonpy)

def analyser(args):
    analyse.run_analysis(args.i)