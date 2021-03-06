import CamScan
from argparse import ArgumentParser

def main():

    parser = ArgumentParser(description='Find interesting internet-exposed cameras through the Shodan API.')
    pageInfo = parser.add_mutually_exclusive_group()


    parser.add_argument('--init',
                        help='Initialize Shodan API with your API key (only has to be done on first run)')

    pageInfo.add_argument('-p','--page',
                          help='Specify page or pages to search')

    pageInfo.add_argument('--all',
                          help='Run every page of search results on Shodan',
                          action='store_true')

    parser.add_argument('-d','--dirname',
                        help='specify name of new directory to save images',
                        type=str)

    parser.add_argument('-t','--timeout',
                        help='Time in seconds to wait for each host until giving up',
                        type=int)

    parser.add_argument('-v','--verbose',
                        help='Print each url to terminal as each connection is made, along with its status',
                        action='store_true')

    parser.add_argument('-c','--count',
                        help='Returns # of pages for chosen Shodan query',
                        action='store_true')

    cli_input = parser.parse_args()

    scan = CamScan.CamScan()

    if cli_input.init:
        scan.initShodan(cli_input.init)

    if cli_input.page:
        scan.setPages(eval(cli_input.page))

    if cli_input.all:
        scan.setPages(None)

    if cli_input.dirname:
        scan.dirname = cli_input.dirname

    if cli_input.timeout:
        scan.timeout = int(cli_input.timeout)

    if cli_input.verbose:
        scan.verbose = True

    scan.chooseFromCSV('queries.csv')

    if cli_input.count:
        print(scan.pagesCount(), 'Page(s)')
        choice = input('Run? [y/n]:')

        if choice != 'y':
            raise Exception


    scan.run()
    scan.generatePage()
    scan.showImages()


if __name__ == '__main__':
    main()
