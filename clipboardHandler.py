import time

import pyperclip

def check_clipboard():
    previous_content = ''

    while True:
        current_content = pyperclip.paste()

        # If content has changed, print it
        if current_content != previous_content:
            print("Clipboard content changed:", current_content)
            previous_content = current_content

        # Sleep for some time before checking again
        time.sleep(0.2)  # You can adjust the sleep duration as needed


if __name__ == '__main__':
    check_clipboard()
