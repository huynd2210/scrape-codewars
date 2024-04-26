import subprocess

def run_program(max_attempts):
    attempts = 0
    while attempts < max_attempts:
        try:
            # Replace 'python your_program.py' with the command to run your program
            process = subprocess.Popen(['python', 'your_program.py'])
            process.wait()  # Wait for the program to finish
        except Exception as e:
            print("Error occurred:", e)
        finally:
            attempts += 1

if __name__ == "__main__":
    max_attempts = 5  # Change this to the desired number of attempts
    run_program(max_attempts)