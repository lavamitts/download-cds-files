from classes.geography_list import GeographyList
from classes.reference_data import ActionCodeList, MeasureTypeList, ConditionCodeList, BaseRegulationList


# Get a list of all geo areas
print("Getting reference data")

obj = GeographyList()
geography_dict = obj.geography_dict
geography_hjid_dict = obj.geography_hjid_dict

# Get a list of all measure types
obj = MeasureTypeList()
measure_type_dict = obj.measure_type_dict

# Get a list of all action codes
obj = ActionCodeList()
action_code_dict = obj.action_code_dict

# Get a list of all condition codes
obj = ConditionCodeList()
condition_code_dict = obj.condition_code_dict

# Get a list of all base regulations
obj = BaseRegulationList()
base_regulation_dict = obj.base_regulation_dict

print("Getting reference data - complete")

change_list = []
code_lists = []
definition_list = {}

duty_list = []
conditional_duty_list = []
code_master_list = {}
max_condition_count = 0
max_add_code = ""
