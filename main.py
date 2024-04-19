import json
import random
import time

import requests


def get_completed_challenges(username, page=0):
    url = f"https://www.codewars.com/api/v1/users/{username}/code-challenges/completed?page={page}"
    response = requests.get(url)

    if response.status_code == 200:
        completed_challenges = response.json()
        return completed_challenges
    else:
        print(f"Failed to retrieve completed challenges for user '{username}'. Status code: {response.status_code}")
        return None


def get_all_completed_challenges(username):
    all_challenges = {}

    page = 0
    while True:
        try:
            url = f"https://www.codewars.com/api/v1/users/{username}/code-challenges/completed?page={page}"
            response = requests.get(url)

            if response.status_code == 200:
                completed_challenges = response.json()
                # Extract IDs and names from the current page
                challenges_on_page = {challenge['id']: challenge['name'] for challenge in completed_challenges['data']}
                all_challenges.update(challenges_on_page)

                # Check if there are more pages to fetch
                if page + 1 < completed_challenges['totalPages']:
                    page += 1
                else:
                    break
            else:
                print(
                    f"Failed to retrieve completed challenges for user '{username}'. Status code: {response.status_code}")
                break
            print("Collected: ", len(all_challenges))
            print("Current page: ", page)
            print("Total pages: ", completed_challenges['totalPages'])
            print("----------------")
            time.sleep(random.uniform(0, 1))
        except Exception as e:
            print(f"Error occurred while fetching completed challenges: {e}")
            save_completed_challenges_to_file(all_challenges, "current_progress.json")
    return all_challenges

def save_completed_challenges_to_file(challenges_dict, filename):
    with open(filename, 'w') as file:
        json.dump(challenges_dict, file)

def readJson(filename):
    with open(filename, 'r') as file:
        return json.load(file)



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

def scrapeCodewarsProblems(username):
    filename = f"{username}_completed_challenges.json"

    all_completed_challenges = get_all_completed_challenges(username)
    print("All Completed Challenges:")
    for challenge_id, challenge_name in all_completed_challenges.items():
        print("ID:", challenge_id, "- Name:", challenge_name)

    # Save to file
    save_completed_challenges_to_file(all_completed_challenges, filename)
    print(f"Completed challenges saved to '{filename}'.")


if __name__ == '__main__':
    username = "Voile"
    pythonSupported = []
    try:
        # scrapeCodewarsProblems()

        codeChallenges = readJson(f"{username}_completed_challenges.json")
        i = 0
        for challenge_id, challenge_name in codeChallenges.items():
            if check_if_python_supported(challenge_id):
                pythonSupported.append(challenge_id)
            i += 1
            print("Done:", i)

        print(pythonSupported)
        with open(f"{username}_python_supported_challenges.txt", 'w') as file:
            for item in pythonSupported:
                file.write(str(item) + "\n")

        print("Amount of python supported challenges: ", len(pythonSupported))
    except Exception as e:
        print(e)
        with open(f"{username}_python_supported_challenges.txt", 'w') as file:
            for item in pythonSupported:
                file.write(str(item) + "\n")