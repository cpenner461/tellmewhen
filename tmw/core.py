
import logging
import sys
import time

import requests

#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TMWCoreException(Exception):
    pass

# types of checks we can do for events
event_types = [
    'status_code', 
    'string_match',
]

def check_until(url, check_type, check_value, frequency, num_checks):
    """Check url until the specified condition is met"""

    checks_done = 0
    results = False

    while (checks_done < num_checks or num_checks == 0) and not results:
        
        checks_done += 1
        results = check_once(url, check_type, check_value)

        if results or checks_done == num_checks:
            return (results, checks_done)

        sys.stdout.write('.')
        sys.stdout.flush()
        
        time.sleep(frequency)

    sys.stdout.write('\n')
    sys.stdout.flush()
    return (results, checks_done)

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


