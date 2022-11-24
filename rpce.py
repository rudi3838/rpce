# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 18:12:07 2022

@author: rudip
"""

import pandas as pd

def get_file_contents(filename = "test.psc"):
    filelines = []
    error = 0
    with open(filename) as file_in:
        for line in file_in:
            filelines.append(line)
            
    return error, filelines
    

def check_code(filelines):
    return 0
    pass


# This function executes the pseudocode
def execute_code(filelines):
    length_filelines = len(filelines)
    int_current_line = 0
    string_current_line = ""
    
    # Dataframe which holds variables
    variables = pd.DataFrame()
    
    
    # get the algorithm interface
    while int_current_line < length_filelines:
        string_current_line = filelines[int_current_line]
        
        if "algorithm" == string_current_line[0:9]:
            int_position = 0 # 0 = before bracket; 1 = in brackets; 2 = after brackets
            i = 0
            #information about one variable
            var_direction = 'n'
            var_name = ""
            while i < len(string_current_line):
                letter = string_current_line[i]
                if letter == ' ' or letter == '\t':
                    pass
                elif int_position == 0 and letter == '(':
                    int_position = 1;
                elif int_position == 1 and letter == ')':
                    int_position = 2
                elif int_position == 1 and letter == '\\':
                    var_direction = string_current_line[i+1]
                    var_name = string_current_line[i+2:].split(' ')
                    for x in range(0,len(var_name)):
                        if var_name[x] != '':
                            var_name = var_name[x]
                            break
                    new_variable = pd.Series({'name': var_name, 'direction': var_direction, 'value': "0", 'datatype': "int"})
                    variables = variables.append(new_variable, ignore_index=True)
                elif int_position == 2 and letter == ':':
                    string_current_line = string_current_line[i:].split(' ')
                    temp_already_datatype = False
                    var_name = ""
                    var_datatype = ""
                    for x in range(0,len(string_current_line)):
                        if string_current_line[x] != '':
                            if temp_already_datatype:
                                var_name = string_current_line[x]
                                break
                            else:
                                var_datatype = string_current_line[x]
                                temp_already_datatype = True
                    new_variable = pd.Series({'name': var_name, 'direction': 'o', 'value': "0", 'datatype': var_datatype})
                    variables = variables.append(new_variable, ignore_index=True)
                    
                i = i + 1
            
            
        int_current_line = int_current_line + 1
    
    int_current_line = int_current_line + 1
    
    while int_current_line < length_filelines:
        pass


"""
Test Code down below
"""

def main():
    
    filename = "test.psc"
    error, filelines = get_file_contents(filename)
    if error != 0:
        print("Something happened")
    
    error = check_code(filelines)
    if error != 0:
        print("Something happened")
        
    error = execute_code(filelines)
    if error != 0:
        print("Something happened")
    
    return

if __name__ == "__main__":
    main()