import configparser

def read_ini(filepath:str) -> dict:
    # Create a configparser object
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(filepath)
    
    # Dictionary to store configurations
    parameters = {}

    # Iterate through each section in the .ini file
    for section in config.sections():
        # Iterate through each option in the section
        for option in config.options(section):
            # Store the option and its value in the dictionary
            parameters[option] = config.get(section, option)

    return parameters



def key_bit_select(ini_default:str, func:str, pre:float, inbit:int) -> int:
    # Create a configparser object
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(ini_default)
    
    # Dictionary to store configurations
    parameters = {}

    # Iterate through each section in the .ini file
    for section in config.sections():
        parameters[section] = []
        # Iterate through each option in the section
        for option in config.options(section):
            # Store the option and its value in the dictionary
            parameters[section].append((float(option), int(config.get(section, option))))
        parameters[section] = sorted(parameters[section], key=lambda x : x[0])

    if func not in parameters.keys():
        return inbit

    for section in parameters.keys():
        if section == func:
            for ind, it in enumerate(parameters[section]):
                if pre < it[0]:
                    if ind == 0:
                        kb = inbit
                    else:
                        kb = parameters[section][ind-1][1]
                    break
            if ind == len(parameters[section])-1:
                kb = parameters[section][-1][1]
            break
    
    return kb


# Usage example
if __name__ == "__main__":
    # filepath = 'template/example.ini'  # Replace with your .ini file path
    # params = read_ini(filepath)
    # print(params)

    dK = 'template/defaultK.ini'
    kb = key_bit_select(dK, 'tanh', 0.01, 15)
    print(kb)