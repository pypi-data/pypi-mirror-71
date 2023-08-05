#!/usr/bin/env python
#
# gitcommit: a tool for writing conventional commits, conveniently
# Author: Ben Greenberg
# Created: 20th September 2019
#
# Implements Conventional Commit v1.0.0-beta.4
#
# TEMPLATE:
#
# <type>[(optional scope)]: <description>
#
# [BREAKING CHANGE: ][optional body / required if breaking change]
#
# [optional footer]
#
# ADDITIONAL RULES:
# - Subject line (i.e. top) should be no more than 50 characters.
# - Every other line should be no more than 72 characters.
# - Wrapping is allowed in the body and footer, NOT in the subject.
#

from __future__ import print_function
import os
import sys
import subprocess
import textwrap
from prompt_toolkit import PromptSession, prompt, ANSI
from prompt_toolkit.history import FileHistory
from prompt_toolkit.application.current import get_app
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings
from gitcommit.style import Ansi
from gitcommit.validators import (
    DescriptionValidator,
    TypeValidator,
    YesNoValidator,
    BodyValidator,
    FooterValidator,
)
from gitcommit.completers import TypeCompleter, FooterCompleter
from gitcommit.updater import check_for_update
from gitcommit.utils import capitaliseFirst
from gitcommit.style import style

home = os.path.expanduser("~")
CONFIG_HOME_DIR = os.path.join(home, ".gitcommit/")

IS_BREAKING_CHANGE = None  # default for global variable
try:
    WINDOW_WIDTH, _ = os.get_terminal_size()
except:
    WINDOW_WIDTH = 80  # default


bindings = KeyBindings()


@bindings.add("s-down")
def emulate_submit(event):
    "Emulate the enter key for text submission with Shift+Down"
    get_app().current_buffer.validate_and_handle()


class LineLengthPrompt:
    def __init__(self, length_limit, session):
        self.limit = length_limit
        self.session = session
        self.invalid_style = Style.from_dict({"rprompt": "bg:#ff0066 #000000"})
        self.valid_style = Style.from_dict({"rprompt": "bg:#b0f566 #000000"})

    def get_text(self):
        text = get_app().current_buffer.text
        cur_len = len(text)

        if cur_len > self.limit:
            self.session.style = self.invalid_style
            return f" {cur_len}/{self.limit} chars "

        else:
            self.session.style = self.valid_style
            return f" {cur_len}/{self.limit} chars "


def wrap_width(string):
    def format_string(string):
        string_lines = string.split("\n")
        string_lines_wrapped = []
        for line in string_lines:
            string_lines_wrapped += textwrap.wrap(
                line,
                width=WINDOW_WIDTH,
                break_long_words=False,
                replace_whitespace=False,
            )
        return "\n".join(string_lines_wrapped)

    if type(string) is list:
        return "\n".join([format_string(s) for s in string])
    elif type(string) is str:
        return format_string(string)
    else:
        raise TypeError("Unable to parse string argument")


def add_type(commit_msg):
    valid_types = {
        "feat": "MUST be used the commit adds/builds toward a new feature",
        "fix": "MUST be used when a commit represents a bug fix",
        "chore": "Any change to build system, dependencies, config files, scripts (no production code)",
        "docs": "Changes to documentation",
        "perf": "Changes that improves performance",
        "refactor": "Refactoring production code, e.g. renaming a variable/restructuring existing logic",
        "revert": "Any commit that explicitly reverts part/all changes introduced in a previous commit",
        "style": "Changes to white-space, formatting, missing semi-colons, etc.",
        "test": "Changes to tests e.g. adding a new/missing test or fixing/correcting existing tests",
        "wip": "Any code changes that are work in progress; they may not build (use these sparingly!)",
    }

    Ansi.print_info(
        wrap_width(
            [
                "Please specify the type of this commit using one of the available keywords. Accepted types: ",
                "TAB to autocomplete...",
            ]
        )
    )

    type_names = sorted(valid_types.keys())
    # create prefixes e.g. "    0  chore"
    prefixes = ["  " + str(i) + "  " + t for i, t in enumerate(type_names)]
    prefix_length = max([len(p) for p in prefixes]) + 2

    for i in range(len(type_names)):
        # type descriptions
        type_descr_width = WINDOW_WIDTH - prefix_length
        descr_lines = textwrap.wrap(
            valid_types[type_names[i]],
            width=type_descr_width,
            subsequent_indent=" " * prefix_length,
            break_long_words=False,
        )
        # ensure each line has trailing whitespace, then do join
        type_descr_str = "".join(map(lambda l: l.ljust(type_descr_width), descr_lines))

        # Combine type name with type description
        type_print = prefixes[i].ljust(prefix_length) + type_descr_str

        # Print the type
        Ansi.print_warning(type_print)

    valid_numeric_types = [str(n) for n in range(len(type_names))]
    valid_inputs = list(valid_types.keys()) + valid_numeric_types

    print()
    text = Ansi.b_green("Type: ")
    history_file_path = os.path.join(CONFIG_HOME_DIR, "type_history")
    c_type = prompt(
        ANSI(text),
        completer=TypeCompleter(),
        validator=TypeValidator(valid_inputs),
        history=FileHistory(history_file_path),
        key_bindings=bindings,
    )

    # Convert from number back to proper type name
    if c_type in valid_numeric_types:
        c_type = type_names[int(c_type)]

    commit_msg += c_type
    return commit_msg


def add_scope(commit_msg):
    Ansi.print_info(
        wrap_width(
            "\nWhat is the scope / a noun describing section of repo? (try to keep under 15 characters)"
        )
    )
    text = Ansi.colour(Ansi.fg.bright_green, "Scope (optional): ")
    history_file_path = os.path.join(CONFIG_HOME_DIR, "scope_history")
    c_scope = prompt(
        ANSI(text), history=FileHistory(history_file_path), key_bindings=bindings
    ).strip()

    if c_scope != "":
        commit_msg += "({})".format(c_scope)

    return commit_msg


def check_if_breaking_change():
    global IS_BREAKING_CHANGE  # required to be able to write to variable
    contains_break = ""
    print()  # breakline from previous section
    while True:
        text = Ansi.b_yellow("Does commit contain breaking change? (no) ")
        contains_break = (
            prompt(
                ANSI(text),
                validator=YesNoValidator(answer_required=False),
                key_bindings=bindings,
            )
            .lower()
            .strip()
        )
        if contains_break == "":  # default
            IS_BREAKING_CHANGE = False
            break
        elif contains_break in ["y", "yes"]:
            IS_BREAKING_CHANGE = True
            return True
        else:
            IS_BREAKING_CHANGE = False
            return False


def add_description(commit_msg):
    if IS_BREAKING_CHANGE is None:
        raise ValueError("Global variable `IS_BREAKING_CHANGE` has not been set.")

    if IS_BREAKING_CHANGE:
        commit_msg += "!: "
    else:
        commit_msg += ": "

    num_chars_remaining = 50 - len(commit_msg)
    Ansi.print_info(
        wrap_width(
            "\nWhat is the commit description / title. A short summary of the code changes. Use the imperative mood. No more than {} characters.".format(
                num_chars_remaining
            )
        )
    )

    c_descr = ""

    history_file_path = os.path.join(CONFIG_HOME_DIR, "description_history")
    session = PromptSession(
        history=FileHistory(history_file_path), key_bindings=bindings
    )

    length_prompt = LineLengthPrompt(num_chars_remaining, session)
    while c_descr == "":
        text = Ansi.b_green("Description: ")
        c_descr = session.prompt(
            ANSI(text),
            validator=DescriptionValidator(num_chars_remaining),
            rprompt=length_prompt.get_text,
        )

    # Sanitise
    c_descr = c_descr.strip()  # remove whitespace
    c_descr = capitaliseFirst(c_descr)  # capital first letter
    if c_descr[-1] == ".":
        c_descr = c_descr[:-1]  # remove period if last character
        c_descr = c_descr.strip()  # remove further whitespace

    commit_msg += c_descr
    return commit_msg


def custom_prompt_continuation(width, line_number, is_soft_wrap):
    text_continuation = " " * (width - 2) + "┃ "
    return ANSI(Ansi.colour(Ansi.fg.bright_green, text_continuation))


def add_body(commit_msg):
    if IS_BREAKING_CHANGE is None:
        raise ValueError("Global variable `IS_BREAKING_CHANGE` has not been set.")

    history_file_path = os.path.join(CONFIG_HOME_DIR, "body_history")
    session = PromptSession(
        prompt_continuation=custom_prompt_continuation,
        history=FileHistory(history_file_path),
        key_bindings=bindings,
    )
    body_validator = BodyValidator(session, IS_BREAKING_CHANGE)

    if IS_BREAKING_CHANGE:
        Ansi.print_info(
            wrap_width(
                [
                    "\nExplain what has changed in this commit to cause breaking changes.",
                    "Press Esc before Enter to submit.",
                ]
            )
        )
        # text = Ansi.b_green("Body (required) ┃ ")
        text = Ansi.colour(Ansi.fg.bright_green, Ansi.bold, "Body ┃ ")
    else:
        Ansi.print_info(
            wrap_width(
                [
                    "\nProvide additional contextual information about the changes here.",
                    "Press Esc before Enter to submit.",
                ]
            )
        )
        text = Ansi.colour(Ansi.fg.bright_green, "Body (optional) ┃ ")

    c_body = session.prompt(ANSI(text), validator=body_validator)
    c_body = c_body.strip()  # remove leading/trailing whitespace
    c_body = capitaliseFirst(c_body)  # capital first letter

    if c_body != "":
        if IS_BREAKING_CHANGE:
            c_body = "BREAKING CHANGE: " + c_body

        b_lines = c_body.split("\n")
        num_blank_lines = 0  # track the number of consecutive blank lines

        condensed_b_lines = []
        for line in b_lines:
            l_stripped = line.strip()
            if l_stripped == "":
                num_blank_lines += 1
            else:
                num_blank_lines = 0

            if num_blank_lines > 1:
                continue  # ignore any blank lines after the first
            elif l_stripped == "":
                # skip any processing and add to output if blank
                condensed_b_lines.append(l_stripped)
            else:
                # check if we are dealing with a bulleted line
                bulleted_line = False
                if l_stripped[0] in ["*", "-"]:
                    bulleted_line = True
                    line_after_bullet = l_stripped[1:].strip()
                    l_stripped = " " + l_stripped[0] + " " + line_after_bullet

                # format each line with forced line breaks to maintain maximum line length
                wrapped_line = "\n".join(
                    textwrap.wrap(
                        l_stripped,
                        width=72,
                        break_long_words=False,
                        break_on_hyphens=False,
                        subsequent_indent="   " if bulleted_line else "",
                    )
                )
                condensed_b_lines.append(wrapped_line)

        # recombine all user defined lines
        full_body = "\n".join(condensed_b_lines)

        # append to commit message
        commit_msg += "\n\n" + full_body

    return commit_msg


def add_footer(commit_msg):
    Ansi.print_info(
        wrap_width(
            [
                "\nThe footer MUST contain meta-information about the commit:",
                " - Related pull-requests, reviewers, breaking changes",
                " - GitHub close/fix/resolve #issue or username/repository#issue",
                " - One piece of meta-information per-line",
                " - To submit, press the Esc key before Enter",
            ]
        )
    )

    text = Ansi.colour(Ansi.fg.bright_green, "Footer (optional) ┃ ")
    history_file_path = os.path.join(CONFIG_HOME_DIR, "footer_history")
    session = PromptSession(
        completer=FooterCompleter(),
        multiline=False,
        prompt_continuation=custom_prompt_continuation,
        history=FileHistory(history_file_path),
        key_bindings=bindings,
    )
    c_footer = session.prompt(ANSI(text), validator=FooterValidator(session)).strip()

    if c_footer != "":
        f_lines = c_footer.split("\n")
        f_lines = [
            l for l in f_lines if l.strip() != ""
        ]  # remove any lines that are empty: ""

        for i, line in enumerate(f_lines):
            line = line.strip()  # clean up extraneous whitespace

            # format each line with forced line breaks to maintain maximum line length
            f_lines[i] = "\n".join(
                textwrap.wrap(
                    line,
                    width=72,
                    break_long_words=False,
                    break_on_hyphens=False,
                    subsequent_indent="  ",
                )
            )

        # recombine all user defined footer lines
        formatted_footer = "\n".join(f_lines)
        commit_msg += "\n\n" + formatted_footer

    return commit_msg


def run(args):
    # print(sys.version + "/n")

    if len(args) > 0 and args[0] in ["version", "update"]:
        check_for_update(verbose=True)
        return  # Exit early

    # Ensure the config directory exists
    os.makedirs(CONFIG_HOME_DIR, exist_ok=True)

    commits_file_path = os.path.join(CONFIG_HOME_DIR, "commit_msg_history")
    commit_msg_history = FileHistory(commits_file_path)

    if WINDOW_WIDTH < 80:
        Ansi.print_error(
            f"It is recommended you increase your window width ({WINDOW_WIDTH}) to at least 80."
        )

    commit_msg = ""
    if len(args) > 0 and args[0] == "retry":
        args = args[1:]  # consume the "retry" first arg
        cm_histories_iter = commit_msg_history.load_history_strings()
        last_commit_msg = next(cm_histories_iter, "")
        if last_commit_msg == "":
            Ansi.print_error("Could not find a previous commit message")
        commit_msg = last_commit_msg

    if commit_msg == "":
        print("Starting a conventional git commit...")
        print(
            Ansi.colour(
                Ansi.fg.bright_red, "Tip: Press the up arrow key to recall history!"
            )
        )
        commit_msg = add_type(commit_msg)
        commit_msg = add_scope(commit_msg)
        check_if_breaking_change()
        commit_msg = add_description(commit_msg)
        commit_msg = add_body(commit_msg)
        commit_msg = add_footer(commit_msg)
        print()

    Ansi.print_ok("This is your commit message:")
    print()
    print(commit_msg)
    print()

    # print("\nNOTE: This was a dry run and no commit was made.\n")

    # It is expected that all remaining args at this point are for the git
    # commit command
    args_string = " ".join(args)
    text = Ansi.colour(Ansi.fg.bright_yellow, "Extra args for git commit: ")
    extra_args_file_path = os.path.join(CONFIG_HOME_DIR, "extra_args_history")
    extra_args_str = prompt(
        ANSI(text),
        default=args_string,
        history=FileHistory(extra_args_file_path),
        key_bindings=bindings,
    )
    if extra_args_str != "":
        argv_passthrough = extra_args_str.split(" ")
    else:
        argv_passthrough = []

    # Ask for confirmation to commit
    confirmation_validator = YesNoValidator(answer_required=True)
    text = Ansi.b_yellow("Do you want to make your commit? [y/n] ")
    confirm = prompt(
        ANSI(text), validator=confirmation_validator, key_bindings=bindings
    ).lower()

    if confirm in confirmation_validator.confirmations:
        commit_msg_history.store_string(commit_msg)
        cmds = ["git", "commit", "-m", commit_msg] + argv_passthrough
        returncode = subprocess.run(cmds).returncode
        print()
        if returncode == 0:
            Ansi.print_ok("\nCommit has been made to conventional commits standards!")
        else:
            Ansi.print_error("\nThere was an error whilst attempting the commit!")

    elif confirm in confirmation_validator.rejections:
        print("Aborting the commit...")

    check_for_update()


def main():
    try:
        # print(sys.argv)
        run(sys.argv[1:])
    except KeyboardInterrupt:
        print("\nAborted.")
