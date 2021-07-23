# deprecate-password

Deprecate passwords that are stored in [pass](https://www.passwordstore.org/) without deleting any files.
The old passwords are moved into a seperate folder (default: `z_deprecated`) and are assigned an incremental version number for later reference.

## Usage
```
python deprecate-password.py account
```
where `account` is the same identifier as in `pass show`.

The latest deprecated version of the password of an account can be restored by using the `--restore` flag.  In case of any file conflicts, the program exists and no files are overwritten.  For more information, try the `--help` flag.

## Requirements

- Python 3.8
