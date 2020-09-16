from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass
import time
import logging
import tenacity
import PySimpleGUI as sg
import os


@dataclass
class WeTransfer:
    pass

    @staticmethod
    @tenacity.retry(stop=tenacity.stop_after_attempt(10))
    def upload_via_wetransfer(upload_filename):
        """
        Opens a selenium browser instance, navigates to wetransfer.
        Requires chrome webdriver to be installed on PATH.
        :return: Selenium webdriver instance
        """

        xpaths = {
            "agree": "//button[@class='button welcome__agree button--enabled']",
            "accept cookies": "//button[@class='button welcome__button welcome__button--accept button--enabled']",
            "toggle options": "//button[@class='transfer__toggle-options']",
            "receive link": "(//div[@class='radioinput__check'])[2]",
            "send transfer": "//button[@class='transfer__button']",
            "file input": "//input[@type='file']",
        }
        executable_path = os.getcwd() + '/chromedriver'
        driver = webdriver.Chrome(executable_path=executable_path)

        driver.get("https://wetransfer.com")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h2"))
        )
        driver.find_element_by_xpath(xpaths["agree"]).click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpaths["accept cookies"]))
        )
        driver.find_element_by_xpath(xpaths["accept cookies"]).click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths["toggle options"]))
        )
        driver.find_element_by_xpath(xpaths["toggle options"]).click()
        driver.find_element_by_xpath(xpaths["receive link"]).click()
        driver.find_element_by_xpath(xpaths["file input"]).send_keys(upload_filename)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths["send transfer"]))
        )
        driver.find_element_by_xpath(xpaths["send transfer"]).click()

        return driver

    @staticmethod
    def check_upload_status(driver):
        """
        Checks the page to see if data is still being transferred.
        :param: A Selenium webdriver instance in which an upload has already begun.
        :return: result, a list. Empty if the upload has failed, contains link if it succeeded.
        """
        logging.basicConfig(
            filename="WeTransfer Checker Logs.txt",
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
        )
        xpaths = {
            "upload status": "//p[contains(text(), 'uploaded')]",
            "final link": "//input[@class='transfer-link__url']",
        }

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpaths["upload status"]))
        )
        logging.info("[*] Upload commenced.")
        start_time = time.time()
        while True:
            if driver.find_elements_by_xpath(xpaths["upload status"]):
                original_upload_status = driver.find_element_by_xpath(
                    xpaths["upload status"]
                ).text
                time.sleep(30 - ((time.time()) - start_time) % 30)  # checks every 30s
                if driver.find_elements_by_xpath(xpaths["upload status"]):
                    after_5m_upload_status = driver.find_element_by_xpath(
                        xpaths["upload status"]
                    ).text
                    logging.info("[*] Checking upload status....")
                    if original_upload_status == after_5m_upload_status:
                        logging.info("[*] The upload has failed; restarting...")
                        result = []
                        driver.close()
                        break
                    logging.info(
                        "[*] Upload status is good, {}.".format(after_5m_upload_status)
                    )
            elif driver.find_elements_by_xpath(xpaths["final link"]):
                logging.info("[*] Upload successful, saving your link!")
                final_link = driver.find_element_by_xpath(xpaths["final link"])
                result = [final_link.get_attribute("value")]
                driver.close()
                break

        return result


def GUI():
    """
    A very simple gui to allow non-technical users to run this program.
    :return: None.
    """
    sg.theme("Dark Teal 7")

    layout = [
        [sg.Text("Choose your file paths!", font="HelveticaNeue 12")],
        [
            sg.Text(
                "Which file do you want to upload?",
                font="HelveticaNeue 12",
                size=(30, 1),
            ),
            sg.InputText(),
            sg.FileBrowse(),
        ],
        [
            sg.Text(
                "Where do you want to save the link?",
                font="HelveticaNeue 12",
                size=(30, 1),
            ),
            sg.InputText(),
            sg.FolderBrowse(),
        ],
        [sg.Submit(), sg.Cancel()],
    ]

    window = sg.Window("WeTransfer Checker", layout, font="HelveticaNeue 12")

    event, values = window.read()
    window.close()

    file_path, folder_path = values[0], values[1]

    if file_path and folder_path:
        while True:
            driver_instance = WeTransfer.upload_via_wetransfer(file_path)
            result_output = WeTransfer.check_upload_status(driver=driver_instance)
            if result_output:
                with open(folder_path + "/WeTransfer-link.txt", "w") as f:
                    f.write(result_output[0])
                break

    return None


if __name__ == "__main__":
    GUI()
