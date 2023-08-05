"""
Run some tests
"""

from pklcache import cache
import os

fname = "test_cache.pkl"

def rm_if_present():
    if os.path.isfile(fname):
        os.remove(fname)

def cleanup(func):
    def wrapper(*args, **kwargs):
        rm_if_present()
        func(*args, **kwargs)
        rm_if_present()
    return wrapper


@cleanup
def test1():
    @cache(fname, arg_check=True)
    def foo():
        ret = [(69,96), "who cares about types", 42, [4,2,0]]
        return ret

    # Call foo two times, the first is executed and saves the 
    # result on disk, the second time it just loads the data
    ret = foo()  
    ret_cached = foo()

    assert(ret==ret_cached)
    assert(os.path.isfile(fname))
    print("Test 1: OK")


@cleanup
def test2():
    @cache(fname, enabled=False)
    def foo1():
        ret = "nope"
        return ret

    ret = foo1()
    assert(not os.path.isfile(fname))
    print("Test 2: OK")


@cleanup
def test3():
    @cache(fname, arg_check=True)
    def foo(a,b,c=34,d=34):
        return (a,b,c,d)
    @cache(fname, arg_check=False)
    def foo1(a,b,c=34,d=34):
        return (a,b,c,d)
    ret1 = foo(12,65,d=56)
    ret2 = foo(23,12,c=8)
    ret3 = foo1(23,2000,c=1000)
    assert(ret1 != ret2)
    print(ret1, ret2, ret3)
    print("Test 3: OK")


if __name__ == '__main__':

    test1()

    test2()

    test3()



"""

@cache("merda.sdpl")
def cazzo(er,ar):
    return er+ar

print(cazzo(23,9))
print(cazzo(456,213))
print(cazzo(3412,874,pklcache_enable=False))

"""
