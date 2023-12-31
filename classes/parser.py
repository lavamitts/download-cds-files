import os
import sys
import csv
from datetime import datetime
from dotenv import load_dotenv

import classes.globals as g
import classes.functions as f
from classes.database import Database
from classes.classification import Classification
from .xml_file import XmlFile


class Parser(object):
    def __init__(self):
        load_dotenv('.env')
        self.OVERWRITE_XLSX = int(os.getenv('OVERWRITE_XLSX'))
        self.alcohol_specific = int(os.getenv('ALCOHOL_SPECIFIC'))
        self.path = os.path.join(os.getcwd(), "resources")
        self.xml_path = os.path.join(self.path, "xml")
        self.xlsx_path = os.path.join(self.path, "xlsx")
        self.balance_path = os.path.join(self.path, "balances")

    def parse_files(self):
        if self.alcohol_specific:
            # To enforce a specific data file parse action
            file_list = [
                "export-20240707T000000_20230707T235959-20230708T001536.xml"
            ]
            self.OVERWRITE_XLSX = 1
        else:
            file_list = os.listdir(self.xml_path)

        file_list.sort()
        for filename in file_list:
            if filename.endswith(".xml"):
                if self.OVERWRITE_XLSX == 1:
                    proceed = True
                else:
                    excel_filename = f.xml_to_xlsx_filename(filename)
                    proceed = not self.check_exists(excel_filename)
                if proceed:
                    xml_file = XmlFile(filename)
                    xml_file.parse_xml()
                    xml_file.check_for_document_codes()
            else:
                continue

    def check_exists(self, filename):
        filename = filename.replace("xml", "xlsx")
        xlsx_filename = os.path.join(self.xlsx_path, filename)
        exists = os.path.exists(xlsx_filename)
        return exists
