#
# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
The mycroft.util.parse module provides various parsing functions for things
like numbers, times, durations etc. It's intention is to convert naturally
expressed concepts into standard computer readable formats. Doing this also
enables localization.

It also provides some useful associated functions like basic fuzzy matching.

The module uses lingua-franca (https://github.com/mycroftai/lingua-franca) to
do most of the actual parsing. However methods may be wrapped specifically for
use in Mycroft Skills.
"""
from warnings import warn
from difflib import SequenceMatcher

# lingua_franca is optional, both lingua_franca and lingua_nostra are supported
# if both are installed preference is given to LN
# "setters" will be set in both lbs
# LN should be functionality equivalent to LF

from mycroft.util.time import now_local
from mycroft.util.log import LOG

try:
    try:
        from lingua_nostra.parse import extract_number, extract_numbers, \
            extract_duration, get_gender, normalize
        from lingua_nostra.parse import extract_datetime as lf_extract_datetime
        from lingua_nostra.time import now_local
    except ImportError:
        from lingua_franca.parse import extract_number, extract_numbers, \
            extract_duration, get_gender, normalize
        from lingua_franca.parse import extract_datetime as lf_extract_datetime
        from lingua_franca.time import now_local
except ImportError:
    def lingua_franca_error(*args, **kwargs):
        raise ImportError("lingua_franca is not installed")

    extract_number = extract_numbers = extract_duration = get_gender = \
        normalize = lf_extract_datetime = lingua_franca_error


def fuzzy_match(x, against):
    """Perform a 'fuzzy' comparison between two strings.
    Returns:
        float: match percentage -- 1.0 for perfect match,
               down to 0.0 for no match at all.
    """
    return SequenceMatcher(None, x, against).ratio()


def match_one(query, choices):
    """
        Find best match from a list or dictionary given an input

        Arguments:
            query:   string to test
            choices: list or dictionary of choices

        Returns: tuple with best match, score
    """
    if isinstance(choices, dict):
        _choices = list(choices.keys())
    elif isinstance(choices, list):
        _choices = choices
    else:
        raise ValueError('a list or dict of choices must be provided')

    best = (_choices[0], fuzzy_match(query, _choices[0]))
    for c in _choices[1:]:
        score = fuzzy_match(query, c)
        if score > best[1]:
            best = (c, score)

    if isinstance(choices, dict):
        return (choices[best[0]], best[1])
    else:
        return best


def _log_unsupported_language(language, supported_languages):
    """
    Log a warning when a language is unsupported

    Args:
        language: str
            The language that was supplied.
        supported_languages: [str]
            The list of supported languages.
    """
    supported = ' '.join(supported_languages)
    LOG.warning('Language "{language}" not recognized! Please make sure your '
                'language is one of the following: {supported}.'
                .format(language=language, supported=supported))


def extract_datetime(text, anchorDate="DEFAULT", lang=None,
                     default_time=None):
    """Extracts date and time information from a sentence.

    Parses many of the common ways that humans express dates and times,
    including relative dates like "5 days from today", "tomorrow', and
    "Tuesday".

    Vague terminology are given arbitrary values, like:

    * morning = 8 AM
    * afternoon = 3 PM
    * evening = 7 PM

    If a time isn't supplied or implied, the function defaults to 12 AM

    Args:
        text (str): the text to be interpreted
        anchorDate (:obj:`datetime`, optional): the date to be used for
            relative dating (for example, what does "tomorrow" mean?).
            Defaults to the current local date/time.
        lang (str): the BCP-47 code for the language to use, None uses default
        default_time (datetime.time): time to use if none was found in
            the input string.

    Returns:
        [:obj:`datetime`, :obj:`str`]: 'datetime' is the extracted date
            as a datetime object in the user's local timezone.
            'leftover_string' is the original phrase with all date and time
            related keywords stripped out. See examples for further
            clarification
            Returns 'None' if no date or time related text is found.
    Examples:
        >>> extract_datetime(
        ... "What is the weather like the day after tomorrow?",
        ... datetime(2017, 06, 30, 00, 00)
        ... )
        [datetime.datetime(2017, 7, 2, 0, 0), 'what is weather like']
        >>> extract_datetime(
        ... "Set up an appointment 2 weeks from Sunday at 5 pm",
        ... datetime(2016, 02, 19, 00, 00)
        ... )
        [datetime.datetime(2016, 3, 6, 17, 0), 'set up appointment']
        >>> extract_datetime(
        ... "Set up an appointment",
        ... datetime(2016, 02, 19, 00, 00)
        ... )
        None
    """
    if anchorDate is None:
        warn(DeprecationWarning("extract_datetime(anchorDate=None) is "
                                "deprecated. This parameter can be omitted."))
    if anchorDate is None or anchorDate == "DEFAULT":
        anchorDate = now_local()
    if not lang:
        from mycroft.configuration.locale import get_default_lang
        lang = get_default_lang()
    return lf_extract_datetime(text,
                             anchorDate,
                             lang,
                             default_time)
