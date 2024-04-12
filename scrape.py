import subprocess
import re
import time

import autopep8
from lxml import html
from lxml import etree
from io import StringIO
from bs4 import BeautifulSoup
import pyautogui
import pyperclip

def getFirstChildHtmlInsideXpath(html, xpath):
    # Parse the HTML string
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    # Find the first matching element using XPath
    first_child = tree.xpath(xpath + '/child::*')[0]

    # Serialize the first child element to HTML
    return etree.tostring(first_child, encoding='unicode')


def replace_multiple_whitespaces_with_single_whitespace(string):
    return re.sub(r'[ ]+', ' ', string)

def format_python_code(code):
    formatted_code = autopep8.fix_code(code)
    return formatted_code
def strip_html(html):
    # Parse the HTML string
    soup = BeautifulSoup(html, 'html.parser')

    # Extract text from the parsed HTML
    text = soup.get_text(separator=' ')

    return text.strip()

#
# xpath = "/html/body/div[1]/div[1]/main/div[4]/div[4]/div[2]/div/div/div[1]/pre"
#
#
#
# childInsideXpath = getFirstChildHtmlInsideXpath(html, xpath)
# content = format_python_code(replace_multiple_whitespaces_with_single_whitespace(strip_html(childInsideXpath)).strip())
#
# print(content)
#



def open_chrome(url):
    # Command to open Google Chrome with the specified URL
    command = f"start chrome {url}"

    # Execute the command
    subprocess.Popen(command, shell=True)


def scrapeSolution(url):
    open_chrome(url)
    time.sleep(5)
    pyautogui.press("f12")
    time.sleep(1)
    consoleButtonPosition = (1400, 130)
    pyautogui.click(consoleButtonPosition)
    time.sleep(1)

    javascriptCode = """
    function writeToClipboard(text) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
    }
    const html = document.documentElement.outerHTML;

    writeToClipboard(html);
    """

    pyperclip.copy(javascriptCode)

    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)
    html = pyperclip.paste()
    xpath = "/html/body/div[1]/div[1]/main/div[4]/div[4]/div[2]/div/div/div[1]/pre"
    childInsideXpath = getFirstChildHtmlInsideXpath(html, xpath)
    content = format_python_code(
        replace_multiple_whitespaces_with_single_whitespace(strip_html(childInsideXpath)).strip())

    print(content)


if __name__ == '__main__':
    url = "https://www.codewars.com/kata/57d29ccda56edb4187000052/solutions/python"
    scrapeSolution(url)
