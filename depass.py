import os
import argparse
import re
import shutil
from typing import Optional

def version_from_deprecated_file(file_name: str) -> Optional[int]:
    match = re.search(r"\.old\.([0-9]+)\.gpg", file_name)
    if match:
        return int(match.group(1))
    else:
        return None


def latest_deprecated_version(account: str, store_path: str, deprecated_dir: str) -> Optional[int]:
    account_name = os.path.basename(account)
    account_dir = os.path.dirname(account)
    deprecated_account_dir = os.path.join(store_path, deprecated_dir, account_dir)
    latest_version = None

    if os.path.exists(deprecated_account_dir):
        for file_name in os.listdir(deprecated_account_dir):
            file_path = os.path.join(deprecated_account_dir, file_name)
            file_account_name = re.sub(r"\.old\.[0-9]+\.gpg", "", file_name)

            if not os.path.isfile(file_path) or file_account_name != account_name:
                continue

            version = version_from_deprecated_file(file_name)

            if version is not None and (latest_version is None or latest_version < version):
                latest_version = version

    return latest_version


def deprecate(account: str, store_path: str, deprecated_dir: str, version: int):
    account_dir = os.path.dirname(account)
    deprecated_account_dir = os.path.join(store_path, deprecated_dir, account_dir)

    if not os.path.exists(deprecated_account_dir):
        os.makedirs(deprecated_account_dir)

    deprecated_account = os.path.join(deprecated_dir, f"{account}.old.{version}")
    move(account, deprecated_account, store_path)


def restore(account: str, store_path: str, deprecated_dir: str, version: int):
    deprecated_account = os.path.join(deprecated_dir, f"{account}.old.{version}")
    move(deprecated_account, account, store_path)


def move(src_account: str, tgt_account, store_path: str):
    src_path = os.path.join(store_path, f"{src_account}.gpg")
    dst_path = os.path.join(store_path, f"{tgt_account}.gpg")

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source account {src_account} does not exist")

    if os.path.exists(dst_path):
        raise FileExistsError(f"Target account {tgt_account} is already occupied")

    shutil.move(src_path, dst_path)
    print(f"{src_account} -> {tgt_account}")


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
        help="""Restore the latest deprecated password
        (NOP if there is a current password)"""
    )
    parser.add_argument(
        "-p", "--path",
        default=os.path.join(os.path.expanduser("~"), ".password-store"),
        help="Path to password store")
    parser.add_argument(
        "-d", "--dir",
        default="z_deprecated",
        help="Directory for deprecated passwords inside password store"
    )

    args = parser.parse_args()

    latest_version = latest_deprecated_version(args.account, args.path, args.dir)

    try:
        if args.restore:
            if latest_version is None:
                print(f"No deprecated passwords were found for {args.account}")
            else:
                restore(args.account, args.path, args.dir, latest_version)
        else:
            next_version = 0 if latest_version is None else latest_version + 1
            deprecate(args.account, args.path, args.dir, next_version)
    except (FileNotFoundError, FileExistsError) as error:
        print(str(error))


if __name__ == "__main__":
    main()
