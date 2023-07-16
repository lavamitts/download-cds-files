import csv
from classes.master import Master
import classes.globals as g
import classes.functions as f


class MeasureComponent(Master):

    def __init__(self, elem):
        Master.__init__(self, elem)
        self.elem = elem
        self.get_data()

    def get_data(self):
        if self.operation != "D":
            self.duty_amount = Master.process_null_float(self.elem.find("dutyAmount"))
            self.duty_expression_id = Master.process_null(self.elem.find("dutyExpression/dutyExpressionId"))
            self.measurement_unit_code = Master.process_null(self.elem.find("measurementUnit/measurementUnitCode"))
            self.measurement_unit_qualifier_code = Master.process_null(self.elem.find("measurementUnitQualifier/measurementUnitQualifierCode"))
            self.monetary_unit_code = Master.process_null(self.elem.find("monetaryUnit/monetaryUnitCode"))
            self.get_duty_string()
        else:
            self.duty_string = None

    def get_duty_string(self):
        self.duty_string = ""

        if self.duty_expression_id == "01":
            if self.monetary_unit_code == "":
                self.duty_string += "{0:1.4f}".format(self.duty_amount) + "%"
            else:
                self.duty_string += "{0:1.4f}".format(self.duty_amount) + " " + self.monetary_unit_code
                if self.measurement_unit_code != "":
                    self.duty_string += " / " + f.get_measurement_unit(self.measurement_unit_code)
                    if self.measurement_unit_qualifier_code != "":
                        self.duty_string += " / " + f.get_qualifier(self.measurement_unit_qualifier_code)

        elif self.duty_expression_id in ("04", "19", "20"):
            if self.monetary_unit_code == "":
                self.duty_string += "+ {0:1.4f}".format(self.duty_amount) + "%"
            else:
                self.duty_string += "+ {0:1.4f}".format(self.duty_amount) + " " + self.monetary_unit_code
                if self.measurement_unit_code != "":
                    self.duty_string += " / " + f.get_measurement_unit(self.measurement_unit_code)
                    if self.measurement_unit_qualifier_code != "":
                        self.duty_string += " / " + f.get_qualifier(self.measurement_unit_qualifier_code)

        elif self.duty_expression_id == "15":
            if self.monetary_unit_code == "":
                self.duty_string += "MIN {0:1.4f}".format(self.duty_amount) + "%"
            else:
                self.duty_string += "MIN {0:1.4f}".format(self.duty_amount) + " " + self.monetary_unit_code
                if self.measurement_unit_code != "":
                    self.duty_string += " / " + f.get_measurement_unit(self.measurement_unit_code)
                    if self.measurement_unit_qualifier_code != "":
                        self.duty_string += " / " + f.get_qualifier(self.measurement_unit_qualifier_code)

        elif self.duty_expression_id in ("17", "35"):  # MAX
            if self.monetary_unit_code == "":
                self.duty_string += "MAX {0:1.4f}".format(self.duty_amount) + "%"
            else:
                self.duty_string += "MAX {0:1.4f}".format(self.duty_amount) + " " + self.monetary_unit_code
                if self.measurement_unit_code != "":
                    self.duty_string += " / " + f.get_measurement_unit(self.measurement_unit_code)
                    if self.measurement_unit_qualifier_code != "":
                        self.duty_string += " / " + f.get_qualifier(self.measurement_unit_qualifier_code)

        elif self.duty_expression_id in ("12"):
            self.duty_string += " + AC"

        elif self.duty_expression_id in ("14"):
            self.duty_string += " + ACR"

        elif self.duty_expression_id in ("21"):
            self.duty_string += " + SD"

        elif self.duty_expression_id in ("25"):
            self.duty_string += " + SDR"

        elif self.duty_expression_id in ("27"):
            self.duty_string += " + FD"

        elif self.duty_expression_id in ("29"):
            self.duty_string += " + FDR"

        elif self.duty_expression_id in ("99"):
            self.duty_string += self.measurement_unit_code

        else:
            print("Measure condition: Unexpected duty expression found", self.duty_expression_id)

        self.duty_string = self.duty_string.replace("  ", " ")
        if self.duty_string not in g.duty_list:
            g.duty_list.append(self.duty_string)
