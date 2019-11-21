#!/usr/bin/python
# -*- coding: utf-8 -*-

from fla.ndfa.instance import Instance

import copy
import logging

class NonDeterministicFiniteAutomaton:
    def __init__(self, states, initial_states, acceptance_states, transitions):
        self.states = states
        self.initial_states = initial_states
        self.acceptance_states = acceptance_states
        self.transitions = transitions
        self.current_configurations = [] 
        self.closure = {}
        for state in self.states:
            self.get_closure(state)

    def restart(self):
        self.current_configuration = []
        
    def get_closure(self, state):
        if state not in self.closure:
            changes = 0
            new_closure = set()
            new_closure.add(state)
            changes += 1
            while changes > 0:
                changes = 0
                closure_update = set()
                for closure_state in new_closure:
                    for transition in self.transitions:
                        if transition.match_state(closure_state) and transition.is_empty_transition() and transition.new_state not in new_closure:
                            closure_update.add(transition.new_state)
                            changes += 1
                new_closure.update(closure_update)
            self.closure[state] = new_closure
        logging.debug("Closure for state " + state + ": " + str(self.closure[state]))
        return self.closure[state]
    
    def verify_status(self, configuration):
        if len(configuration.current_word) == 0:
            if configuration.current_state in self.acceptance_states:
                configuration.acceptance_status = True
            else:
                configuration.acceptance_status = False
    
    def get_decision(self):
        for configuration in self.current_configurations:
            if len(configuration.current_word) == 0:
                closure = self.get_closure(configuration.current_state)
                if len(closure.intersection(self.acceptance_states)) > 0:
                    return True
        return False

    def get_initial_configurations(self, word):
        configurations = []
        for state in self.initial_states:
            for closure_state in self.get_closure(state):
                configuration = Instance(self, closure_state, word)
                configurations.append(configuration)
        return configurations

    def get_configurations_for_closure(self, configuration):
        configurations = []
        for state in self.get_closure(configuration.current_state):
            configuration = Instance(self, state, configuration.current_word)
            configurations.append(configuration)
        return configurations

    def load_configurations(self, configurations):
        self.current_configurations = configurations
        for configuration in configurations:
            logging.debug("__initial__ -> " + str(configuration))

    def step_forward(self):
        configurations_current_step = copy.copy(self.current_configurations)
        self.current_configurations = []
        for configuration in configurations_current_step:
            for transition in configuration.get_valid_transitions():
                if transition.is_empty_transition():
                    logging.debug("Ignoring transition because of closure: " + str(transition))
                else:
                    new_configuration = configuration.apply_transition(transition)
                    if new_configuration is not None:
                        self.current_configurations.append(new_configuration)
                        logging.debug(str(configuration) + " -> " + str(new_configuration))
                        closure_configurations = self.get_configurations_for_closure(new_configuration)
                        if len(closure_configurations) > 0:
                            # self.current_configurations.extend(closure_configurations)
                            for closure_configuration in closure_configurations:
                                self.current_configurations.append(closure_configuration)
                                logging.debug(str(configuration) + " -> " + str(new_configuration))


    def run(self):
        pertinence_decision = self.get_decision()
        if pertinence_decision == True:
            return True
        halted_configurations = []
        while self.current_configurations:
            self.step_forward()
            for configuration in self.current_configurations:
                self.verify_status(configuration)
                if configuration.acceptance_status != None:
                    halted_configurations.append(configuration)
            if len(halted_configurations) > 0:
                if self.get_decision():
                    break
        self.current_configurations = halted_configurations
        return self.get_decision()
        
