import argparse

def setupArgparse():
    parser = argparse.ArgumentParser(description="Checkout your project branches")
    parser.add_argument("-d", "--deploy", help="additional develop branch", action="store_true")

    group = parser.add_mutually_exclusive_group()
    # group.add_argument("-d", "--dev", help="additional develop branch", action="store_true")
    group.add_argument("-m", "--main", help="checkout main project", action="store_true")
    group.add_argument('-b', '--bootloader', help="checkout bootloader project", action="store_true")

    return parser.parse_args()


def main():
    args = setupArgparse()
    if args.main:
        command = "mkdir src && git worktree add src/webportal && git worktree add src/tx_firmware && git worktree add src/tx_app_server"
        print(args.main)


if __name__ == '__main__':
    main()
