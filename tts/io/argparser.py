import argparse
from tts.mod import tracker, computer, analyser
from tts.lib.data import champions, traits
import tts.data
import os
import glob



def parse():

    path = os.path.abspath(tts.data.__file__).rstrip('__init__.py')
    input_files = [i.lstrip(path) for i in glob.glob(f'{path}*.bin')]

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title='modules',
                                       description='valid subcommands',
                                       help='TTS modules: track, compute, analyse')

    parser.add_argument('--version', action='store_true',
                        help="TraitTrackerSolver version.")

    # Track parser
    track_parser = subparsers.add_parser('track', help='TTS track module.')
    track_parser.add_argument('champs', type=str, nargs='*', choices=[champ["name"].lower() for champ in champions],
                            help="champs in your possession")
    track_parser.add_argument('-i', type=str, help='np file in data folder', choices=input_files, default='8_champs_7+_traits.bin')
    track_parser.add_argument('-mc', type=int, choices=[1, 2, 3, 4, 5], help='maximum cost of champs considered', default=3)
    track_parser.add_argument('-cs', type=int, choices=[6, 7, 8, 9, 10], help='maximum board size considered', default=7)
    track_parser.set_defaults(func=tracker)

    # Compute parser
    compute_parser = subparsers.add_parser('compute', help='Compute module.')
    compute_parser.add_argument('-c', type=int, default=7, help='board size considered')
    compute_parser.add_argument('-t', type=int, default=7, help='minimum active traits considered')
    compute_parser.add_argument('-e', type=str, default=None, choices=[trait["name"].lower() for trait in traits])

    compute_parser.set_defaults(func=computer)

    # Analysis parser
    analyse_parser = subparsers.add_parser('analyse', help='Analysis module.')
    analyse_parser.add_argument('-i', type=str, help='np file in data folder', choices=input_files,
                              default='8_champs_7+_traits.bin')
    analyse_parser.set_defaults(func=analyser)


    args = parser.parse_args()

    return args