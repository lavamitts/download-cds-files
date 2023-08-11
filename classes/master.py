import os
import logging


class Master(object):
    def __init__(self, elem):
        # Get the operation type
        try:
            self.operation = elem.find("metainfo/opType").text
        except Exception as e:
            self.operation = ""
            logging.warning('No operation found', e.args)

        # Get the national versus EU
        try:
            self.national = 1 if elem.find(
                "metainfo/origin").text == "N" else 0
        except Exception as e:
            self.national = 0
            logging.warning('No origin node found', e.args)

        self.expand_operation()

    def expand_operation(self):
        if self.operation == "C":
            self.operation_text = "Create a new"
        elif self.operation == "U":
            self.operation_text = "Update an existing"
        elif self.operation == "D":
            self.operation_text = "Delete a"

    @staticmethod
    def process_null(elem):
        if elem is None:
            return ""
        else:
            return elem.text

    def process_null_float(elem):
        if elem is None:
            return ""
        else:
            return float(elem.text)

    def process_null_int(elem):
        if elem is None:
            return ""
        else:
            return int(elem.text)

    @staticmethod
    def get_template(filename):
        path = os.path.join(os.getcwd(), "templates")
        filename = os.path.join(path, filename)
        f = open(filename, "r")
        contents = f.read()
        return contents

    @staticmethod
    def format_date(d):
        if d is None:
            return ""
        elif d == "":
            return ""
        else:
            return d[8:10] + "/" + d[5:7] + "/" + d[0:4]

    @staticmethod
    def format_date_ymd(d):
        if d is None:
            return ""
        elif d == "":
            return ""
        else:
            return d[0:4] + "-" + d[5:7] + "-" + d[8:10]
