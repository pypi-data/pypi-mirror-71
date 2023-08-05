#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

import sys
import signal
import json
import DeepSecurity
import SmartCheck
import argparse
from inspect import getmembers, isfunction, signature

import logging

from .session import Session
LOG = logging.getLogger('thus.clidriver')
LOG_FORMAT = (
    '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')

# Don't remove this line.  The idna encoding
# is used by getaddrinfo when dealing with unicode hostnames,
# and in some cases, there appears to be a race condition
# where threads will get a LookupError on getaddrinfo() saying
# that the encoding doesn't exist.  Using the idna encoding before
# running any CLI code (and any threads it may create) ensures that
# the encodings.idna is imported and registered in the codecs registry,
# which will stop the LookupErrors from happening.
# See: https://bugs.python.org/issue29288
u''.encode('idna')

def _set_user_agent_for_session(session):
    session.user_agent_name = 'thus-cli'
 #   session.user_agent_version = __init__.__version__


def main():
    driver = create_clidriver()
    rc = driver.main()
    return rc

def create_clidriver():
    session =  Session()
    _set_user_agent_for_session(session)
    #load_plugins(session.full_config.get('plugins', {}),
    #             event_hooks=session.get_component('event_emitter'))
    driver = CLIDriver(session=session)
    return driver

def setCLIParse():
    parser = argparse.ArgumentParser(description='THUS CLI')
    return parser


class CLIDriver(object):

    def __init__(self, session=None):
        #self._functions_list = [o for o in getmembers(deepsecurity) if isfunction(o[1])]
        self._functions = dir(DeepSecurity)
        if session is None:
            self.session = Session()
        else:
            self.session = session
        self._cli_data = None
        self._command_table = None
        self._argument_table = None
        self._parser = argparse.ArgumentParser(description='THUS CLI')
        self._profile = "default"
       # self.alias_loader = AliasLoader()

    def parseCliFlag(self, arg):
        split = arg.split("=")
        if(split[0] == "--profile"):
            self._profile = split[1]

    def parseCommand(self):
        if len(sys.argv) < 2:
            print("Usage: <service> <module> <command> (sub command arguments)")
            return
        j = 1
        if sys.argv[1].startswith("--"):
            self.parseCliFlag(arg=sys.argv[1])
            j = j + 1

        self._command = sys.argv[j+1]
        for c in self._functions:
            if c.lower() == self._command.lower():
                self._command = c
                break

        self._service = sys.argv[j]
        self._subcommand = sys.argv[j+2]
        self._arguments = {}
        i = j+3
        while sys.argv[i:]:
            split=sys.argv[i].split("=")
            self._arguments[split[0]]=split[1]
            i=i+1


    def FindClass(self, module):
        listing = dir (module)
        for c in listing:
            if c.lower() == self._command.lower():
                self._command = c
                break
        classToCall = getattr(module, self._command)
        return classToCall
    def FindFunction(self, rtv):
        listing = dir(rtv)
        for f in listing:
            if f.lower() == self._subcommand.lower():
                self._subcommand = f
                break
        method_to_call = getattr(rtv, self._subcommand)
        argments = signature(method_to_call).parameters
        return method_to_call

    def ExecuteCommand(self):
        service = self._service.lower()
        if service == 'workloadsecurity' or service == 'ws':
            #Place holder until WS diverges from DS
            service = 'deepsecurity'
        if service == 'containersecurity' or service == 'cs':
            # Place holder until sc diverges rom cs
            service = 'smartcheck'
        if service == 'deepsecurity' or service=='ds':
            config = self.session.BuildDSMConfig(profile=self._profile)
            connection = DeepSecurity.connect.Connection(config=config)
            group_to_call = self.FindClass(module=DeepSecurity) #getattr(DeepSecurity, self._command)
            rtv = group_to_call(config=config, connection=connection)
            method_to_call = self.FindFunction(rtv=rtv)
            rtv = method_to_call(**self._arguments)
        if service == 'smartcheck' or service == 'sc':
            config = self.session.BuildSCConfig(profile=self._profile)
            connection = SmartCheck.connect.Connection(config=config)
            group_to_call = self.FindClass(module=SmartCheck) # getattr(SmartCheck, self._command)
            rtv = group_to_call(config=config, connection=connection)
            method_to_call = self.FindFunction(rtv=rtv)
            rtv = method_to_call(*self._arguments)
        return rtv

    def printResults(self, results):
        try:
            print(json.dumps(results))
        except:
            print(results)

    def main(self):
        self.parseCommand()
        results = self.ExecuteCommand()
        self.printResults(results)