""" Run this file to start WMVC monitor"""
import argparse

from wmvc import VCMonitor

parser = argparse.ArgumentParser()
parser.add_argument('-rt', '--runtime', dest='runtime', type=int, help='Runtime for WMVC monitor in seconds.')
parser.add_argument('-logger', '--loggerfilename', dest='loggerfilename', type=str, help='Saved logger file name, default as runlog.log')

if __name__ == '__main__':
    args = parser.parse_args()
    VCMonitor(args.runtime, args.loggerfilename).run()
