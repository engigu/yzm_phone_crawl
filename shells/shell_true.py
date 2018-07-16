import sys
import time


def main():
    if sys.argv[1] == 'shell':
        r = input('确定输入a:')
        if r.upper() == 'A':
            print(' pressed A')
            # time.sleep(1)
            r_ = input('二次确定输入b:')
            if r_.upper() == 'B':
                print(' pressed B')


if __name__ == '__main__':
    main()
