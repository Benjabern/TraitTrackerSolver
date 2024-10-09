from tts.io.argparser import parse

def main():

    args = parse()

    args.func(args)


if __name__ == "__main__":
    main()
