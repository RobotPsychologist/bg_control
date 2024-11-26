from pipeline_generator import PipelineGenerator
from sktime.transformations.series.exponent import ExponentTransformer
from sktime.transformations.series.cos import CosineTransformer

from sktime.transformations.series.impute import Imputer

from loguru import logger

gen = PipelineGenerator()

gen.load_data(["2024-11-15_679372__i5mins_d4hrs_c10g_l5hrs_n4.csv",
               "2024-11-15_679372__i5mins_d4hrs_c10g_l5hrs_n3.csv"])

gen.generate_pipeline([
    CosineTransformer(),
    Imputer(method = "constant", value = 0)
])

#gen.generate_pipeline(run = 1) #alternative method, get pipeline from a run

gen.fit_transform()

processed_data = gen.save_output()
print(processed_data["2024-11-15_679372__i5mins_d4hrs_c10g_l5hrs_n4.csv"].head())