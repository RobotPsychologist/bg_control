import os
import importlib
import inspect
import sktime.annotation as ann
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
import yaml
# List of relevant class names
relevant_class_names = [
    "ClaSPSegmentation",
    "EAgglo",
    "GaussianHMM",
    "GMMHMM",
    "GreedyGaussianSegmentation",
    # "HMM",
    "InformationGainSegmentation",
    "PoissonHMM",
    "STRAY",
    "ClusterSegmenter"
]

# List to store the relevant classes
model_classes = []

def find_relevant_classes_in_module(module):
    """
    Search for relevant classes in a given module and add them to the model_classes list.
    """
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if name in relevant_class_names:  # Check if the class is relevant
            model_classes.append(obj)  # Save the class reference

def import_relevant_classes():
    """
    imports classes from sktime.annotation based on the relevant_class_names list
    """
    annotation_path = os.path.dirname(ann.__file__)  # Get the folder path

    # Loop through all .py files in the annotation folder
    for filename in os.listdir(annotation_path):
        if filename.endswith(".py") and filename != "__init__.py":  # Ignore __init__.py
            module_name = f"sktime.annotation.{filename[:-3]}"  # Convert filename to module name
            
            try:
                # Import the module dynamically
                module = importlib.import_module(module_name)
                find_relevant_classes_in_module(module)  # Search for relevant classes
            except ImportError as e:
                print(f"Could not import {module_name}: {e}")


def load_model_configs():
    with open('model_configs.yaml', 'r') as file:
        return yaml.safe_load(file)
    
# Run the function to import relevant classes
import_relevant_classes()

model_configs = load_model_configs()
# Display the collected relevant classes
print(f"Collected {len(model_classes)} relevant classes:")
for cls in model_classes:
    print(f"- {cls.__name__}")
    if cls.__name__ in model_configs:
        config = model_configs[cls.__name__]
        instance = cls(**config)
        print(f"  Instantiated with config: {config}")
    else:
        print("  No config found, using default parameters")
        instance = cls()



