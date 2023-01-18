from src.logger import Logger


def __test_funct(arg, end):
    return arg + end


def test_prod():
    print('-' * 10 + 'Testing prod' + '-' * 10)
    log_tester = Logger(is_poduction=True, base_func=__test_funct)
    tmp = log_tester.v('Verbose message,  INVISIBLE')
    print(tmp)
    assert tmp is None
    tmp = log_tester.i('Info message,     INVISIBLE')
    print(tmp)
    assert tmp is None
    tmp = log_tester.w('Warning message,  INVISIBLE')
    print(tmp)
    assert tmp is None
    tmp = log_tester.e('Error message,    VISIBLE')
    print(tmp)
    assert tmp is not None


def test_testing():
    print('-' * 10 + 'Testing test' + '-' * 10)
    log_tester = Logger(is_poduction=False, base_func=__test_funct)
    tmp = log_tester.v('Verbose message,  VISIBLE')
    print(tmp)
    assert tmp is not None
    tmp = log_tester.i('Info message,     VISIBLE')
    print(tmp)
    assert tmp is not None
    tmp = log_tester.w('Warning message,  VISIBLE')
    print(tmp)
    assert tmp is not None
    tmp = log_tester.e('Error message,    VISIBLE')
    print(tmp)
    assert tmp is not None


test_prod()
test_testing()
