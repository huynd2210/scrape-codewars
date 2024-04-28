import json

import requests


def get_challenge_info(challenge_id_list):
    base_url = "https://www.codewars.com/api/v1/code-challenges/{}"

    challenge_info = []

    for challenge_id in challenge_id_list:
        url = base_url.format(challenge_id)
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            info = {
                "id": data["id"],
                "name": data["name"],
                "url": data["url"],
                "category": data["category"],
                "description": data["description"],
                "tags": data["tags"],
                "rank_name": data["rank"]["name"]
            }

            challenge_info.append(info)
        else:
            print("Failed to fetch data for challenge ID:", challenge_id)

    return challenge_info

def save_to_json(data, filename):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

def readTextFile(filename):
    with open(filename, 'r') as file:
        return file.read()


def readJson(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def split_list_and_save(lst, n, filename_prefix):
    # Calculate the size of each part
    part_size = len(lst) // n
    remainder = len(lst) % n

    # Split the list into n parts
    parts = [lst[i * part_size:(i + 1) * part_size] for i in range(n)]

    # Distribute the remainder elements
    for i in range(remainder):
        parts[i % n].append(lst[-(i + 1)])

    # Save each part into a file
    for i, part in enumerate(parts):
        filename = f"{filename_prefix}_{i}.txt"
        with open(filename, "w") as file:
            for item in part:
                file.write(str(item) + "\n")


# scrapedSolutions = readJson("huynd2210_scraped_solutions.json")
# num_parts = 4
# file_prefix = "part"
#
# split_list_and_save(list(scrapedSolutions.keys()), num_parts, file_prefix)


def doTheRequest(filename):
    rawString = readTextFile(filename)
    challengeIds = rawString.split()
    challengeInfo = get_challenge_info(challengeIds)

    save_to_json(challengeInfo, f'{filename}_challenge_info.json')


if __name__ == '__main__':

    doTheRequest("part_2.txt")


