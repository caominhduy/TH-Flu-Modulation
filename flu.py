from code.preprocess.epi import preprocess as epi_preprocess
from code.graph.render import epi_render
import argparse

__author__ = 'Duy Cao'
__license__ = 'MIT'
__status__ = 'release'
__url__ = 'https://github.com/caominhduy/TH-Flu-Modulation'
__version__ = '1.0.0'

def main(args):
    if args.test:
        df_flu = epi_preprocess()
        epi_render(df_flu)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='use "-h" or "--help" for more instructions')
    parser.add_argument('-t', '--test', action='store_true', \
                    help='Download and preprocess latest data, train, and predict')
    args = parser.parse_args()
    main(args)
