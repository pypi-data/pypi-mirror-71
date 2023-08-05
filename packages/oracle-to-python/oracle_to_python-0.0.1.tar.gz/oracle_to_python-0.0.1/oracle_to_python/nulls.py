
def nvl(value, replace_if_value_is_null):
    """
    nvl function Converts NULL value to actual value.

    nvl(None,5) will return 5
    """
    return value if value else replace_if_value_is_null


def nvl2(expr1, value_if_expr1_not_null, value_if_expr1_null):
    """
    If expr1 is not None, nvl2 returns expr2. If expr1 is None, nvl2 returns expr3

    nvl2(None,5,7) will return 7 and

    nvl2('dEexams',5,7) will return 5
    """
    return value_if_expr1_not_null if expr1 else value_if_expr1_null


def nullif(value1, value2):
    """
    The nullif function returns a None value if both parameters are equal in value.
    If the parameters are not equal, it returns the value of the first parameter.

    nullif(1,1) will retun None and

    nullif(1,2) will return 1
    """
    return None if value1 == value2 else value1

def coalesce(list_of_values):
    """
    The coalesce function returns the first non-None or none-blank or non-false value in list.
    If all expressions are None it returns None. The following would return '5'.

    coalesce(None, None, '5')
    """
    result= list([v for v in list_of_values if v])
    return result[0] if result else None


if __name__ == '__main__':
    print(f"NVL->{nvl(None, 'ABC')}")
    print(f"NVL2->{nvl2('NotNull', 'FirstParamNotNull', 'FirstParamNull')}")
    print(f"NVL2->{nvl2(None, 'FirstParamNotNull', 'FirstParamNull')}")
    print(f"NULLIF->{nullif('BothValueEqual','BothValueEqual')}")
    print(f"NULLIF->{nullif('BothValueNotEqual','FirstValueIsBothValueNotEqual')}")
    print(f"coalesce->{coalesce(['x',None,'',None,'3','w'])}")
