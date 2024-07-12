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



def key_bit_select(ini_default:str) -> int:
    pass


# Usage example
if __name__ == "__main__":
    filepath = 'template/example.ini'  # Replace with your .ini file path
    params = read_ini(filepath)
    print(params)
