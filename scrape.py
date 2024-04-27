import json
import subprocess
import re
import time

import autopep8
import requests
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
def readTextFile(filename):
    with open(filename, 'r') as file:
        return file.read()


def readJson(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def open_chrome(url):
    # Command to open Google Chrome with the specified URL
    command = f"start chrome {url}"

    # Execute the command
    subprocess.Popen(command, shell=True)


def scrapeSolutionsForAGivenList(ids):
    result = {}
    try:
        for id in ids:
            url = f"https://www.codewars.com/kata/{id}/solutions/python"
            solution = scrapeSolution(url)
            result[id] = solution
            time.sleep(0.2)
        return result
    except Exception as e:
        print(e)
        print("-" * 50)
        return result


def scrapeSolution(url):
    open_chrome(url)
    time.sleep(14)
    # Open the inspector
    pyautogui.press("f12")
    time.sleep(1.2)
    # Click on console
    consoleButtonPosition = (1400, 130)
    pyautogui.click(consoleButtonPosition)
    time.sleep(1.2)

    javascriptCode = """
    function writeToClipboard(text) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
    }

    function isElementExists(xpath) {
        var result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
        return result.singleNodeValue !== null;
    }
    function clickElementByXPath(xpath) {
        var element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (element) {
            element.click();
        } else {
            console.error("Element with XPath '" + xpath + "' not found.");
        }
    }

    function runScraper(){
        let unlockBtnXpath = "/html/body/div[1]/div[1]/main/div[4]/div[3]/div[2]/div/p[2]/a"
        if (isElementExists(unlockBtnXpath)){
            clickElementByXPath(unlockBtnXpath);
        }
        const html = document.documentElement.outerHTML;
    
        writeToClipboard(html);
    }
    runScraper()
    """

    pyperclip.copy(javascriptCode)
    # Paste the code
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    html = pyperclip.paste()

    if html == javascriptCode:
        time.sleep(1)
        html = pyperclip.paste()

    # print("pasted content: ", html)
    xpath = "/html/body/div[1]/div[1]/main/div[4]/div[4]/div[2]/div/div/div[1]/pre"

    childInsideXpath = getFirstChildHtmlInsideXpath(html, xpath)
    content = format_python_code(
        replace_multiple_whitespaces_with_single_whitespace(strip_html(childInsideXpath)).strip())

    print(content)
    # Close the tab
    pyautogui.hotkey('ctrl', 'w')
    return content


def check_if_python_supported(challenge_id):
    # Construct the API endpoint URL
    url = f"https://www.codewars.com/api/v1/code-challenges/{challenge_id}"

    try:
        # Send a GET request to the API endpoint
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()  # Convert the response to JSON format

        # Check if Python is in the list of supported languages
        if "python" in data.get("languages", []):
            return True
        else:
            return False

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return False


def unlockSolutionAndCopySolution(url, delay=6):
    open_chrome(url)
    time.sleep(delay)
    # Click on the unlock solution button using js
    # Open the inspector
    pyautogui.press("f12")
    time.sleep(1.2)
    # Click on console
    consoleButtonPosition = (1400, 130)
    pyautogui.click(consoleButtonPosition)
    time.sleep(1.2)

    unlockJsCode = """
    function clickElementByXPath(xpath) {
        var element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (element) {
            element.click();
        } else {
            console.error("Element with XPath '" + xpath + "' not found.");
        }
    }
    var unlockBtnXpath = "/html/body/div[1]/div[1]/main/div[4]/div[3]/div[2]/div/p[2]/a"
    clickElementByXPath(unlockBtnXpath);
    """

    pyperclip.copy(unlockJsCode)
    # Paste the code
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)

    copyJsCode = """
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

    pyperclip.copy(copyJsCode)
    # Paste the code
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    html = pyperclip.paste()

    if html == copyJsCode:
        time.sleep(1)
        html = pyperclip.paste()

    # print("pasted content: ", html)
    xpath = "/html/body/div[1]/div[1]/main/div[4]/div[4]/div[2]/div/div/div[1]/pre"

    childInsideXpath = getFirstChildHtmlInsideXpath(html, xpath)
    content = format_python_code(
        replace_multiple_whitespaces_with_single_whitespace(strip_html(childInsideXpath)).strip())

    print(content)
    # Close the tab
    pyautogui.hotkey('ctrl', 'w')
    return content


# Note that the pasted code will be in the clipboard
def copyAndPasteJsCode(jsCode):
    pyperclip.copy(jsCode)
    # Paste the code
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)


def getKataIdFromUrl(url):
    return url.split("/")[-1]


def scrapeUnfishedCodewarsProblemsWithoutIdList():
    baseUrl = "https://www.codewars.com/kata/search/my-languages?q=&r%5B%5D=-8&r%5B%5D=-7&r%5B%5D=-6&r%5B%5D=-5&xids=completed&beta=false&order_by=satisfaction_percent%20desc%2Ctotal_completed%20desc"
    open_chrome(baseUrl)
    time.sleep(5)

    clickOnFirstProblemJsCode = """
    function clickElementByXPath(xpath) {
        var element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (element) {
            element.click();
        } else {
            console.error("Element with XPath '" + xpath + "' not found.");
        }
    }  

    firstProblemXpath = "/html/body/div[1]/div[1]/main/section[2]/div[2]/div[3]/div/div[1]/div[1]/a"
    clickElementByXPath(firstProblemXpath)
    """

    # Open the inspector
    pyautogui.press("f12")
    time.sleep(1.2)
    # Click on console
    consoleButtonPosition = (1400, 130)
    pyautogui.click(consoleButtonPosition)
    time.sleep(1.2)
    copyAndPasteJsCode(clickOnFirstProblemJsCode)
    time.sleep(1)

    getCurrentURLJsCode = """
    function writeToClipboard(text) {
           const textarea = document.createElement('textarea');
           textarea.value = text;
           document.body.appendChild(textarea);
           textarea.select();
           document.execCommand('copy');
           document.body.removeChild(textarea);
    }
    function getCurrentUrl(){
    // Get the current URL
        var currentUrl = window.location.href;

    // Print the current URL to the console
        console.log("Current URL:", currentUrl);
        writeToClipboard(currentUrl)
    }
    getCurrentUrl()
    """

    copyAndPasteJsCode(getCurrentURLJsCode)
    currentUrl = pyperclip.paste()
    print(currentUrl)

    kataId = getKataIdFromUrl(currentUrl)

    time.sleep(1)
    pyperclip.copy("")
    goToSolutionPageJsCode = f"window.location.href = '{currentUrl}/solutions/python`';"
    copyAndPasteJsCode(goToSolutionPageJsCode)
    time.sleep(1)

    unlockJsCode = """
        function clickElementByXPath(xpath) {
            var element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (element) {
                element.click();
            } else {
                console.error("Element with XPath '" + xpath + "' not found.");
            }
        }
        var unlockBtnXpath = "/html/body/div[1]/div[1]/main/div[4]/div[3]/div[2]/div/p[2]/a"
        clickElementByXPath(unlockBtnXpath);
        """

    copyAndPasteJsCode(unlockJsCode)
    time.sleep(1)

    copyJsCode = """
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
    copyAndPasteJsCode(copyJsCode)
    time.sleep(1)

    html = pyperclip.paste()

    if html == copyJsCode:
        time.sleep(1)
        html = pyperclip.paste()

    # print("pasted content: ", html)
    xpath = "/html/body/div[1]/div[1]/main/div[4]/div[4]/div[2]/div/div/div[1]/pre"

    childInsideXpath = getFirstChildHtmlInsideXpath(html, xpath)
    content = format_python_code(
        replace_multiple_whitespaces_with_single_whitespace(strip_html(childInsideXpath)).strip())

    print(content)
    # Close the tab
    pyautogui.hotkey('ctrl', 'w')
    return kataId, content


def scrapeLikeANormalPerson():
    scrapedSolutions = readJson("huynd2210_scraped_solutions.json")
    result = {}

    numberOfProblemsToScrape = 10

    try:
        for _ in range(numberOfProblemsToScrape):
            id, solution = scrapeUnfishedCodewarsProblemsWithoutIdList()
            result[id] = solution
            time.sleep(0.2)
        scrapedSolutions.update(result)
        with open("huynd2210_scraped_solutions.json", 'w') as file:
            json.dump(scrapedSolutions, file)
    except Exception as e:
        print(e)
        print("-" * 50)
        scrapedSolutions.update(result)
        with open("huynd2210_scraped_solutions.json", 'w') as file:
            json.dump(scrapedSolutions, file)

def isKataApproved(challenge_id_or_slug):
    # API endpoint URL
    api_url = f"https://www.codewars.com/api/v1/code-challenges/{challenge_id_or_slug}"

    # Send GET request
    response = requests.get(api_url)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()

        # Check if the challenge is approved
        if 'approvedBy' in data:
            return True
        else:
            return False
    else:
        raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")

def scrapeUnfinishedCodewarProblems(username="Voile"):
    # unscrapedCodeChallenges = readJson(f"{username}_completed_challenges.json")
    unscrapedCodeChallenges = readJson(f"{username}_completed_challenges_approved_wip_python_supported.json")
    scrapedSolutions = readJson("huynd2210_scraped_solutions.json")
    result = {}

    scrapedSolutionsIds = set(scrapedSolutions.keys())

    print("Amount of unscraped challenges: ", len(unscrapedCodeChallenges))
    print("Amount of scraped solutions: ", len(scrapedSolutionsIds))

    maxProblemsToScrape = 200
    i = 0

    scrapedThisSession = set()
    pythonNotSupportedThisSession = set()
    problemNotApprovedThisSession = set()

    try:
        for id in unscrapedCodeChallenges:
            isKataPythonSupported = check_if_python_supported(id)
            isProblemApproved = isKataApproved(id)

            if i > maxProblemsToScrape:
                break
            # if isKataPythonSupported and id not in scrapedSolutionsIds and isProblemApproved:
            #     url = f"https://www.codewars.com/kata/{id}/solutions/python"
            #     solution = unlockSolutionAndCopySolution(url)
            #     result[id] = solution
            #     time.sleep(0.2)
            #     i += 1

            if not isKataPythonSupported:
                pythonNotSupportedThisSession.add(id)

            if not isProblemApproved:
                problemNotApprovedThisSession.add(id)

            if isKataPythonSupported and id not in scrapedSolutionsIds and isProblemApproved:
                url = f"https://www.codewars.com/kata/{id}/solutions/python"
                solution = unlockSolutionAndCopySolution(url)
                result[id] = solution
                time.sleep(0.2)
                i += 1
                scrapedThisSession.add(id)


        scrapedSolutions.update(result)

        unscrapedCodeChallenges = {key: value for key, value in unscrapedCodeChallenges.items() if key not in scrapedThisSession}
        unscrapedCodeChallenges = {key: value for key, value in unscrapedCodeChallenges.items() if key not in pythonNotSupportedThisSession}
        unscrapedCodeChallenges = {key: value for key, value in unscrapedCodeChallenges.items() if key not in problemNotApprovedThisSession}

        with open(f"{username}_completed_challenges_approved_wip_python_supported.json", 'w') as file:
            json.dump(unscrapedCodeChallenges, file)
        with open("huynd2210_scraped_solutions.json", 'w') as file:
            json.dump(scrapedSolutions, file)


    except Exception as e:
        print(e)
        print("-" * 50)
        scrapedSolutions.update(result)
        unscrapedCodeChallenges = {key: value for key, value in unscrapedCodeChallenges.items() if key not in scrapedThisSession}
        unscrapedCodeChallenges = {key: value for key, value in unscrapedCodeChallenges.items() if key not in pythonNotSupportedThisSession}
        unscrapedCodeChallenges = {key: value for key, value in unscrapedCodeChallenges.items() if key not in problemNotApprovedThisSession}

        with open(f"{username}_completed_challenges_approved_wip_python_supported.json", 'w') as file:
            json.dump(unscrapedCodeChallenges, file)
        with open("huynd2210_scraped_solutions.json", 'w') as file:
            json.dump(scrapedSolutions, file)



def removeScrapedProblemsFromMainList():
    username = "Voile"
    unscrapedCodeChallenges = readJson(f"{username}_completed_challenges.json")
    scrapedSolutions = readJson("huynd2210_scraped_solutions.json")

    newDict = {}

    for id in unscrapedCodeChallenges:
        if id not in scrapedSolutions:
            # del unscrapedCodeChallenges[id]
            newDict[id] = unscrapedCodeChallenges[id]

    with open(f"{username}_completed_challenges.json", 'w') as file:
        json.dump(newDict, file)


def removeUnapprovedKata():
    global result_dict
    username = "Voile"
    unscrapedCodeChallenges = readJson(f"{username}_completed_challenges.json")
    unapprovedKata = {}
    i = 0
    try:
        for id in unscrapedCodeChallenges:
            if i > 900:
                break
            if not isKataApproved(id):
                unapprovedKata[id] = unscrapedCodeChallenges[id]
            i+=1
            print(i)

        result_dict = {key: value for key, value in unscrapedCodeChallenges.items() if key not in unapprovedKata}
        with open(f"{username}_completed_challenges_approved_wip.json", 'w') as file:
            json.dump(result_dict, file)

        print("Amount of challenges left: ", len(result_dict))
    except:
        print("Error")
        with open(f"{username}_completed_challenges_approved_wip.json", 'w') as file:
            json.dump(result_dict, file)

        print("Amount of challenges left: ", len(result_dict))

        raise Exception("Error")

def removeNonPythonChallenges():
    challenges = readJson("Voile_completed_challenges_approved_wip.json")
    i = 0
    newDict = {}
    global finalDict
    try:
        for id in challenges:
            if i > 200:
                break
            if check_if_python_supported(id):
                newDict[id] = challenges[id]
            i+=1
            print(i)

        finalDict = {key: value for key, value in challenges.items() if key not in newDict}
        with open("Voile_completed_challenges_approved_wip_python_supported.json", 'w') as file:
            json.dump(finalDict, file)
    except Exception as e:
        with open("Voile_completed_challenges_approved_wip_python_supported.json", 'w') as file:
            json.dump(finalDict, file)
        raise e

def removeScrapedFromApproved():
    challenges = readJson("Voile_completed_challenges_approved_wip.json")
    scrapedSolution = readJson("huynd2210_scraped_solutions.json")

    newDict = {}
    for id in challenges:
        if id not in scrapedSolution:
            newDict[id] = challenges[id]

    with open("Voile_completed_challenges_approved_wip_unscraped.json", 'w') as file:
        json.dump(newDict, file)



def retry(func, n_attempts, delay=0):
    """
    Retry a function for a specified number of attempts if it fails.

    Args:
        func (callable): The function to be retried.
        n_attempts (int): Number of attempts to retry the function.
        delay (int, optional): Delay in seconds between retries.

    Returns:
        The result of the function if successful, otherwise None.
    """
    for _ in range(n_attempts):
        try:
            result = func()
            return result  # If successful, return the result
        except Exception as e:
            print(f"Attempt failed: {e}")
            if delay > 0:
                time.sleep(delay)
    return None


if __name__ == '__main__':


    unscrapedCodeChallenges = readJson(f"Voile_completed_challenges_approved_wip_python_supported.json")
    scrapedSolutions = readJson("huynd2210_scraped_solutions.json")

    print("Amount of unscraped challenges: ", len(unscrapedCodeChallenges))

    for id in scrapedSolutions:
        if id in unscrapedCodeChallenges:
            del unscrapedCodeChallenges[id]
    with open(f"Voile_completed_challenges_approved_wip_python_supported.json", 'w') as file:
        json.dump(unscrapedCodeChallenges, file)
    print("Amount of challenges left: ", len(unscrapedCodeChallenges))


    # url = "https://www.codewars.com/kata/57d29ccda56edb4187000052/solutions/python"
    # url = "https://www.codewars.com/kata/52efefcbcdf57161d4000091/solutions/python"
    # scrapeSolution(url)
    #
    # username = "huynd2210"
    # codeChallenges = readTextFile(f"{username}_python_supported_challenges.txt").split("\n")
    # ids = list(codeChallenges)
    # scrapedSolutions = readJson("huynd2210_scraped_solutions.json")
    # scrapedSolutionsIds = list(scrapedSolutions.keys())
    # remainingIds = list(set(ids) - set(scrapedSolutionsIds))
    # remainingIds.remove('')
    #
    # print(ids)
    # result = scrapeSolutionsForAGivenList(remainingIds)
    # result.update(scrapedSolutions)
    # with open("huynd2210_scraped_solutions.json", 'w') as file:
    #     json.dump(result, file)

    # scrapeUnfinishedCodewarProblems()
    # retry(scrapeUnfinishedCodewarProblems, 5, 90)


    # removeScrapedProblemsFromMainList()

    # removeUnapprovedKata()
    # removeNonPythonChallenges()
    # removeScrapedFromApproved()

    # id, solution = scrapeUnfishedCodewarsProblemsWithoutIdList()

    # print(id)
    # print(solution)
    # scrapeLikeANormalPerson()