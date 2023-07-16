import csv
from classes.master import Master
from cds_objects.measure_condition_component import MeasureConditionComponent
import classes.globals as g


class MeasureCondition(Master):

    def __init__(self, elem, measure_sid, additional_code):
        Master.__init__(self, elem)
        self.elem = elem
        self.measure_sid = measure_sid
        self.additional_code = additional_code
        self.measure_condition_component_array = []
        self.condition_duty_string = ""
        self.get_data()

    def get_data(self):
        if self.operation != "D":
            self.sid = Master.process_null_float(self.elem.find("sid"))
            self.condition_sequence_number = Master.process_null(self.elem.find("conditionSequenceNumber"))
            self.certificate_code = Master.process_null(self.elem.find("certificate/certificateCode"))
            self.certificate_type_code = Master.process_null(self.elem.find("certificate/certificateType/certificateTypeCode"))
            self.certificate = self.certificate_type_code + self.certificate_code
            self.action_code = Master.process_null(self.elem.find("measureAction/actionCode"))
            self.condition_code = Master.process_null(self.elem.find("measureConditionCode/conditionCode"))
            self.condition_duty_amount = Master.process_null(self.elem.find("conditionDutyAmount"))
            self.condition_measurement_unit_code = Master.process_null(self.elem.find("measurementUnit/measurementUnitCode"))
            self.condition_measurement_unit_qualifier_code = Master.process_null(self.elem.find("measurementUnitQualifier/measurementUnitQualifierCode"))
            self.condition_monetary_unit_code = Master.process_null(self.elem.find("monetaryUnit/monetaryUnitCode"))
            if self.condition_duty_amount != "":
                self.get_condition_duty_string()

            self.get_condition_code_description()
            self.get_action_code_description()
            self.get_measure_condition_components()

            self.output = ""
            if self.certificate == "":
                self.certificate = "n/a"
            self.output += "Condition " + str(self.condition_sequence_number).zfill(2) + ". "
            self.output += "Certificate: " + self.certificate + ", "
            self.output += "Condition code: " + self.condition_code + " (" + self.condition_code_description + "), "
            self.output += "Action code: " + self.action_code + " (" + self.action_code_description + ")"
            if self.condition_duty_string != "":
                self.output += "<br />Condition duty amount: " + self.condition_duty_string + ";"
            if self.measure_condition_component_string != "":
                self.output += "<br />Conditional duty: " + self.measure_condition_component_string + ";"

            self.output += "<br /><br />"
        else:
            self.output = ""

    def get_condition_duty_string(self):
        self.condition_duty_string = ""
        if self.condition_monetary_unit_code != "":
            self.condition_duty_string = self.condition_monetary_unit_code + str(self.condition_duty_amount) + " "
        else:
            self.condition_duty_string = str(self.condition_duty_amount) + " "
        if self.condition_measurement_unit_code != "":
            self.condition_duty_string += self.condition_measurement_unit_code + " "
        if self.condition_measurement_unit_qualifier_code != "":
            self.condition_duty_string += self.condition_measurement_unit_qualifier_code
        self.condition_duty_string = self.condition_duty_string.strip()

    def get_measure_condition_components(self):
        measure_condition_components = self.elem.findall('measureConditionComponent')
        self.measure_condition_component_string = ""

        if measure_condition_components:
            self.measure_condition_components = []
            for measure_condition_component in measure_condition_components:
                mcc = MeasureConditionComponent(measure_condition_component, self.sid)
                self.measure_condition_components.append(mcc)

            self.measure_condition_components.sort(key=lambda x: x.duty_expression_id, reverse=False)

            for mcc in self.measure_condition_components:
                measure_condition_component_string = mcc.duty_string
                if measure_condition_component_string != "":
                    self.measure_condition_component_string += measure_condition_component_string

        self.measure_condition_component_string_excel = self.measure_condition_component_string.replace("<br />", "\n")
        self.measure_condition_component_array = [
            "Measure condition components",
            self.measure_condition_component_string
        ]

        if "X3" in self.additional_code:
            if self.measure_condition_component_string != "":
                if self.measure_condition_component_string not in g.conditional_duty_list:
                    g.conditional_duty_list.append(self.measure_condition_component_string)

    def get_condition_code_description(self):
        self.condition_code_description = g.condition_code_dict[self.condition_code]

    def get_action_code_description(self):
        self.action_code_description = g.action_code_dict[self.action_code]
