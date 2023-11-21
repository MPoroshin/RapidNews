import multiprocessing as mp


def main():
    prcs = []
    for module in ['newsProcess', 'botProcess']:
        prc = mp.Process(target=import_module, args=(module,))
        prc.start()
        prcs.append(prc)

    for prc in prcs:
        prc.join() #миша реально жопа


def import_module(module):
    import sys
    sys.modules[module] = __import__(module)


if __name__ == '__main__':
    main()
