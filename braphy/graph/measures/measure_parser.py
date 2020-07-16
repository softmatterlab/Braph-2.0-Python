import importlib
from braphy.graph.measures.measure import Measure
import re

class MeasureParser():

    measures = None
    measures_descriptions = None
    measures_dimensions = None
    measures_dimensions_str = None

    def list_measures():
        if MeasureParser.measures is not None:
            return MeasureParser.measures

        measures_dict = {}
        for measure in Measure.__subclasses__():
            snake_case_measure_name = re.sub(r'(?<!^)(?=[A-Z])', '_', measure.__name__).lower()
            measure = getattr(importlib.import_module("braphy.graph.measures.{}".format(snake_case_measure_name)), measure.__name__)
            graph_types = measure.get_valid_graph_types()
            for graph_type in graph_types:
                if graph_type not in measures_dict.keys():
                    measures_dict[graph_type] = {}
                measures_dict[graph_type][measure] = graph_types[graph_type]
        MeasureParser.measures = measures_dict
        return measures_dict

    def list_measures_descriptions():
        if MeasureParser.measures_descriptions is not None:
            return MeasureParser.measures_descriptions
        measures_dict = {}
        for measure_type in Measure.__subclasses__():
            measures = measure_type.get_description()
            measures_dict[measure_type] = measures
        MeasureParser.measures_descriptions = measures_dict
        return measures_dict

    def list_measures_dimensions():
        if MeasureParser.measures_dimensions is not None:
            return MeasureParser.measures_dimensions
        measures_dict = {}
        for measure_type in Measure.__subclasses__():
            for sub_measure, dimension in measure_type.dimensions().items():
                measures_dict[sub_measure] = dimension
        MeasureParser.measures_dimensions = measures_dict
        return measures_dict

    def list_measures_dimensions_str():
        if MeasureParser.measures_dimensions_str is not None:
            return MeasureParser.measures_dimensions_str
        measures_dict = {}
        for sub_measure, dimension in MeasureParser.list_measures_dimensions().items():
            measures_dict[sub_measure] = Measure.dimensions_str(dimension)
        MeasureParser.measures_dimensions_str = measures_dict
        return measures_dict
