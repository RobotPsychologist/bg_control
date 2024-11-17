from sktime.transformations.compose import TransformerPipeline

from loguru import logger

import random
import re
import os
import json
import pandas as pd

class PipelineGenerator():

    """
    Class to generate sktime transformer pipeline:
        Data is saved in 0_meal_identification/meal_identification/data/processed in the format:
            run_# - number of run
            run_#/data - the output data from that run
            run_#/pipelines - pipelines saved from the run

    to-do:
        load data from a dataframe (in addition to files)
        load transformers from json config file rather than .zip pipeline
        add getters/setters and other helper methods
        add functionality to delete previous runs
        clean up logic & good coding practices
        implement proper exception handling
        test with various transformers
        write documentation on how to use
    """

    def __init__(self, 
                 output_dir = "0_meal_identification/meal_identification/data/processed",
                 input_dir = "0_meal_identification/meal_identification/data/interim"):
        
        self.data_cat = {} 
        self.data_num = {} 
        self.pipe = {} 
        self.column_order = None #order of columns for data for consistency

        #set up paths for data directories
        self.processed_dir_path = os.path.join(self.__get_root_dir(), output_dir)
        self.interim_dir_path = os.path.join(self.__get_root_dir(), input_dir)
        self

    def load_data(self, raw_files):
        '''
        Loads data from files in the input_dir directory and splits it into numeric/categorical

        Parameters
        ----------
        raw_files : list of str
            list of datasets in input_dir to be used with the pipeline. Format: "filename.csv"

        Returns
        -------
        '''

        data = {}

        #read the data from interim directory
        for file in raw_files:
            file_path = os.path.join(self.interim_dir_path, file)
            data[file] = pd.read_csv(file_path, parse_dates=['date'])
        
        #separate data into numerical/categorical for sktime transformers 
        for key in data:
            self.column_order = list(data[key].columns)
            self.data_num[key] = data[key]._get_numeric_data()
            self.data_cat[key] = data[key][list(set(data[key].columns) - set(self.data_num[key].columns))]

    def generate_pipeline(self, transformers = None, run = None):
        '''
        Creates a pipeline either based on provided list of transformers or copies one from a previous run

        Parameters
        ----------
        transformers : optional, list of sktime transformers
            Transformers to be added into pipeline, in the provided order
        run: optional, int
            Number of the run from which transformer params should be taken
        Returns
        -------
        '''

        if not transformers and not run:
            raise TypeError("List of transformers or run number was not provided")

        # load pipeline from past runs
        if run:
            pipeline_path = os.path.join(self.processed_dir_path, f"run_{run}", "pipelines")

            for file in os.scandir(pipeline_path): # this is junky, refractor
                pipe = TransformerPipeline.load_from_path(os.path.join(pipeline_path, file))
                break

        # load pipeline from parameters
        else: 
            pipe = TransformerPipeline(steps = transformers)

        # clone pipeline to fit to different datasets
        for key in self.data_num:
            self.pipe[key] = pipe.clone() 

    def fit(self):
        '''
        Fits the pipeline to the loaded data

        Parameters
        ----------

        Returns
        -------
        '''
        for key in self.pipe:
            
            #fit if pipeline was not fitted before
            try: 
                self.pipe[key].check_is_fitted()
            except:
                self.pipe[key].fit(self.data_num[key])

    def transform(self):
        '''
        Transforms the data from the pipelines

        Parameters
        ----------

        Returns
        -------
        '''

        for key in self.pipe:
            self.data_num[key] = self.pipe[key].transform(self.data_num[key])

    def fit_transform(self):
        '''
        Applies fit and transform in sequence

        Parameters
        ----------

        Returns
        -------
        '''

        self.fit()
        self.transform()

    def save_output(
            self,
            output_dir = "0_meal_identification/meal_identification/data/processed"
    ):
        '''
        Applies fit and transform in sequence

        Parameters
        ----------
        output_dir: str
            The directory in which pipelines and transformed data should be stored
        Returns
        -------
        processed_data: dictionary of pandas DataFrames
            Data supplied to the PipelineGenerator after transformations
        '''

        output_dir = self.processed_dir_path 

        # figure out which run is the last one
        runs = []
        for i in os.listdir(output_dir):
            run_num = re.search("[0-9]+", i)
            if run_num:
                runs.append(int(run_num.group()))

        if not runs:
            runs = [0]
        new_run = max(runs)+1
        
        # make the run directory
        output_dir = os.path.join(output_dir, f"run_{new_run}")
        os.mkdir(output_dir)

        # make the data directory 
        dir_path_data = os.path.join(output_dir, "data")
        os.mkdir(dir_path_data)

        # make the pipeline directory 
        dir_path_pipelines = os.path.join(output_dir, "pipelines")
        os.mkdir(dir_path_pipelines)


        processed_data = {}
        # save processed datasets into the data directory and pipelines into pipeline directory
        for key in self.data_num:
            whole_data = pd.concat([self.data_num[key], self.data_cat[key]], axis=1)
            whole_data = whole_data[self.column_order]
            whole_data.to_csv(os.path.join(dir_path_data, key), index=True)

            processed_data[key] = whole_data

            pipeline_path = os.path.join(dir_path_pipelines, "Pipeline_" + key)
            pipeline_path = pipeline_path.rpartition('.')[0]
            self.pipe[key].save(path = pipeline_path)
        
        logger.info(self.pipe[key].get_params())
        
        # save pipeline configuration into json
        with open(os.path.join(dir_path_pipelines, "Pipeline_config.json"), "w") as json_file:
            transformer_config = random.choice(list(self.pipe.values())).get_params()
            json.dump({key: str(value) for key, value in transformer_config.items()}, json_file, indent=4) 

        return processed_data


    def __get_root_dir(self, current_dir=None):
        """
        Get the root directory of the project by looking for a specific directory 
        (e.g., '.github') that indicates the project root.

        Parameters
        ----------
        current_dir : str, optional
            The starting directory to search from. If None, uses the current working directory.

        Returns
        -------
        str
            The root directory of the project.
        """
        if current_dir is None:
            current_dir = os.getcwd()

        unique_dir = '.github'  # Directory that uniquely identifies the root

        while current_dir != os.path.dirname(current_dir):
            if os.path.isdir(os.path.join(current_dir, unique_dir)):
                return current_dir
            current_dir = os.path.dirname(current_dir)

        raise FileNotFoundError(f"Project root directory not found. '{unique_dir}' directory missing in path.")