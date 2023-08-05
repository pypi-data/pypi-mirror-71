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
The easiest way to install cloudonecli is to use pip in a `pip`  in a ``virtualenv``:

    $ pip3 install cloudonecli

or, if you are not installing in a ``virtualenv``, to install globally::

    $ sudo pip3 install cloudonecli

or for your user:

    $ pip3 install --user cloudonecli

If you have the cloudonecli installed and want to upgrade to the latest version
you can run::

    $ pip3 install --upgrade cloudonecli
    
## Command Completion -- HIGHLY recommended

The cloudonecli package includes a very useful command completion feature.
This feature is not automatically installed so you need to configure it manually.
To enable tab completion for bash either use the built-in command ``complete``::

    $ complete -C cloudonecli_completer cloudonecli

Or add ``bin/cloudonecli_bash_completer`` file under ``/etc/bash_completion.d``,
``/usr/local/etc/bash_completion.d`` or any other ``bash_completion.d`` location.

## Getting Started
Before using cloudonecli, you need to provide credentials and hostnames of your services.
You do this by creating a config file. The file should be placed in `~/.cloudone/credentials`

    [default]
    DSMapikey = F16564D5-492A-F167-5472-2CEDA60E12D7:GDwCvBV2kV7FjSVuYJXdEqeeeu0WKlls3/sqwu+HEXM=
    SCUser: administrator
    SCPassword: MySuperPassword   
    
This creates a ``default`` profile that has both Deep Security and Smart Check credentials. You can add additional 
profiles for more servers. 

 Next, we need a config file to tell the cloudonecli, when using profile `default` what settings we want to use. 
 The file should nbe placed in `~/.cloudone/config`    
 
    [default]
    DSMhost = https://emydsm.example.com:443/api
    DSMverifyssl = False
    SCHost = https://mySmartCheck.example.com:443/api
    SCverifyssl = False

**Note** The `/api` at the end of the URL is required. 

Now when `default` profile is used for Smart Check, it will connect to `https://mySmartCheck.example.com:443/api` using the username`administrator` and password `MySuperPassword`


## Examples 

Get a list of computers from Deep Security: 

    cloudone deepsecurity computers listcomputers

Get a list of polices from Deep Security: 

    cloudone deepsecurity policies listPolicies
    
Get a list of scans from Smart Check 

    cloudone smartcheck  scans listScans
 
 
 ## Getting Help
 Use github issues for logging buggs and feature requests. 
 
 
 