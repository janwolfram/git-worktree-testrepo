#!/usr/bin/python3
import argparse, os

def setupArgparse(branches):
    parser = argparse.ArgumentParser(description="Checkout your project branches", prefix_chars='-+')
    parser.add_argument("--deploy", action="store_true", help="set deploy branches to current status")

    # automatically create flags from branches.txt
    group = parser.add_mutually_exclusive_group()
    for branch in branches:
        splitted = branch.split("_")
        shortform = ""
        for word in splitted:
            shortform += word[0]
        # flag to checkout a branch + deploy branch
        group.add_argument("+{}".format(shortform), "++{}".format(branch), help="checkout {} in src".format(branch), action="store_const", const=1, default=0)    
        # flag to remove a branch + deploy branch
        group.add_argument("-{}".format(shortform), "--{}".format(branch), help="remove {} in src".format(branch), action="store_const", const=2, default=0)
    return parser.parse_args()


def createDeployBranch(branch_name, src_path):
    cmd = "cd {}{} ; git checkout -b {}_deploy ; git checkout {} ; cd .. ; cd ..; git worktree add deploy/{}_deploy".format(src_path, branch_name, branch_name, branch_name, branch_name)
    os.system(cmd)


def updateDeployBranches(src_path):
    os.chdir(src_path)
    my_branches = os.listdir(os.getcwd())
    for branch in my_branches:
        cmd = "cd {} && git pull".format(branch)
        os.system(cmd)

    os.chdir("../deploy")
    my_deploy_branches = os.listdir(os.getcwd())
    for deploy_branch in my_deploy_branches:
        parent_branch = deploy_branch[:-7]
        cmd = "cd {} ; git rebase {}".format(deploy_branch, parent_branch)
        os.system(cmd)


def handleFlags(flags, branches):
    if flags["deploy"]:
        # update deploy branches
        if "src" in os.path.dirname(os.getcwd()) or "deploy" in os.path.dirname(os.getcwd()):
            updateDeployBranches("../../src/")
        else:    
            updateDeployBranches("src/")

    for branch_name in branches:
        # checkout branches
        if flags[branch_name] == 1:
            if "src" in os.path.dirname(os.getcwd()) or "deploy" in os.path.dirname(os.getcwd()):
                cmd = "cd ..; cd ..; git worktree add src/{}".format(branch_name)
                os.system(cmd)
                # create local deploy branch
                createDeployBranch(branch_name, "../../src/")
                
            else:    
                cmd = "git worktree add src/{}".format(branch_name)
                os.system(cmd)
                # create local deploy branch
                createDeployBranch(branch_name, "src/")

        # remove branches
        if flags[branch_name] == 2: 
            cmd = "git worktree remove {} ; git worktree remove {}_deploy".format(branch_name, branch_name)
            os.system(cmd)

           
def main():
    branches = open("branches", "r").read().splitlines()
    args = setupArgparse(branches)
    # arguments to dict
    flags = vars(args)
    handleFlags(flags, branches)

    
if __name__ == '__main__':
    main()
