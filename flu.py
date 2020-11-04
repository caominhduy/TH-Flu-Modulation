from code.preprocess.epi import preprocess as epi_preprocess
from code.preprocess.weather import preprocess as noaa_preprocess
from code.graph.render import epi_render, station_render, weather_render
from code.model.merger import merge
from code.model.regress import regress_plot
import argparse

__author__ = 'Duy Cao'
__license__ = 'MIT'
__status__ = 'release'
__url__ = 'https://github.com/caominhduy/TH-Flu-Modulation'
__version__ = '1.0.0'

def main(args):
    if args.test:
        # df_flu = epi_preprocess()
        # epi_render(df_flu)
        # df_weather = noaa_preprocess('station')
        # station_render(df_weather, 'All-Station')
        # noaa_preprocess('temp')
        # weather_render()
        # merge()
        # regress_plot('temp')
        # regress_plot('humid')
        regress_plot('test')
    if args.graph:
        df_flu = epi_preprocess()
        epi_render(df_flu)
        df_weather = noaa_preprocess('station')
        station_render(df_weather, 'All-Station')
        noaa_preprocess('temp')
        weather_render()
        merge()
        regress_plot('temp')
        regress_plot('humid')
    if args.no_graph:
        df_flu = epi_preprocess()
        df_weather = noaa_preprocess('station')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='use "-h" or "--help" for more instructions')
    parser.add_argument('--graph', action='store_true', \
                        help='Process data and plot maps and graphs')
    parser.add_argument('--no_graph', action='store_true', \
                        help='Process data only')
    parser.add_argument('-t', '--test', action='store_true', \
                    help='Test')
    args = parser.parse_args()
    main(args)
