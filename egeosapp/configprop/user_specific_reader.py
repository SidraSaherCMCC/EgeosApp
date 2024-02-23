import configparser

def load_simulation_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)

    user_specific_properties = {}

    # Assuming all the properties in the file are required
    required_properties = [
        "model", "spillType", "duration", "oilParcelNumber", "plotStep",
        "simulationDuration", "spillRateCoefficient", "spillRate",
        "horizontalDiffusivity", "windCorrection", "stokesDrift",
        "var_19", "var_29", "var_39", "selector"
    ]

    for property_name in required_properties:
        try:
            user_specific_properties[property_name] = config.get("DEFAULT", property_name)
        except configparser.NoOptionError:
            # Handle missing properties if needed
            print(f"Warning: Property '{property_name}' not found in the configuration file.")

    return user_specific_properties

# Example usage:
file_path = "C:/CMCC/Egeos/EgeosCode/egeosdjango/egeosapp/configprop/user_specific.ini"
user_specific_config = load_simulation_config(file_path)

# Display the values
for key, value in user_specific_config.items():
    print(f"{key}: {value}")
