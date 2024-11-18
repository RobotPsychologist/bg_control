from sktime.transformations.series.exponent import ExponentTransformer
from sktime.transformations.compose import Id
from sktime.transformations.compose import TransformerPipeline
from sklearn.preprocessing import StandardScaler
import pandas as pd

def run_pipeline(pipeline, data):
    '''
    run a transformer pipeline given certain data
    questions:  does the training script provide the pipeline, or should we build this in transformation
                do we want to work with only Series->Series or also Panel->Panel
    todo:   add flag to cache transformed data
            add flag to run as list of Series or as Panel
            log transformations applied
            testing
    '''
    transformed_data = []
    for df in data:
        transformed = pipeline.fit_transform(df)
        transformed_data.append(transformed)
    return transformed_data

def create_pipeline(transformers):
    '''
    creates a pipeline from a list of transformers (apply all in series)?
    questions:  how should FeatureUnions be handled?
    '''
    pipeline = TransformerPipeline(steps=transformers)
    return pipeline


