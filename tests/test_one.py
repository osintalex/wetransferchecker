import pytest
from app import WeTransfer
import os

# Run this with command python -m pytest tests/test_one.py
# Chromedriver executable must be in project root directory for this to work

upload_file = os.getcwd() + '/tests/test-file.txt'

driver_instance = WeTransfer.upload_via_wetransfer(upload_filename=upload_file)
link_save_test = WeTransfer.check_upload_status(driver=driver_instance)

def test_output_after_upload():
    assert (len(link_save_test[0]) != 0), "List should not be empty after successful upload"
