# AliasKeepr
Store aliases in profiles so that they can be moved, and activated on demand.

## Use case
Teams that pair, and share keyboards getting frustrated when they can't `gs` (`git status`) on other team members' machines. In this case, there can be a team git repo of the `.akrc` directory, and importing their aliases is as simple as `ak yourname`.

## Usage

    usage: aliaskeepr.py [-h] [-c CONFIG] [--init-alias INIT_ALIAS] profile
    
    Import some aliases
    
    positional arguments:
      profile               Profile to output config for
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            Directory where profiles are stored
      --init-alias INIT_ALIAS
                            When using the 'init' profile, the alias name to
                            insert

## Simple setup
In your `~/.bashrc`, or `~/.zshrc`, etc add: `[ -e aliaskeepr.py ] && eval "$(aliaskeepr.py init)"`.

This will add the `ak` alias that will automatically eval, and import profiles. To use, you can simple say `ak someprofile`, and the profile aliases will be imported.

## Example profile

    [aliases]
    ll = ls -la
    fpy = find "$@" -iname '*.py'
    
If this is stored in `~/.akrc/example.ini`, and the `ak` alias is setup, typing `ak example` will give you:

- **`ll`** that executes `ls -la`
- **`ll -h`** that executes `ls -la -h`
- **`fpy ~`** that executes `find ~ -iname '*.py'`
