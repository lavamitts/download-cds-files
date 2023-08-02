import sys
from classes.master import Master
import classes.globals as g

from cds_objects.change import MeasureChange
from cds_objects.measure_component import MeasureComponent
from cds_objects.measure_condition import MeasureCondition
from cds_objects.measure_condition_component import MeasureConditionComponent
from cds_objects.measure_excluded_geographical_area import MeasureExcludedGeographicalArea
from cds_objects.footnote_association_measure import FootnoteAssociationMeasure


class Measure(Master):
    def __init__(self, elem, worksheet, row_count):
        Master.__init__(self, elem)
        self.elem = elem
        self.worksheet = worksheet
        self.row_count = row_count
        self.combined_duty = ""
        self.footnote_string = ""
        self.descriptions = []
        self.duty_expression_array = []
        self.measure_condition_array = []
        self.mcs = []
        self.get_data()

    def get_data(self):
        self.measure_sid = Master.process_null_int(self.elem.find("sid"))
        self.measure_generating_regulation_id = Master.process_null(self.elem.find("measureGeneratingRegulationId"))
        self.geographical_area_id = Master.process_null(self.elem.find("geographicalArea/geographicalAreaId"))
        self.goods_nomenclature_item_id = Master.process_null(self.elem.find("goodsNomenclature/goodsNomenclatureItemId"))
        self.measure_type_id = Master.process_null(self.elem.find("measureType/measureTypeId"))
        self.validity_start_date = Master.process_null(self.elem.find("validityStartDate"))
        self.validity_end_date = Master.process_null(self.elem.find("validityEndDate"))
        self.ordernumber = Master.process_null(self.elem.find("ordernumber"))
        self.additional_code_code = Master.process_null(self.elem.find("additionalCode/additionalCodeCode"))
        self.additional_code_type_id = Master.process_null(self.elem.find("additionalCode/additionalCodeType/additionalCodeTypeId"))
        self.additional_code = self.additional_code_type_id + self.additional_code_code

        if self.measure_sid == -1011445882:
            a = 1

        self.get_geographical_area_description()
        self.get_measure_type_description()
        self.get_measure_components()
        self.get_measure_conditions()
        self.get_measure_excluded_geographical_areas()
        self.get_footnotes()
        self.get_regulation_group_id()

        change = MeasureChange(self.measure_sid, self.goods_nomenclature_item_id, "Measure", self.operation)

        if self.additional_code != "":
            if self.additional_code[0:2] == "X3":
                if self.additional_code == "X333":
                    a = 1
                obj = {
                    "conditions": []
                }
                if len(self.mcs) > g.max_condition_count:
                    g.max_condition_count = len(self.mcs)
                    g.max_add_code = self.additional_code

                for mc in self.mcs:
                    c = {
                        "condition_sequence_number": int(mc.condition_sequence_number),
                        "duty_amount": mc.condition_duty_amount,
                        "condition_measurement_unit_code": mc.condition_measurement_unit_code,
                        "condition_measurement_unit_qualifier_code": mc.condition_measurement_unit_qualifier_code,
                        "action_code": mc.action_code,
                        "positive": True if mc.action_code != "06" else False,
                        "component_string": mc.measure_condition_component_string_excel
                    }
                    obj["conditions"].append(c)

                g.code_master_list[self.additional_code] = obj
                a = 1
        g.change_list.append(change)
        a = 1

    def get_regulation_group_id(self):
        if self.measure_generating_regulation_id in g.base_regulation_dict:
            self.regulation_group_id = g.base_regulation_dict[self.measure_generating_regulation_id]
        else:
            self.regulation_group_id = ""
        self.has_group_id_issue = False
        if self.additional_code_code is not None:
            if self.measure_type_id in ["103", "105", "112", "115", "117", "119"]:
                if "00" in self.additional_code_code:
                    if self.regulation_group_id != "SUS":
                        self.has_group_id_issue = True
                if "00" not in self.additional_code_code:
                    if self.regulation_group_id != "DNC":
                        self.has_group_id_issue = True

    def get_geographical_area_description(self):
        try:
            self.geographical_area_description = g.geography_dict[self.geographical_area_id]
        except Exception as e:
            print("Failure on geo area", self.geographical_area_id)
            sys.exit()

    def get_measure_type_description(self):
        self.measure_type_description = g.measure_type_dict[self.measure_type_id]

    def write_data(self):
        # Write the Excel
        self.worksheet.write(self.row_count, 0, self.operation_text + " measure", g.excel.format_wrap)
        self.worksheet.write(self.row_count, 1, self.goods_nomenclature_item_id, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 2, self.additional_code, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 3, self.measure_type_id + " (" + self.measure_type_description + ")", g.excel.format_wrap)
        self.worksheet.write(self.row_count, 4, self.geographical_area_id + " (" + self.geographical_area_description + ")", g.excel.format_wrap)
        self.worksheet.write(self.row_count, 5, self.ordernumber, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 6, Master.format_date(self.validity_start_date), g.excel.format_wrap)
        self.worksheet.write(self.row_count, 7, Master.format_date(self.validity_end_date), g.excel.format_wrap)
        self.worksheet.write(self.row_count, 8, self.combined_duty, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 9, self.exclusion_string, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 10, self.footnote_string, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 11, self.measure_condition_string_excel, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 12, self.measure_sid, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 13, self.measure_generating_regulation_id, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 14, self.regulation_group_id, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 15, self.has_group_id_issue, g.excel.format_wrap)

    def get_measure_components(self):
        measure_components = self.elem.findall('measureComponent')
        self.measure_components = []
        self.combined_duty = ""

        if measure_components:
            for measure_component in measure_components:
                duty_string = MeasureComponent(measure_component).duty_string
                if duty_string is not None:
                    self.measure_components.append(duty_string)

        for item in self.measure_components:
            self.combined_duty += " " + item
        self.combined_duty = self.combined_duty.strip()
        self.duty_expression_array = [
            "Duty expression",
            self.combined_duty
        ]

    def get_measure_conditions(self):
        measure_conditions = self.elem.findall('measureCondition')
        self.measure_condition_string = ""

        if measure_conditions:
            mcs = []
            for measure_condition in measure_conditions:
                mc = MeasureCondition(measure_condition, self.measure_sid, self.additional_code)
                mcs.append(mc)

            if len(mcs) > 0:
                try:
                    self.mcs = sorted(mcs, key=lambda x: x.condition_sequence_number, reverse=False)
                except Exception as e:
                    a = 1
            else:
                self.mcs = []

            for mc in self.mcs:
                measure_condition_string = mc.output
                if measure_condition_string != "":
                    self.measure_condition_string += measure_condition_string
        self.measure_condition_string_excel = self.measure_condition_string.replace("<br />", "\n")

        self.measure_condition_array = [
            "Measure conditions",
            self.measure_condition_string
        ]

    def get_measure_excluded_geographical_areas(self):
        measure_excluded_geographical_areas = self.elem.findall('measureExcludedGeographicalArea')
        self.measure_excluded_geographical_areas = []
        self.exclusion_string = ""

        if measure_excluded_geographical_areas:
            for measure_excluded_geographical_area in measure_excluded_geographical_areas:
                geographical_area_id = MeasureExcludedGeographicalArea(
                    measure_excluded_geographical_area).geographical_area_id
                if geographical_area_id is not None:
                    self.exclusion_string += geographical_area_id + ", "

        self.exclusion_string = self.exclusion_string.strip()
        self.exclusion_string = self.exclusion_string.strip(",")

        self.exclusion_string_array = [
            "Excluded countries",
            self.exclusion_string
        ]

    def get_footnotes(self):
        footnotes = self.elem.findall('footnoteAssociationMeasure')
        self.footnotes = []
        self.footnote_string = ""

        if footnotes:
            for footnote in footnotes:
                footnote_id = FootnoteAssociationMeasure(footnote).footnote
                if footnote_id != "":
                    self.footnote_string += footnote_id + ", "

        self.footnote_string = self.footnote_string.strip()
        self.footnote_string = self.footnote_string.strip(",")

        self.footnote_array = [
            "Associated footnotes",
            self.footnote_string
        ]
