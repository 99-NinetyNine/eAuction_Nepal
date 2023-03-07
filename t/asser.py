def f1():
    assert 2 == True

def f2():
    try:
        f1()
    except Exception as e:
        print("error")

f2()