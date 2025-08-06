#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 14:58:07 2025

@author: lau
"""

#%% THE ONE CLASS TO RULE THEM ALL

class Experiment():
    
    def __init__(self):
        pass
    
    def check_user(self):
        pass
    
    def open_GUI(self):
        pass
    
    def define_io_files(self):
        pass
    
    def define_texts(self):
        pass
    
    def set_experiment_parameters(self):
        pass
    
    def create_experiment_window(self):
        pass
    
    def present_text(self):
        pass
    
    def present_instructions(self):
        pass
    
    def present_response_options(self):
        pass
    
    def wait(self):
        pass
    
    def run_practice(self):
        pass
    
    def define_staircase(self):
        pass
    
    def run_staircase(self):
        pass
    
    def counterbalance_target_trials(self):
        pass

    def get_trigger_value(self):
        pass
    
    def present_trial(self):
        pass
    
    def run_experiment(self):
        pass
    
    def present_thank_you_screen(self):
        pass


#%% RUN EXPERIMENT

## initalise
experiment = Experiment()    

## setting up experiment
experiment.check_user()
experiment.open_GUI()
experiment.define_io_files()
experiment.define_texts()
experiment.set_experiment_parameters()
experiment.create_experiment_window()

## practice
experiment.present_instructions()
experiment.run_practice()


## staircase
experiment.present_instructions()
experiment.run_staircase()

## experiment
experiment.set_experiment_parameters()
experiment.present_instructions()
experiment.run_experiment()

## thank you

experiment.present_thank_you_screen()