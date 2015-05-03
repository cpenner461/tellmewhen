'''

This is where the core functionality of checking URLs and deciding if they
match the specified conditions live.  
'''
import logging
import time
import re

import requests

logger = logging.getLogger(__name__)

class TMWCoreException(Exception):
    """Generic TMW exception"""
    pass

# types of checks we can do for events
event_types = [
    'status_code', 
    'string_match',
    'regex_match',
]

def check_until(url, check_type, check_value, frequency, num_checks, index = None):
    """Check url until the specified condition is met"""

    checks_done = 0
    results = False

    while (checks_done < num_checks or num_checks == 0) and not results:

        checks_done += 1
        results = check_once(url, check_type, check_value)

        if results or checks_done == num_checks:
            return (results, checks_done, index)

        time.sleep(frequency)

    return (results, checks_done, index)

def check_once(url, check_type, check_value):
    """Check a url once"""

    if check_type == 'status_code':
        try:
            check_value = int(check_value)
        except ValueError:
            raise TMWCoreException("Status codes must be integers")

        return _status_check(url, check_value)
    elif check_type == 'string_match':
        return _string_check(url, check_value)
    if check_type == 'regex_match':
        return _regex_check(url, check_value)
    else:
        raise TMWCoreException('Invalid check type')

def _status_check(url, expected_code):
    """Check a url for the expected_code
    return True/False"""

    value = _check_code(
            _get_url(url), 
            expected_code
        )
    logger.debug('value is %s', value)
    return value

def _string_check(url, match_string):
    """Check a url for the match_string
    return True/False"""

    return _check_contains(
            _get_url(url),
            match_string
        )

def _regex_check(url, regex):
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
    results = re.search(regex, response.text)
    return results != None

