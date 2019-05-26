import pandas as pd

from datetime import datetime

drop_columns = ["TypeOfIncident", "CalYear", "FinYear", "SpecialServiceType"]
column_renames = {
    "AnimalGroupParent": "animal",
    "DateTimeOfCall": "datetime",
    "IncidentNumber": "incident",
    "PumpCount": "pump_count",
    "PumpHoursTotal": "pump_hours",
    "HourlyNotionalCost(£)": "hourly_cost",
    "IncidentNotionalCost(£)": "total_cost",
    "FinalDescription": "description",
    "AnimalGroupParent": "animal",
    "PropertyType": "property",
    "PropertyCategory": "property_type",
    "OriginOfCall": "origin",
    "SpecialServiceTypeCategory": "service_type",
    "WardCode": "ward_code", "Ward": "ward",
    "BoroughCode": "borough_code", "Borough": "borough",
    "StnGroundName": "station",
    "PostcodeDistrict": "post_district",
    
}

def load_data(data_file):
    data = pd.read_csv(data_file, encoding="ISO-8859-1")
    
    # Parse DateTime
    data["DateTimeOfCall"] = pd.to_datetime(data["DateTimeOfCall"])
    
    # Drop useless columns
    data.drop(columns=drop_columns, inplace=True)
    
    # Rename coluns
    data.rename(columns=column_renames, inplace=True)
    
    # Cleaning
    data.replace("cat", "Cat", inplace=True)
    return data

