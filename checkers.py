'''
Created on Nov 26, 2017

@author: akaiser
'''

import argparse
import random
import subprocess


class CheckerClass:
    '''
    Interface to implement for a checker
    '''

    def run_check(self):
        '''
        Method to implement for a check, should return a tuple of (boolean, string)
        '''
        pass

    def get_name(self):
        pass


class RandomChecker(CheckerClass):
    '''
    Checker that fails FAILURE_RATE percent of the time
    '''
    FAILURE_RATE = 50

    def run_check(self):
        random_var = random.random()
        if (random_var < (RandomChecker.FAILURE_RATE / 100.0)):
            return (False, "Random var was: {}".format(random_var))
        else:
            return (True, "")

    def get_name(self):
        return "Random check"


class TooManyProcessesChecker(CheckerClass):
    '''
    Checker that checks if there are too many Xvfb processes
    '''
    # This should fail if there are greater than 5 Xvfb processes (6 is
    # because there is one for the grep process)
    MAX_NUMBER_OF_PROCS = 6

    def run_check(self):
        number_of_procs = subprocess.check_output(
            "ps aux | grep Xvfb | wc -l", shell=True)
        number_of_procs = int(number_of_procs)
        if (number_of_procs > TooManyProcessesChecker.MAX_NUMBER_OF_PROCS):
            full_out = subprocess.check_output(
                "ps aux | grep Xvfb", shell=True, universal_newlines=True)
            return (False, full_out)
        else:
            return (True, "")

    def get_name(self):
        return "TooManyProcessesChecker check"


class UpdateStateMemoryChecker(CheckerClass):
    '''
    Checks if the update_state process is taking up too much memory.
    '''
    MAX_MEMORY_PERCENT = 75

    def run_check(self):
        memory_percent = subprocess.check_output(
            ("ps aux | "
             "grep update_state | "
             "grep -v grep | "
             "grep Sl | "
             "tr -s \" \" | "
             "cut -f4 -d\" \""),
            shell=True)
        memory_percent = float(memory_percent.strip())
        if (memory_percent > UpdateStateMemoryChecker.MAX_MEMORY_PERCENT):
            return (False, "Memory currently at: {}".format(memory_percent))
        else:
            return (True, "")

    def get_name(self):
        return "Update state memory check"


if __name__ == "__main__":
    # Run a check once
    possible_checkers = {'random': RandomChecker(),
                         'too_many_procs': TooManyProcessesChecker(),
                         'memory': UpdateStateMemoryChecker()}
    parser = argparse.ArgumentParser(description='Run a single check.')
    parser.add_argument('--checker_name', choices=possible_checkers.keys())
    args = parser.parse_args()

    if args.checker_name:
        checker = possible_checkers[args.checker_name]
        result = checker.run_check()
        print(result)
    else:
        print("You must select a checker_name")
