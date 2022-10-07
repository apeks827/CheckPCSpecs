def out_green(text):
    out = ('\033[32m{}'.format(text))
    print("\033[0m".format(""), end="")
    return out
def out_yellow(text):
    out = '\033[33m{}'.format(text)
    return out
def out_red(text):
    out = '\033[31m{}'.format(text)
    print("\033[0m".format(""), end="")
    return out
def clear_color():
    print("\033[0m".format(""), end="")