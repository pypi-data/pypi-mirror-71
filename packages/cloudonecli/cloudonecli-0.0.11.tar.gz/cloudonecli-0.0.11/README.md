# cloudonecli

This package provides a command line tool for use with Trend Micro Cloud One suite of products, including 
- Deep Security (on premises and DSaaS)
- Smart Check 
- Cloud Conformity (coming)
- Network Security (coming)

This package currently supports Python versions: 
- 3.6.x and greater
- 3.7.x and greater 
- 3.8.x and greater

**Note:** All replys from the server are in JSON. Therefore [jq](https://stedolan.github.io/jq/) is a good companion 
program to pipe the output to.  For most distros, you can install jq with `yum install jq` or `apt-get install jq`
 
## Installation
The easiest way to install thus is to use pip in a `pip`  in a ``virtualenv``:

    $ pip3 install thus --user

or, if you are not installing in a ``virtualenv``, to install globally:

    $ sudo pip3 install thus

or for your user:

    $ pip3 install --user thus

If you have the thus installed and want to upgrade to the latest version
you can run::

    $ pip3 install --upgrade thus
    
## Command Completion -- HIGHLY recommended

 Not sure what shell you have? Run `echo $SHELL` if the result is `/bin/bash` you have bash. If it comes back `/bin/zsh` you have zsh.
 ###bash 
 To enable tab completion for bash, execute 
 
    source thus_completer_bash.sh
 
 If you used `--user` when installing thus, the standard location for `thus_completer_bash.sh` is in `~/.local/bin/thus_completer_bash.sh`
 If you did not use `--user` when installing thus, the standard location for `thus_completer_bash.sh` is in `/usr/bin/thus_comleter_bash.sh`
 To enable this everytime, add the `source` command to the full path to `thus_completer_bash.sh` to your `~/.bashrc` file.
 ### zsh
 Locate your `thus_completer_zsh.sh` file. 
 If you used `--user` then installing thus, the standard location for `thus_completer_zsh.sh` is in `~/.local/bin/thus_completer_zsh.sh`
 If you did not use `--user` when installing thus, the standard location for `thus_completer_zsh.sh` is in `/usr/bin/thus_comleter_zsh.sh`
 
 Edit the ~/.zshrc file. Add the following lines to the top of the file. It must be before any call to `autoload`
 `$fpath=$fpath:~/.local/bin/thus_completer_zsh.sh`

Restart your terminal for changes to take effect. 

## Getting Started
Before using thus, you need to provide credentials and hostnames of your services.
You do this by creating a config file. The file should be placed in `~/.thus/credentials`

    [default]
    DSMapikey = F16564D5-492A-F167-5472-2CEDA60E12D7:GDwCvBV2kV7FjSVuYJXdEqeeeu0WKlls3/sqwu+HEXM=
    SCUser: administrator
    SCPassword: MySuperPassword   
    
This creates a ``default`` profile that has both Deep Security and Smart Check credentials. You can add additional 
profiles for more servers. 

 Next, we need a config file to tell the thus, when using profile `default` what settings we want to use. 
 The file should nbe placed in `~/.thus/config`    
 
    [default]
    DSMhost = https://emydsm.example.com:443/api
    DSMverifyssl = False
    SCHost = https://mySmartCheck.example.com:443/api
    SCverifyssl = False

**Note** The `/api` at the end of the URL is required. 

Now when `default` profile is used for Smart Check, it will connect to `https://mySmartCheck.example.com:443/api` using the username`administrator` and password `MySuperPassword`


## Examples 

Get a list of computers from Deep Security: 

    thus deepsecurity computers list

Get a list of computers from Deep Security with only two expand values: 

    thus deepsecurity computers list expand=interfaces,webreputation

Get a list of polices from Deep Security: 

    thus deepsecurity policies list
    
Get a list of scans from Smart Check 

    thus smartcheck scans list
 
 
 ## Getting Help
 Use github issues for logging bugs and feature requests. 
 
