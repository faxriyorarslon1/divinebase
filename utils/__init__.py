import random
from pathlib import Path
from os.path import join as join_path

# print(random.randint(10000, 99999))

BASE_URL = Path(__file__).parent.parent
# print(BASE_URL)
EXCEL_PATH = join_path(BASE_URL, 'media', 'excel_utils')
HOSPITAL_EXCEL_PATH = join_path(BASE_URL, 'media', 'hospital')
