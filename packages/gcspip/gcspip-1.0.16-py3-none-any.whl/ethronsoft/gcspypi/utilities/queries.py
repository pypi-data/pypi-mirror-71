from __future__ import division
from ethronsoft.gcspypi.package.package import Package
from ethronsoft.gcspypi.utilities.version import complete_version
from ethronsoft.gcspypi.exceptions import InvalidParameter
import functools
from packaging.version import parse


def cmp(a, b):
    if a > b:
        return 1
    elif a < b:
        return -1
    else:
        return 0


def pkg_comp_version(v1, v2):
    """
    Given version v1 and v2,
    with format MM.mm.bb and tokens
    [MM, mm, bb]
    let's compare them token by
    token, converting tokens starting with a 0
    in decimals
    """
    version1 = parse(v1)
    version2 = parse(v2)

    if version1 > version2:
        return 1
    elif version2 > version1:
        return -1
    else:
        return 0

    # def leading_zeroes(v):
    #     res = 0
    #     for x in v:
    #         if x == "0":
    #             res += 1
    #         else:
    #             break
    #     return res
    # v1 = v1.split(".")
    # v2 = v2.split(".")
    # # if one version has more digits than the other make them equal size
    # # by appending a 0 as padding. This is useful for development if
    # # someone wants to tag versions like 1.0.0.dev1
    # if len(v1) == 3:
    #     v1.append("0")
    # if len(v2) == 3:
    #     v2.append("0")
    # for i in range(4):
    #     # If the length of one token is bigger 1 eg. dev1 extract the number
    #     if len(v1[i]) > 1:
    #         v1[i] = str([int(s) for s in v1[i] if s.isdigit()][0])
    #     if len(v2[i]) > 1:
    #         v2[i] = str([int(s) for s in v2[i] if s.isdigit()][0])
    #     v1i = float(v1[i]) / (10 ** leading_zeroes(v1[i]))
    #     v2i = float(v2[i]) / (10 ** leading_zeroes(v2[i]))
    #     if v1i > v2i:
    #         return 1
    #     elif v1i < v2i:
    #         return -1
    # return 0
    
    
def pkg_comp_name_version(i, x):
    if i.name == x.name:
        return pkg_comp_version(i.version, x.version)
    elif i.name > x.name:
        return 1
    else:
        return -1


def pkg_comp_name(i, x):
    if i.name == x.name:
        return 0
    elif i.name > x.name:
        return 1
    else:
        return -1


def cmp_bisect(list, key, cmp=cmp):
    lo = 0
    hi = len(list) - 1
    mid = 0
    while lo <= hi:
        mid = lo + ((hi - lo) // 2)
        i = cmp(list[mid], key)
        if i < 0:
            lo = mid + 1
        elif i > 0:
            hi = mid - 1
        else:
            break
    if list and cmp(key, list[mid]) <= 0:
        return mid
    else:
        return mid + 1


def floor(list, key, cmp=cmp):
    if not list:
        return None
    indx = cmp_bisect(list, key, cmp)
    if indx >= len(list):
        return list[-1]
    c = cmp(list[indx], key)
    if c <= 0:
        return list[indx]
    else:
        return list[indx - 1] if indx > 0 else None


def ceiling(list, key, cmp=cmp):
    if not list:
        return None
    indx = cmp_bisect(list, key, cmp)
    if indx >= len(list):
        return None

    return list[indx]


def lower(list, key, cmp=cmp):
    if not list:
        return None
    indx = cmp_bisect(list, key, cmp)
    if indx >= len(list):
        return list[-1]

    return list[indx - 1] if indx > 0 else None


def higher(list, key, cmp=cmp):
    if not list:
        return None
    indx = cmp_bisect(list, key, cmp)
    if indx >= len(list):
        return None
    c = cmp(list[indx], key)
    if c <= 0:
        return list[indx + 1] if indx < len(list) - 1 else None
    else:
        return list[indx]


def equal(list, key, cmp=cmp):
    if not list:
        return None
    indx = cmp_bisect(list, key, cmp)
    if indx >= len(list):
        return None
    return list[indx] if cmp(list[indx], key) == 0 else None


def pkg_range_query(list, pkg_name, op1="", v1="", op2="", v2=""):
    # empty version means last version
    if op1 == "==" or not op1:
        if v1:
            x = equal(list, Package(pkg_name, complete_version(v1)), pkg_comp_name_version)
        else:
            x = lower(list, Package(pkg_name + 'x01', ""), pkg_comp_name)
    elif op1 == "<":
        if v1:
            x = lower(list, Package(pkg_name, complete_version(v1)), pkg_comp_name_version)
        else:
            x = lower(list, Package(pkg_name + 'x01', ""), pkg_comp_name)
            x = lower(list, x, pkg_comp_name)
    elif op1 == ">":
        if v1:
            x = higher(list, Package(pkg_name, complete_version(v1)), pkg_comp_name_version)
        else:
            x = None
    elif op1 == "<=":
        if v1:
            x = floor(list, Package(pkg_name, complete_version(v1)), pkg_comp_name_version)
        else:
            x = lower(list, Package(pkg_name + 'x01', ""), pkg_comp_name) #lower than last
    elif op1 == ">=":
        if v1:
            x = ceiling(list, Package(pkg_name, complete_version(v1)), pkg_comp_name_version)
        else:
            x = lower(list, Package(pkg_name + 'x01', ""), pkg_comp_name)
    else:
        raise InvalidParameter("Invalid operator" + op1)

    if x and x.name != pkg_name:
        return None

    if v2:
        if op2 == "==":
            # return equal(list, Package(pkg_name, complete_version(v2)), pkg_comp_name_version)
            return x if x.version == complete_version(v2) else None
        elif op2 == "<":
            return x if x.version < complete_version(v2) else None
        elif op2 == ">":
            return x if x.version > complete_version(v2) else None
        elif op2 == "<=":
            return x if x.version <= complete_version(v2) else None
        elif op2 == ">=":
            return x if x.version <= complete_version(v2) else None
        else:
            raise InvalidParameter("Invalid operator" + op2)
    else:
        return x


def get_package_type(path):
    if ".zip" in path:
        return "SOURCE"
    elif ".tar" in path:
        return "SOURCE"
    elif ".whl" in path:
        return "WHEEL"
    else:
        raise InvalidParameter("Unrecognized file extension. expected (.zip|.tar*|.whl) Actual file: {0}".format(path))


def items_to_package(items, unique=False):
    res = []
    s = set([])
    for item in items:
        tokens = item.split("/")
        name = tokens[-3]
        version = tokens[-2]
        if unique:
            key = "{}/{}".format(name, version)
            if key not in s:
                res.append(Package(name, version, type=get_package_type(item)))
                s.add(key)
        else:
            res.append(Package(name, version, type=get_package_type(item)))
    return sorted(res, key=functools.cmp_to_key(pkg_comp_name_version))
