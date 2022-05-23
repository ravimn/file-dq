import os
import glob
import datetime
from dateutil.parser import parse
from concurrent.futures import ThreadPoolExecutor

def validateMultipleFiles(files=None, headerInfo=None, delim=','):
    futures_list = []
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for file in files:
            futures = executor.submit(validateFile, file, headerInfo, delim)
            futures_list.append(futures)

        for future in futures_list:
            try:
                result = future.result()
                results.append(result)
            except Exception:
                results.append(None)

    return results

def validateFile(filename=None, headerInfo=None, delim=','):
    """
    Return number of rows that failed validation.

    :param file: str, Path to file to be validated.
    :param headerInfo: List of header type
    """

    failCount = 0;
    with open(filename, 'r', encoding='UTF-8') as file:
        while (line := file.readline().rstrip()):
            if not validateRow(line, headerInfo, delim):
                failCount = failCount + 1

    return failCount

def validateRow(row=None, headerInfo=None, delim=','):
    if row is None:
        raise RuntimeException('row is not defined')

    if headerInfo is None:
        raise RuntimeException('headerInfo is not defined')


    out = row.split(delim)
    r_len = len(out)
    h_len = len(headerInfo)

    if r_len != h_len:
        raise RuntimeException('counts dont match')

    i = 0
    isValidRow = True
    while i < r_len:
        try:
            if not validateType(out[i], headerInfo[i]):
                isValidRow = False
                break
        except RuntimeError as e:
            print('Validation error ', e)
            isValidRow = False
            break

        i = i + 1

    return isValidRow

def validateType(value=None, expectedType=None):
    print ( 'Value [{}] HeaderType [{}] ValueType [{}]'.format(value, expectedType, type(value)))

    if value is None:
        raise RuntimeError('Value is not set')

    if expectedType not in ('date', 'bool', 'num', 'str'):
        raise RuntimeError('expectedType is not valid')

    if expectedType == 'date':
        return is_date(col)

    if expectedType == 'bool':
        return isinstance(value, bool)

    if expectedType == 'num':
        return is_number(value)

    if expectedType == 'str':
        return isinstance(value, str)

    return False


def is_number(string):
    try:
        int(string)
        return True
    except ValueError:
        pass

    try:
        float(string)
        return True
    except ValueError:
        pass

    return False


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def main():
    headerInfo = ('str','num','str','str')

    #Get list of files.  Split files using unix split command
    files = glob.glob('test*')
    print ('Validate file of multipleFiles is', validateMultipleFiles(files, headerInfo))

if __name__ == "__main__":
    main()
