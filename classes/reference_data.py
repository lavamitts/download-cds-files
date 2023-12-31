from classes.database import Database


class MeasureTypeList(object):
    def __init__(self):
        print("- Getting list of measure types")
        self.measure_type_dict = {}
        sql = """select mt.measure_type_id, mtd.description
        from measure_types mt, measure_type_descriptions mtd
        where mt.measure_type_id = mtd.measure_type_id
        and validity_end_date is null
        order by 1"""
        d = Database()
        rows = d.run_query(sql)
        for row in rows:
            self.measure_type_dict[row[0]] = row[1]


class ActionCodeList(object):
    def __init__(self):
        print("- Getting list of action codes")
        self.action_code_dict = {}
        sql = """select action_code, description from measure_action_descriptions mad order by 1"""
        d = Database()
        rows = d.run_query(sql)
        for row in rows:
            self.action_code_dict[row[0]] = row[1]


class ConditionCodeList(object):
    def __init__(self):
        print("- Getting list of condition codes")
        self.condition_code_dict = {}
        sql = """select condition_code, description from measure_condition_code_descriptions mccd order by 1"""
        d = Database()
        rows = d.run_query(sql)
        for row in rows:
            self.condition_code_dict[row[0]] = row[1]

class BaseRegulationList(object):
    def __init__(self):
        print("- Getting list of condition codes")
        self.base_regulation_dict = {}
        sql = """
        select base_regulation_id, regulation_group_id
        from base_regulations where validity_start_date >= '2016-01-01'
        order by base_regulation_id
        """
        d = Database()
        rows = d.run_query(sql)
        for row in rows:
            self.base_regulation_dict[row[0]] = row[1]
