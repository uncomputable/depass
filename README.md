# Depass: Password Deprecator

An automatic workflow to (un)deprecate passwords inside the [password store](https://www.passwordstore.org).

```
depass [--restore] account
```

## Build the script using nix

Clone the repo.

```bash
git@github.com:uncomputable/depass.git
cd depass
```

Build the default package.

```bash
nix-build
```

## Install the script using nix

Install the built derivation in your nix profile.

```bash
nix profile install ./result
```

## Build the script without nix

IDK, use setuptools or something 😝
