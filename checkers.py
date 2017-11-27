'''
Created on Nov 26, 2017

@author: akaiser
'''


import random


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


FAILURE_RATE = 50


class RandomChecker(CheckerClass):
    '''
    Checker that fails FAILURE_RATE percent of the time
    '''

    def run_check(self):
        random_var = random.random()
        if (random_var < (FAILURE_RATE / 100.0)):
            return (False, "Random var was: {}".format(random_var))
        else:
            return (True, "")

    def get_name(self):
        return "Random check"
