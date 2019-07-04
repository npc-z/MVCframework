import random
import time


def log(*args, **kwargs):
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(int(time.time()))
    formatted = time.strftime(time_format, localtime)
    print(formatted, *args, **kwargs)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(formatted, *args, file=f, **kwargs)


def random_string():
    """
    生成一个随机的字符串
    """
    seed = 'bdjsdlkgjsklgelgjelgjsegker234252542342525g'
    s = ''
    for i in range(16):
        s += random.choice(seed)
    return s
