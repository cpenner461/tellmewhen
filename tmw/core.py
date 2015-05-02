
import logging
import sys
import time
import re

import requests

#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TMWCoreException(Exception):
    pass

# types of checks we can do for events
event_types = [
    'status_code', 
    'string_match',
    'regex_match',
]

def check_until(url, check_type, check_value, frequency, num_checks):
    """Check url until the specified condition is met"""

    checks_done = 0
    results = False

    while (checks_done < num_checks or num_checks == 0) and not results:
        
        checks_done += 1
        results = check_once(url, check_type, check_value)

        if results or checks_done == num_checks:
            return results

        sys.stdout.write('.')
        sys.stdout.flush()
        
        time.sleep(frequency)

    sys.stdout.write('\n')
    sys.stdout.flush()
    return results

def check_once(url, check_type, check_value):
    """Check a url once"""

    if check_type == 'status_code':
        try:
            check_value = int(check_value)
        except ValueError:
            raise TMWCoreException("Status codes must be integers")

        return status_check(url, check_value)
    elif check_type == 'string_match':
        return string_check(url, check_value)
    if check_type == 'regex_match':
        return regex_check(url, check_value)
    else:
        raise TMWCoreException('Invalid check type')

def status_check(url, expected_code):
    """Check a url for the expected_code
    return True/False"""

    value = _check_code(
            _get_url(url), 
            expected_code
        )
    logger.debug('value is %s', value)
    return value

def string_check(url, match_string):
    """Check a url for the match_string
    return True/False"""

    return _check_contains(
            _get_url(url),
            match_string
        )

def regex_check(url, regex):
    """Checks a url to see if it matches the regex
    return True/False"""
    return _check_matches(
            _get_url(url),
            regex
        )

def _get_url(url):
    """Get a url
    return the response object"""
    return requests.get(url)

def _check_code(response, expected_code):
    """Check the response code from a response object
    return True/False
    """
    logger.debug('expected_code: %s', expected_code)
    logger.debug('status_code: %s', response.status_code)
    return response.status_code == expected_code

def _check_contains(response, match_string):
    """Check the response body for the match_string
    return True/False
    """
    return response.text.find(match_string) > 0

def _check_matches(response, regex):
    """Check to see if the response body matches a regex
    return True/False
    """
    return re.search(regex, response.text)

