class ParamsObj():
    def __init__(self, **kwargs):
        for key, item in kwargs.items():
            self.__setattr__(key, item)


def main():
    po = ParamsObj(a=123, b=555, c=7777)
    print(po.a,po.b,po.c)


if __name__=="__main__":
    main()

