#!/usr/bin/env python
# coding: utf-8
#
# This file is part of `boringit`.
# Copyright (c) 2020 Marcus Mello
# Distributed under a BSD-like license. For full terms see the file LICENSE.txt
#

"""
boringit

"""

import os
import sys
import subprocess
import yaml
import time


def _print(procedure):
    print("""File....: '{}'""".format(procedure[0]))
    print("""Action..: {}""".format(procedure[1]))
    print("""Commit..: {} """.format(procedure[2]))


def make_procedure_list_from(git_status):
    procedure_list = []
    for line in git_status:
        if "modified" in line:
            file_name = line.split()[1]
            action = "git add"
            input_msg = (
                """Blank to not commit. Default action : 'git add'
Write your commit message for the file: '{}'    
Commit message: """
            ).format(file_name)
            commit = (""" "{}" """).format(input(input_msg))
            if commit != ' "" ':
                procedure_list.append((file_name, action, commit))
            print(" ")

        if "deleted" in line:
            file_name = line.split()[1]
            action = "git rm"
            input_msg = (
                """Blank to not commit. Default action : 'git rm'
Write your commit message for the file: '{}'    
Commit message: """
            ).format(file_name)
            commit = (""" "{}" """).format(input(input_msg))
            if commit != ' "" ':
                procedure_list.append((file_name, action, commit))
            print(" ")
        if "Untracked files" in line:
            raw_untracked = str(git_status).split(sep="Untracked files")[1][76:-77]
            untracked_files_list = [
                untracked_file[3:-4] for untracked_file in raw_untracked.split()
            ]
            for untracked_file in untracked_files_list:
                if len(untracked_file) != 0:
                    file_name = untracked_file
                    action = "git add"
                    input_msg = (
                        """Blank to not commit. Default action : 'git add'
Write your commit message for the file: '{}'    
Commit message: """
                    ).format(file_name)
                    commit = (""" "{}" """).format(input(input_msg))
                    if commit != ' "" ':
                        procedure_list.append((file_name, action, commit))
                    print(" ")
    return procedure_list


def user_agreed_with_the(procedure_list):
    print("Commit inventory:")
    print("====================================================")
    print(" ")
    for procedure in procedure_list[:-1]:
        _print(procedure)
        print("----------------------------------------------------")
    _print(procedure_list[-1])
    print("====================================================")
    print(" ")
    accept = input("Proceed commits and pushes? ") or "y"
    print(" ")
    return bool(accept == "y")


def process_these(procedures, to_remotes, from_branch):

    print("====================================================")
    for procedure in procedures:

        file_name = procedure[0]
        action = procedure[1]
        commit = procedure[2]

        print("Processing file: ", file_name)
        print("====================================================")
        print(" ")

        # Add
        add_or_rm_command = action + " " + file_name
        print(add_or_rm_command)
        git_stdout = os.popen(add_or_rm_command).read()

        # Commit
        commit_command = "git commit -m " + commit
        print(commit_command)
        git_stdout = os.popen(commit_command).read()

        print(" ")
        print(git_stdout)

        # Push
        for remote in to_remotes.values():
            print("----------------------------------------------------")
            print("git pushing from {} to {}".format(from_branch, remote["name"]))
            git_stdout = subprocess.run(
                ["git", "push", "-u", remote["name"], from_branch, "--progress"],
                capture_output=True,
            ).stderr.decode("utf8")

            print(" ")
            print(git_stdout)
        print("====================================================")
        print(" ")


def load_remotes():

    remotes = {}

    try:
        with open("remotes.yml", "r") as file:
            remotes = yaml.load(file.read(), Loader=yaml.FullLoader)
    except:
        print(
            "remotes.yml didn't found. Please, follow the documentation and create one."
        )
        # remotes = get_remotes_from_user()

    return remotes


class BorinGit:
    def __init__(self):

        self.remotes = load_remotes()
        if not os.path.isdir(".git"):
            os.popen("git init")
            time.sleep(1)
        self.work_branch = os.popen("git status").readlines()[0][10:-1]

    def init(self):
        print("Hello, no more Boring Git times for you!")

    def add_remotes(self):
        for remote in self.remotes.values():
            command = "git remote add {} {}".format(remote["name"], remote["url"])
            print("Adding {} {}".format(remote["name"], remote["url"]))
            os.popen(command)
            time.sleep(1)

    def acp(self):
        git_status = os.popen("git status").readlines()
        if "nothing to commit" not in git_status:
            procedures = make_procedure_list_from(git_status)
            if len(procedures) != 0:
                if user_agreed_with_the(procedures):
                    process_these(
                        procedures,
                        to_remotes=self.remotes,
                        from_branch=self.work_branch,
                    )
                else:
                    print("Nothing to do.")
            else:
                print("Nothing to do.")
        else:
            print("Nothing to do.")


def main():
    try:
        getattr(BorinGit(), sys.argv[1])()
    except:
        print("{} is not a boringit valid command.".format(sys.argv[1]))


if __name__ == "__main__":
    main()
