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
        group.add_argument("+{}".format(shortform), "++{}".format(branch), help="checkout {} in src".format(branch), action="store_const", const=1, default=0)    
        group.add_argument("-{}".format(shortform), "--{}".format(branch), help="remove {} in src".format(branch), action="store_const", const=2, default=0)
    return parser.parse_args()


def createDeployBranch(branch_name, src_path):
    # create local deploy branch
    cmd = "cd {}{} ; git checkout -b {}_deploy ; git checkout {} ; cd .. ; cd ..; git worktree add deploy/{}_deploy".format(src_path, branch_name, branch_name, branch_name)
    os.system(cmd)


def handleFlags(flags):
    print(flags)
    for branch_name in flags:
        # checkout branches
        if flags[branch_name] == 1:
            if "src" in os.path.dirname(os.getcwd()) or "deploy" in os.path.dirname(os.getcwd()):
                cmd = "cd ..; cd ..; git worktree add src/{}".format(branch_name)
                os.system(cmd)
                # create local deploy branch
                createDeployBranch(branch_name, "../../src")
                
            else:    
                cmd = "git worktree add src/{}".format(branch_name)
                os.system(cmd)
                # create local deploy branch
                createDeployBranch(branch_name, "src/")

        # remove branches
        if flags[branch_name] == 2: 
            if "src" in os.path.dirname(os.getcwd()) or "deploy" in os.path.dirname(os.getcwd()):
                cmd = "git worktree remove ../{}".format(branch_name)
                os.system(cmd)
                cmd = "cd ..; cd .. ; cd deploy; rm -r {}; cd ..; git worktree prune".format(branch_name)

            else:    
                cmd = "git worktree remove src/{}".format(branch_name)   
                os.system(cmd)
                cmd = "cd deploy; rm -r {}; cd ..; git worktree prune".format(branch_name)


def main():
    branches = open("branches","r").read().splitlines()
    args = setupArgparse(branches)
    print(args)
    # arguments to dict
    flags = vars(args)
    handleFlags(flags)

    
if __name__ == '__main__':
    main()
