#!/usr/bin/python3
import argparse, os

def setupArgparse(branches):
    parser = argparse.ArgumentParser(description="Checkout your project branches", prefix_chars='-+')
    # parser.add_argument("-d", "--deploy", help="additional develop branch", action="store_true")

    group = parser.add_mutually_exclusive_group()
    for branch in branches:
        splitted = branch.split("_")
        shortform = ""
        for word in splitted:
            shortform += word[0]
        group.add_argument("+{}".format(shortform), "++{}".format(branch), help="checkout {} in src".format(branch), action="store_true")    
    return parser.parse_args()

def main():
    branches = open("branches","r").read().splitlines()
    args = setupArgparse(branches)
    test = vars(args)
    for branch_name in test:
        if test[branch_name]:
            cmd = "git worktree add src/{}".format(branch_name)
            os.system(cmd)

if __name__ == '__main__':
    main()
