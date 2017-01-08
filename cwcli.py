#!/usr/bin/python

from cw import CacheWarmer
import sys, getopt
import os

def main(argv):
    sitemap_url = ''
    threads_count = 100
    enable_crawler = False
    try:
        opts, args = getopt.getopt(argv,"hs:n:C",["sitemap=","threads="])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            sys.exit()
        if opt in ("-s", "--sitemap"):
            sitemap_url = arg.strip("'\"")
        elif opt in ("-n", "--threads"):
            threads_count = int(arg)
        elif opt in ("-C"):
            enable_crawler = True
    if sitemap_url != '':
        cw = CacheWarmer(sitemap_url, threads_count)
        cw.app.enable_crawler = enable_crawler
        cw.start()

def printHelp():
    file = os.path.basename(__file__)
    print file + ' -s|--sitemap <url> [-c|--threads <threads count>|-C]'
    print ' '
    print '	-s|--sitemap	-	URL a of website sitemap.'
    print '	-n|--threads	-	Optional. A number of threads. 100 by default.'
    print '	-C		-	Optional. Enable a link crawler. A link crawler disabled if an argument is missing.'

if __name__ == "__main__":
    main(sys.argv[1:])
