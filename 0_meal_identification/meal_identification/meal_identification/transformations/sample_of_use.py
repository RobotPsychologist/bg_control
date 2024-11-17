from pipeline_generator import PipelineGenerator
from sktime.transformations.series.exponent import ExponentTransformer
from sktime.transformations.series.cos import CosineTransformer

from sktime.transformations.series.impute import Imputer

from loguru import logger

gen = PipelineGenerator()

gen.load_data(["2024-11-14_500030__timeInter5mins_dayStart4hrs_minCarb5g_3hrMealW.csv",
               "2024-11-14_500030__timeInter5mins_dayStart4hrs_minCarb10g_3hrMealW.csv"])

gen.generate_pipeline([
    CosineTransformer(),
    Imputer(method = "constant", value = 0)
])

#gen.generate_pipeline(run = 1) #alternative method, get pipeline from a run

gen.fit_transform()

processed_data = gen.save_output()
print(processed_data)