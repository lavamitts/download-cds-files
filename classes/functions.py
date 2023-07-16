def parse_date(d):
    d2 = d[6:8] + "/" + d[4:6] + "/" + d[0:4]
    return (d2)

def get_nodes(path):
    pass

def xml_to_xlsx_filename(filename):
    parts = filename.split("T")
    part0 = parts[0]
    parts = part0.split("-")
    part1 = parts[1]
    excel_filename = "CDS updates " + part1[0:4] + "-" + part1[4:6] + "-" + part1[6:] + ".xlsx"
    return (excel_filename)


def get_measurement_unit(s):
    if s == "ASV":
        return "% vol"
    if s == "NAR":
        return "item"
    elif s == "CCT":
        return "ct/l"
    elif s == "CEN":
        return "100 p/st"
    elif s == "CTM":
        return "c/k"
    elif s == "DTN":
        return "100 kg"
    elif s == "GFI":
        return "gi F/S"
    elif s == "GRM":
        return "g"
    elif s == "HLT":
        return "hl"  # 2209009100
    elif s == "HMT":
        return "100 m"  # 3706909900
    elif s == "KGM":
        return "kg"
    elif s == "KLT":
        return "1,000 l"
    elif s == "KMA":
        return "kg met.am."
    elif s == "KNI":
        return "kg N"
    elif s == "KNS":
        return "kg H2O2"
    elif s == "KPH":
        return "kg KOH"
    elif s == "KPO":
        return "kg K2O"
    elif s == "KPP":
        return "kg P2O5"
    elif s == "KSD":
        return "kg 90 % sdt"
    elif s == "KSH":
        return "kg NaOH"
    elif s == "KUR":
        return "kg U"
    elif s == "LPA":
        return "l alc. 100%"
    elif s == "LTR":
        return "l"
    elif s == "MIL":
        return "1,000 items"
    elif s == "MTK":
        return "m2"
    elif s == "MTQ":
        return "m3"
    elif s == "MTR":
        return "m"
    elif s == "MWH":
        return "1,000 kWh"
    elif s == "NCL":
        return "ce/el"
    elif s == "NPR":
        return "pa"
    elif s == "TJO":
        return "TJ"
    elif s == "SPQ":
        return "SPQ"
    elif s == "TNE":
        return "tonne"  # 1005900020
        # return "1000 kg" # 1005900020
    else:
        return s

def get_qualifier(s):
    sQualDesc = ""
    if s == "A":
        sQualDesc = "tot alc"  # Total alcohol
    elif s == "C":
        sQualDesc = "1 000"  # Total alcohol
    elif s == "E":
        sQualDesc = "net drained wt"  # net of drained weight
    elif s == "G":
        sQualDesc = "gross"  # Gross
    elif s == "I":
        sQualDesc = "biodiesel"  # Gross
    elif s == "M":
        sQualDesc = "net dry"  # net of dry matter
    elif s == "P":
        sQualDesc = "lactic matter"  # of lactic matter
    elif s == "R":
        sQualDesc = "std qual"  # of the standard quality
    elif s == "S":
        sQualDesc = " raw sugar"
    elif s == "T":
        sQualDesc = "dry lactic matter"  # of dry lactic matter
    elif s == "X":
        sQualDesc = " hl"  # Hectolitre
    elif s == "Z":
        sQualDesc = "% sacchar."  # per 1% by weight of sucrose
    return sQualDesc
