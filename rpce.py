# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 18:12:07 2022

@author: rudip
"""

import pandas as pd

def get_file_contents(filename = "test.psc"):
    filelines = []
    error = 0
    with open(filename,'r', encoding="utf-8") as file_in:
        for line in file_in:
            filelines.append(line)
            
    return error, filelines

def get_value_of_params(nameofparam = "'Ein Fehler fand statt!'"):
    print("Geben Sie einen Wert für den Parameter " + nameofparam + " ein: ")
    x = input()
    return x
    

def check_code(filelines):
    return 0
    pass


def boolean_statement(statement)-> bool:
    statement = statement.strip()
    return eval(statement)


# This function executes the pseudocode
def execute_code(filelines):
    length_filelines = len(filelines)
    int_current_line = 0
    string_current_line = ""
    int_current_state = 0 # 0 = before begin of algorithm; 1 = params; 2 = local; 3 = Code
    
    # Dataframe which holds variables
    variables = pd.DataFrame()
    dataframe_current_index = 0 # my own indexes
    
    
    # get the algorithm interface
    while int_current_line < length_filelines:
        string_current_line = filelines[int_current_line].strip()
        
        if int_current_state == 0 and "algorithm" == string_current_line[0:9]:
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
                            var_name = var_name[x].rstrip(')')
                            break
                    new_variable = pd.Series({'myindex': dataframe_current_index, 'name': var_name, 'direction': var_direction, 'value': "0", 'datatype': "int"})
                    dataframe_current_index = dataframe_current_index + 1
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
                    new_variable = pd.Series({'myindex': dataframe_current_index, 'name': var_name, 'direction': 'o', 'value': "0", 'datatype': var_datatype})
                    dataframe_current_index = dataframe_current_index + 1
                    variables = variables.append(new_variable, ignore_index=True)
                    
                i = i + 1
            int_current_state = 1 # now the params start
            
        elif int_current_state == 1:
            if ("local" in string_current_line) or ("Local" in string_current_line):
                int_current_state = 2
                continue
            if string_current_line == "": # Wenn nichts (außer Leerzeichen, die oben entfernt werden) in der Zeile steht
                continue
            
            string_current_line = string_current_line.replace("param", '')
            string_current_line = string_current_line.replace("Param", '')
            string_current_line = string_current_line.strip(' ')
            
            var_datatype = string_current_line.split(' ')[0]
            string_current_line = string_current_line.replace(var_datatype, '').strip(' ')
            if '[' in string_current_line: # if it is an array
                var_name = string_current_line.split('[')[0].strip(' ')
                array_min = string_current_line.split('[')[1].replace(']','').replace(';','').strip(' ')[0:2].strip('.')
                array_max = string_current_line.split('[')[1].replace(']','').replace(';','').strip(' ')[-2:].strip('.')
                if not isinstance(array_max, int):
                    temp = variables.query("name == @array_max").iloc[0].myindex
                    array_max = variables.at[temp,"value"]
                temp = variables.query("name == @var_name").iloc[0].myindex
                var_direction = variables.at[temp,"direction"]
                # variables.drop(labels=var_name,inplace=True)
                var_datatype = var_datatype + "_array"
                for i in range(int(array_min), int(array_max) + 1):
                    array_pos_var_name = (var_name + '[' + str(i) + ']')
                    var_value = get_value_of_params(array_pos_var_name)
                    new_variable = pd.Series({'myindex': dataframe_current_index, 'name': array_pos_var_name, 'direction': var_direction, 'value': var_value, 'datatype': var_datatype})
                    dataframe_current_index = dataframe_current_index + 1
                    variables = variables.append(new_variable, ignore_index=True)
            else:
                var_name = string_current_line.replace(';', '')
                var_value = get_value_of_params(var_name)
                temp = variables.query("name == @var_name").iloc[0].myindex
                variables.at[temp,"datatype"] = var_datatype
                variables.at[temp,"value"] = var_value
        
        elif int_current_state == 2:
            if string_current_line == "": # Wenn nichts (außer Leerzeichen, die oben entfernt werden) in der Zeile steht
                int_current_state = 3
                break
            
            string_current_line = string_current_line.replace("local", '')
            string_current_line = string_current_line.replace("Local", '')
            string_current_line = string_current_line.strip(' ')
            
            var_datatype = string_current_line.split(' ')[0]
            var_value = string_current_line.replace(var_datatype, '').split('=')[1].strip(';').strip(' ')
            string_current_line = string_current_line.replace(var_datatype, '').split('=')[0].strip(' ')
            if '[' in string_current_line: # if it is an array
                var_name = string_current_line.split('[')[0].strip(' ')
                array_min = string_current_line.split('[')[1].replace(']','').replace(';','').strip(' ')[0:2].strip('.')
                array_max = string_current_line.split('[')[1].replace(']','').replace(';','').strip(' ')[-2:].strip('.')
                if not isinstance(array_max, int):
                    temp = variables.query("name == @array_max").iloc[0].myindex
                    array_max = variables.at[temp,"value"]
                var_datatype = var_datatype + "_array"
                for i in range(int(array_min), int(array_max) + 1):
                    array_pos_var_name = (var_name + '[' + str(i) + ']')
                    new_variable = pd.Series({'myindex': dataframe_current_index, 'name': array_pos_var_name, 'direction': "local", 'value': var_value, 'datatype': var_datatype})
                    dataframe_current_index = dataframe_current_index + 1
                    variables = variables.append(new_variable, ignore_index=True)
            else:
                var_name = string_current_line.replace(';', '')
                new_variable = pd.Series({'myindex': dataframe_current_index, 'name': var_name, 'direction': "local", 'value': var_value, 'datatype': var_datatype})
                dataframe_current_index = dataframe_current_index + 1
                variables = variables.append(new_variable, ignore_index=True)
            
            
        int_current_line = int_current_line + 1
    
    int_current_line = int_current_line + 1
    
    # actual code execution
    int_states = [[0,0]] # 0 = execute every line; 1 = if; 2 = while; 4 = for
    # first position is state; secound is position
    
    
    while int_current_line < length_filelines:
        string_current_line = filelines[int_current_line].strip()
        int_current_state = int_states[len(int_states)-1]
        
        
        if string_current_line == '':
            int_current_line = int_current_line + 1
            continue
        
        if "elseif" in string_current_line or "else if" in string_current_line:
            pass
        elif "else" in string_current_line:
           pass
        elif "if" in string_current_line:
            int_states.append([1,int_current_line])
            pass
        elif "while" in string_current_line:
            string_current_line = string_current_line.strip("while").strip("do")
            
            if not boolean_statement(string_current_line):
                x = 1
                while x > 0:
                    int_current_line = int_current_line + 1
                    tempstr = filelines[int_current_line].strip()
                    if "for" in tempstr or "if" in tempstr or "while" in tempstr:
                        x = x + 1
                    if "end" in tempstr:
                        x = x - 1
            else:
                int_states.append([2,int_current_line])
            
        # elif "repeat" in string_current_line:
        #    pass
        # elif "do" in string_current_line:
        #    pass
        elif "for" in string_current_line:
            variable =
            up =
            by =
            if int_current_state[1] != int_current_line:    # wenn diese for das erste Mal aufgerufen wird
                int_states.append([4,int_current_line])
                # = zuweisen
            else:
                # hinaufzählen
                pass
            
            wert_variable =
            
            if not wert_variable <= up:
                x = 1
                while x > 0:
                    int_current_line = int_current_line + 1
                    tempstr = filelines[int_current_line].strip()
                    if "for" in tempstr or "if" in tempstr or "while" in tempstr:
                        x = x + 1
                    if "end" in tempstr:
                        x = x - 1
                int_states.pop()
        #elif "return" in string_current_line:
        #    pass
        elif "end" in string_current_line:
            if int_current_state[0] == 2:
                int_current_line = int_current_state[1]
                int_states.pop()
                continue
            if int_current_state[0] == 4:
                int_current_line = int_current_state[1]
                continue
                
        elif '=' in string_current_line:
            pass
        else:
            # Funktionsaufruf etc.
            pass
        
        int_current_line = int_current_line + 1


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