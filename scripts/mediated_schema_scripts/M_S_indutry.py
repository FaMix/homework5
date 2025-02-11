import os
import uuid
import pandas as pd

import run as r


DEFAULT_INDUSTRY_MAPPINGS = {
    'IndustryName': ("Industry", "Area of Activity", "categories", "company_business"),
    'Sector': ("Sector", "market", "type", "nature_of_business")
}

DEFAULT_INDUSTRY_TARGET_COLUMNS = ("IndustryName", "Sector")