import os
import argparse
import re
import sys
from typing import Optional

#
# Customisable
#
# Path to your password store
full_password_store = os.path.expanduser("~/.password-store")
# Path to your directory for deprecated passwords inside your password store
deprecated_dir = "z_deprecated"

#
# Do not change!
#
gpg_extension = ".gpg"
re_deprecated_extension = re.compile(r"\.old\.[0-9]+\.gpg")
re_deprecated_version_number = re.compile(r"\.old\.([0-9]+)\.gpg")


def deprecated_extension(version_number: int) -> str:
    """
    Return the extension that encodes the deprecated `version_number` of the password of some account.
    This extension is usually preceded by the account and succeeded by `.gpg`.

    :param version_number: version number of the deprecated password
    :return: extension that encodes the deprecation `version` number
    """
    return ".old.{}".format(version_number)


def get_previous_version_number(account: str) -> Optional[int]:
    """
    Return the latest deprecated version number of the `account`.

    :param account: account, as in `pass show`
    :return: latest deprecated version number of the `account`, if it exists, else `None`
    """
    account_name = os.path.basename(account)
    account_dir = os.path.dirname(account)
    full_deprecated_account_dir = os.path.join(full_password_store, deprecated_dir, account_dir)
    previous_version_number = None

    if os.path.exists(full_deprecated_account_dir):
        for f in os.scandir(full_deprecated_account_dir):
            if not f.is_file():
                continue

            f_account_name = re_deprecated_extension.sub("", f.name)

            if f_account_name == account_name:
                f_version_number = int(re_deprecated_version_number.search(f.name).group(1))
                
                if not previous_version_number or f_version_number > previous_version_number:
                    previous_version_number = f_version_number

    return previous_version_number


def deprecate_current_version(account: str, current_version_number: int):
    """
    Move the current version of the password of the `account` to the deprecated directory
    and assign the password with the `current_version_number`.

    Creates the deprecated directory and `account` directory within, if they do not already exist.

    Fails if there is no current, non-deprecated version of the password of the `account` (NOP).
    Fails if there is already a deprecated version of the password for the `account`
    with the same version number as `current_version_number` (NOP).

    :param account: account, as in `pass show`
    :param current_version_number: version number that is higher than the latest deprecated version (usually by 1)
    """
    deprecated_account = os.path.join(deprecated_dir, account + deprecated_extension(current_version_number))
    full_deprecated_account_dir = os.path.join(full_password_store, deprecated_dir, os.path.dirname(account))

    if not os.path.exists(full_deprecated_account_dir):
        os.mkdirs(full_deprecated_account_dir)

    move_password(account, deprecated_account)


def restore_previous_version(account: str, previous_version_number: int):
    """
    Move the deprecated password of the `account` with the `previous_version_number`
    back to the non-deprecated password directory and remove its version number.

    The `previous_version_number` should be the latest deprecated version number of the password of the `account`.

    Fails if there is no deprecated version of the password of the `account`
    with the same version number as `previous_version` (NOP).
    Fails if there is already a current, non-deprecated version of the password of the `account` (NOP).

    :param account: account, as in `pass show`
    :param previous_version_number: latest deprecated version number of the password of the `account`
    """
    previous_deprecated_account = os.path.join(deprecated_dir, account + deprecated_extension(previous_version_number))

    move_password(previous_deprecated_account, account)


def move_password(src_account: str, dst_account: str):
    """
    Move the password of `src_account` to the account of `dst_account`.

    Fails if there is no password of `src_account` (NOP).
    Fails if there is already a password of `dst_account` (NOP).

    :param src_account: source account, as in `pass show`
    :param dst_account: destination account, as in `pass show`
    """
    full_src_account_file = os.path.join(full_password_store, src_account + gpg_extension)
    full_dst_account_file = os.path.join(full_password_store, dst_account + gpg_extension)
    
    if not os.path.exists(full_src_account_file):
        print("Cannot move the password at {} because it does not exist!".format(src_account))
        sys.exit(1)

    if os.path.exists(full_dst_account_file):
        print("Cannot move password to {} because there already exists another password!".format(dst_account))
        sys.exit(1)

    os.rename(full_src_account_file, full_dst_account_file)
    print(dst_account)


def main():
    parser = argparse.ArgumentParser(
        description="Deprecate passwords inside the password store",
        epilog="""Deprecated passwords are moved into a separate folder.
        Each password is assigned an increasing version number for future reference.
        No password is ever deleted."""
    )
    parser.add_argument(
        "account",
        help="account in password store (as in `pass show`)"
    )
    parser.add_argument(
        "-r", "--restore", action="store_true",
        help="""restore the latest deprecated password
        (NOP if there is a current password)"""
    )

    args = parser.parse_args()

    previous_version_number = get_previous_version_number(args.account)
    
    if args.restore:
        if previous_version_number is None:
            print("Cannot restore the previous version of {} because there is none!".format(args.account))
            sys.exit(1)
        
        restore_previous_version(args.account, previous_version_number)
    else:
        if previous_version_number is None:
            current_version_number = 0
        else:
            current_version_number = previous_version_number + 1
        
        deprecate_current_version(args.account, current_version_number)


if __name__ == "__main__":
    main()
