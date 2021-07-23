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

## Customisation

At the moment, you have to change two lines of the actual script in order to customise.  There is no separate configuration :(

- [`full_password_store`](https://github.com/chlewe/deprecate-password/blob/6e443342216345756a83acef15b923b06ad0b099/deprecate_password.py#L11) stores the full path to your password store
- [`deprecated_dir`](https://github.com/chlewe/deprecate-password/blob/6e443342216345756a83acef15b923b06ad0b099/deprecate_password.py#L13): stores the path to your directory for deprecated passwords inside your password store
