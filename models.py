import re
import json

# compiling all the regular expressions
re_oem = re.compile(r'([^.]+)\.{3,} *(\d{4}) *-* *(\d{4})*')
re_options = re.compile(r'(.*):(.*)')
re_part = re.compile(r'^(?=.*[0-9])([A-Z0-9]+)$')
re_desc = re.compile(r'^(?!(.*\d.*\d))[^:;\.]*$')

def oem_year(line: str) -> tuple:
    """
    Function that takes in a string and tests to see if it matches the pattern of oem lines, if so then parse
    and return the make and years and also the key to the parent category,
    if not the pattern of oem lines, then return None

    :param line: a string that is passed in to be parsed
    :return: the parsed data or None
    """

    match = re_oem.search(line)

    if match:
        if match.group(3):
            years = list(range(int(match.group(3)), int(match.group(2)) + 1))
            rtn = {'oem': match.group(1).strip(), 'years': years}
        else:
            rtn = {'oem': match.group(1).strip(), 'years': [int(match.group(2))]}

        return 'oems', rtn

    else:
        return 'oems', None


def options(line: str) -> tuple:
    """
    Function that takes in a string and tests to see if it matches the pattern of option lines,
    if so then parse and return option and also the key to the parent category,
    if not the pattern of options, then return None

    :param line: a string that is passed in to be parsed
    :return: the parsed data or None
    """

    match = re_options.search(line)

    if match:
        rtn = {'option_name': match.group(1).strip(), 'value': match.group(2).strip()}
        return 'options', rtn
    else:
        return 'options', None


def part_numbers(line: str) -> tuple:
    """
    Function that takes in a string and tests to see if it matches the pattern of part number lines,
    if so then parse and return part number(s) and also the key to the parent category,
    if not the pattern of part numbers, then return None

    :param line: a string that is passed in to be parsed
    :return: the parsed data or None
    """

    # if ; exists or there is a single part number(start with letter or number)
    if (';' in line and not ':' in line) or re_part.search(line):
        match = re.findall(r'\w+', line)

        if match:
            return 'part_numbers', match
        else:
            return 'part_numbers', None
    else:
        return 'part_numbers', None


def description(line: str) -> tuple:
    """
    Function that takes in a string and tests to see if it matches the pattern of description lines,
    if so then parse and return description and also the key to the parent category,
    if not the pattern of description lines, then return None

    :param line: a string that is passed in to be parsed
    :return: the parsed data or None
    """
    match = re_desc.match(line)  # excludes multiple line material number, options, oems

    if match:
        return 'description', match.group(0)
    else:
        return 'description', None


def titles(line: str) -> tuple:
    """
    Function that takes in a string and tests to see if it matches one of the titles,
    if so then return title and also the key to the parent category,
    if not then return None

    :param line: a string that is passed in to be checked for one of titles
    :return: the title or None
    """
    with open('titles.txt', 'r') as f:
        lines = f.readlines()

    lines = [l.strip('\n') for l in lines]

    if line in lines:
        return 'title', line
    else:
        return 'title', None


def json_dump(data):
    """
    Function that takes data as a dictionary and dumps it into a json file
    :param data: a dictionary filled with all the data
    :return: no return
    """
    with open('test.json', 'w') as f:
        json.dump(data, f)


def cleanup(entry):
    """
    Function that cleans up weird spacing in descriptions
    :param entry: part entry
    :return: no return
    """
    entry.data['description'] = entry.data['description'].strip()


# Class that holds each part entry within the dictionary
class PartEntry:
    def __init__(self):
        self.data = {'title': None,
                     'description': "",
                     'part_numbers': [],
                     'options': [],
                     'oems': []
                     }
        self.title_satisfied = False
        self.desc_satisfied = False
        self.pn_satisfied = False
        self.options_satisfied = False
        self.oems_satisfied = False
        self.starting_line_number = None
        self.ending_line_number = None
