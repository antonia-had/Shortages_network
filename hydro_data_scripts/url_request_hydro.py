"""
This script is adapted from @Nightsphere's telemetrystation-15min.py
from https://github.com/OpenCDSS/cdss-rest-services-examples

Small program to query the HydroBase web services for
historical structure call analysis data for each right in the UCRB.
The web service results are output to stdout or a file.

Run with -h to display the usage.

See the main program at the end of this file.
"""

import argparse
import json
import pprint
import requests
import sys


def build_url(app_data: dict, page_index: int) -> str:
    """
    Build the URL for querying the HydroBase web services,
    for a single parameter.

    Args:
        app_data (dict): Dictionary of command line input.
        page_index (int): Page index, used for multi-page queries.

    Returns:
        URL to use for query.
    """
    # Get needed data, alphabetized
    api_key = get_app_data(app_data, 'API_KEY')
    stationNum = get_app_data(app_data, 'STATION_NUM')
    max_measDate = get_app_data(app_data, 'MAX-MEAS_DATE')
    output_format = get_app_data(app_data, 'OUTPUT_FORMAT')
    page_size = get_app_data(app_data, 'PAGE_SIZE')
    if output_format == 'json':
        # Automatically use pretty print for JSON
        output_format = 'jsonprettyprint'
    min_measDate = get_app_data(app_data, 'MIN-MEAS_DATE')
    #wdid = get_app_data(app_data, 'WDID')

    # Base URL
    url = 'https://dwr.state.co.us/Rest/GET/api/v2/surfacewater/surfacewatertsday/?'
    # Append other parts
    if stationNum != '':
        url = "{}stationNum={}".format(url, stationNum)
    #if wdid != '':
        #url = "{}&wdid={}".format(url, wdid)
    if output_format != '':
        url = "{}&format={}".format(url, output_format)
    if page_size != '':
        url = "{}&pageSize={}".format(url, page_size)
    if page_index != '':
        url = "{}&pageIndex={}".format(url, page_index)
    if min_measDate != '':
        min_measDate = '%2F'.join(min_measDate.split('/'))
        url = "{}&min-measDate={}".format(url, start_date)
    if max_measDate != '':
        max_measDate = '%2F'.join(max_measDate.split('/'))
        url = "{}&max-measDate={}".format(url, end_date)
    if api_key != '':
        api_key = api_key.replace('+', '%2B')
        url = "{}&apiKey={}".format(url, api_key)
    return url


def check_input(app_data: dict) -> None:
    """
    Check input parameters and exit if not correct.
    """
    # Check the output format
    # - required argument so won't be blank
    output_format = get_app_data(app_data, 'OUTPUT_FORMAT')
    error_count = 0
    if (output_format != 'csv') and (output_format != 'json'):
        print_stderr('Output format ({}) is not valid, must be csv or json.'.format(output_format))
        error_count += 1

    # Append .csv or .json to the output file if not already at the end.
    output_file = get_app_data(app_data, 'OUTPUT_FILE')
    if not output_file.endswith(output_format) and output_file != 'stdout':
        output_file = output_file + '.' + output_format
        app_data['OUTPUT_FILE'] = output_file

    # Check the format for start and end dates
    # - optional so could be blank
    min_measDate = get_app_data(app_data, 'MIN-MEAS_DATE')
    if min_measDate is not None and (min_measDate != ''):
        if not check_date(min_measDate):
            print_stderr('Start date ({}) is not valid, must be in format: mm/dd/yyyy'.format(min_measDate))
            error_count += 1
    max_measDate = get_app_data(app_data, 'MAX-MEAS_DATE')
    if max_measDate is not None and (max_measDate != ''):
        if not check_date(max_measDate):
            print_stderr('End date ({}) is not valid, must be in format: mm/dd/yyyy'.format(max_measDate))
            error_count += 1
    if error_count > 0:
        sys.exit(1)


def check_date(date_string: str) -> bool:
    """
    Determine if the date is an valid format mm/dd/yyyy.

    Args:
        date_string(str):  date string to check.

    Returns:
        bool: True if value, False if invalid.
    """
    parts = date_string.split('/')
    if len(parts) != 3:
        print_stderr('Date input ({}) is invalid.'.format(date_string))
        print_stderr('Dates must use format:  mm/dd/yyyy')
        return False
    return True

def get_app_data(app_data: dict, key: str) -> object or None:
    """
    Get application data value from the application data dictionary.

    Args:
        app_data (dict):  Application data from command line.
        key (str):  Name of application data value.

    Returns:
        Object matching the requested key, or None if no value is defined.
    """
    try:
        value = app_data[key]
        # Value is defined so return it
        return value
    except KeyError:
        # Value is not defined
        return None


def parse_command_line() -> dict:
    """
    Parse the command line arguments, warn if they're incorrect, and assign them
    to global constants, since they won't change during this program.

    Returns:
        A dictionary containing the parsed values.
    """
    parser = argparse.ArgumentParser(description='Query the HydroBase web services for call analysis data per water right.')

    # Optional arguments.
    parser.add_argument('--output', metavar='filename', default='stdout',
                        help='Write the output to the specified file instead of stdout.')
    parser.add_argument('--startDate', metavar='start_date', default='',
                        help='The date to start the query in format:  mm/dd/yyyy')
    parser.add_argument('--endDate', metavar='end_date', default='',
                        help='The date to end the query in format: mm/dd/yyyy')
    parser.add_argument('--pageSize', metavar='page_size', default='',
                        help='The page size for the response, used in testing.')
    parser.add_argument('--apiKey', metavar='api_key', default='',
                        help='The API Key to increase response limit from web services.')

    # Required arguments.
    required = parser.add_argument_group('required arguments')
    required.add_argument('--adminNo', metavar='adminNo', help='The right admin number identifier.',
                          required=True)
    required.add_argument('--WDID', metavar='WDID', help='The structure WDID.',
                          required=True)
    required.add_argument('--format', metavar='output_format',
                          help='Format for output: csv or json', required=True)

    # If no arguments are given, print help, and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    # Parse the command line
    args = parser.parse_args()

    # Save arguments in a dictionary and return to the calling code.
    app_data = {}
    app_data['ADMIN_NO'] = args.adminNo
    app_data['WDID'] = args.WDID
    # The following is a list
    app_data['OUTPUT_FORMAT'] = args.format
    app_data['OUTPUT_FILE'] = args.output
    app_data['START_DATE'] = args.startDate
    app_data['END_DATE'] = args.endDate
    app_data['API_KEY'] = args.apiKey
    app_data['PAGE_SIZE'] = args.pageSize
    return app_data


def print_remaining(app_data: dict, page_count: int) -> None:
    """
    Have the first query and determined that the page count is greater than one.
    Since it is, have multiple pages and need to query the rest of the pages for both csv and json.
    print_remaining() prints the pages to stdout, and write_remaining writes the pages to a file.

    Args:
        app_data (dict): Application data from the command line.
        page_count (int): Page count being processed.

    Return:
        None
    """
    output_format = get_app_data(app_data, 'OUTPUT_FORMAT')
    for page_index in range(2, page_count + 1):
        print_stderr("Processing results page {} of {}.".format(page_index, page_count))
        url = build_url(app_data, page_index)
        print_stderr("Request: {}".format(url))
        response = requests.get(url)

        if output_format == 'csv':
            lines = response.text.split('\r\n')
            print(*lines[3::], sep='\n')
        elif output_format == 'json':
            json_obj = json.loads(response.text)
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(json_obj["ResultList"])


def print_stderr(s: str) -> None:
    """
    Print a string to stderr.
    Do this for messages so that output can be redirected.

    Args:
        s (str): String to print.

    Returns:
        None
    """
    print(s, file=sys.stderr)


def process_csv(app_data: dict, first_page: bool, response: str) -> None:
    """
    Append page of results to csv output format.

    Args:
        app_data (dict): Application input from command line.
        first_page (bool): Whether the first page is being written.
        response (str):  Query response.

    Returns:
        None
    """
    print_stderr('Creating csv output format.')
    # response.text is a string, so can split on CRLF
    lines = response.split('\r\n')
    # Determine the amount of pages that the returned data was split into (if any)
    page_count = int(lines[1].split(',')[1])
    print_stderr("Processing results page 1 of {}.".format(page_count))
    output_file = get_app_data(app_data, 'OUTPUT_FILE')

    # Print straight to terminal if no --output argument was received
    if output_file == 'stdout':
        # Write the CSV headers
        print(lines[2])
        # Write the rest of the list from the first data index
        print(*lines[3::], sep='\n')
        # If more than one page, print them all
        if page_count > 1:
            print_remaining(app_data, page_count)

    # Otherwise, write everything but the first two indexes to the named file
    else:
        # First parameter (and its corresponding pages if any)
        if first_page:
            write_file(app_data, lines[2:], first_page=True, last_page=False)
            if page_count > 1:
                write_remaining(app_data, page_count)
        # Second parameter and beyond (and its corresponding pages if any)
        else:
            write_file(app_data, lines[3:], first_page=False, last_page=False)
            if page_count > 1:
                write_remaining(app_data, page_count)

        print_stderr('Data successfully received and written to file \'{}\'\n'.format(output_file))


def process_json(app_data: dict, response: str) -> None:
    """
    Append page of results to JSON output format.

    Args:
        app_data (dict): Application input from command line.
        response (str):  Query response.

    Returns:
        None
    """
    # Retrieve the data and put into a JSON object
    print_stderr('Creating json output format.')
    json_obj = json.loads(response)
    page_count = json_obj["PageCount"]
    print_stderr("Processing results page 1 of {}.".format(page_count))
    output_file = get_app_data(app_data, 'OUTPUT_FILE')
    # Printing to terminal here
    if output_file == 'stdout':
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(json_obj["ResultList"])

        if page_count > 1:
            print_remaining(app_data, page_count)
    # Writing to a file here
    else:
        if page_count == 1:
            write_file(app_data, json_obj["ResultList"], first_page=True, last_page=True)
            print_stderr('Data successfully received and written to file \'{}\'\n'.format(output_file))
        if page_count > 1:
            write_remaining(app_data, page_count)
            print_stderr('Data successfully received and written to file \'{}\'\n'.format(output_file))


def run_batch(app_data: dict) -> None:
    """
    The principal function in the program.  Given the arguments specified on command line,
    fetch the data from the HydroBase web service and output in requested format.
    A single stationid can be specified, but multiple parameters can be requested.

    Args:
        app_data(dict): Dictionary of values from the command line.

    Returns:
        None
    """

    # Whether csv headers should be written at the top of output
    first_page = True

    print_stderr('Fetching data...')

    # Build the URL for requested query.
    # Query first to see if get back more than one page from the database.
    url = build_url(app_data, 1)
    headers = {'Accept-Encoding': 'gzip'}
    print_stderr("Request: {}".format(url))
    response = requests.get(url, headers=headers)

    # Through some means (usually incorrect parameter name) nothing was returned from the database
    if 'zero records from CDSS' in response.text:
        print_stderr('\n    error: {}'.format(response.text))

    output_format = get_app_data(app_data,'OUTPUT_FORMAT')
    if output_format == 'json':
        # Process JSON
        process_json(app_data, response.text)
    elif output_format == 'csv':
        # Process CSV
        process_csv(app_data, first_page, response.text)
        first_page = False
    else:
        print_stderr('Unknown output format {}'.format(output_format))


def write_remaining(app_data: dict, page_count: int) -> None:
    """
    The data returned has more than one page, so write the rest of the pages to file.

    Args:
        app_data (dict):  Application data from command line.
        page_count (int):  Page being processed.

    Returns:
        None
    """
    output_format = get_app_data(app_data, 'OUTPUT_FORMAT')
    for page_index in range(2, page_count + 1):
        url = build_url(app_data, page_index)
        print_stderr("Request: {}".format(url))
        response = requests.get(url)

        if output_format == 'csv':
            lines = response.text.split('\r\n')
            write_file(app_data, lines[3:], first_page=False, last_page=False)
        elif output_format == 'json':
            json_obj = json.loads(response.text)
            if page_index == page_count:
                write_file(app_data, json_obj["ResultList"], first_page=False, last_page=True)
            else:
                write_file(app_data, json_obj["ResultList"], first_page=False, last_page=False)


def write_file(app_data: dict, lines: list, first_page: bool, last_page: bool) -> None:
    """
    Write the data to a file, appending if necessary.

    Args:
        app_data (dict): Dictionary of application data.
        lines (list): Lines to write to the file.
        first_page (bool): Indicates if writing the first page.
        last_page (bool): Indicates if writing the last page.

    Returns:
        None
    """

    output_file = get_app_data(app_data, 'OUTPUT_FILE')
    output_format = get_app_data(app_data, 'OUTPUT_FORMAT')

    with open('./fetched_data/'+output_file, 'a') as outputFile:
        if output_format == 'csv':
            # Write CSV
            # Write the CSV to file
            for item in lines:
                outputFile.write(item + '\n')
        elif output_format == 'json':
            # Write JSON
            # Write the beginning of the JSON object on the first page
            if first_page:
                outputFile.write('{ \"ResultList\": [')
            # Get the number of data lines in the page to determine if at the last line
            page_length = len(lines)
            index = 0
            for item in lines:
                # If on the last line of the page AND the last page, end
                # the list from ResultList (don't want a comma at the end).
                if index == page_length - 1 and last_page:
                    outputFile.write(json.dumps(item, indent=4) + '\n')
                else:
                    outputFile.write(json.dumps(item, indent=4) + ',\n')
                index = index + 1
            # Double check it's the last page and finish writing the JSON object. After
            # that the file will be closed.
            if last_page:
                outputFile.write(']}')


def main() -> None:
    """
    Main function for the program.
    """

    # Parse the command line
    app_data = parse_command_line()

    # Check command line parameters
    check_input(app_data)

    # Perform the web service request in batch mode
    run_batch(app_data)


if __name__ == '__main__':
    """
    Main entry point for the program.
    """
    # Run the main function.
    main()