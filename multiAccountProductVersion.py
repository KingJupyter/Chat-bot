from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from multiprocessing import Process
import json

def Find_Element(driver : webdriver.Chrome, by, value : str) -> WebElement:
    while True:
        try:
            element = driver.find_element(by, value)
            break
        except:
            pass
        sleep(0.1)
    return element

def input_prompt():
    for i in range(1, 21):
        # Determine the number of prompt
        numberPrompt = input('Please input the number of prompt : ')
        prompts = []
        for inputID in range(1, int(numberPrompt) + 1):
            prompt = input(f'Please input prompt{inputID} : ')
            prompts.append({f'prompt{inputID}' : prompt})

        with open(f'prompt-{i}.json', 'w') as file:
            json.dump(prompts, file)

def run_bot(driver_num, email, password):
    driver = webdriver.Chrome()
    chat_url = 'https://huggingface.co/chat/'
    driver.get(chat_url)
    sleep(1)

    # Click "Sign in with Hugging Face" button.
    goToSignBar = Find_Element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div/form/button')
    driver.execute_script('arguments[0].click();', goToSignBar)
    sleep(1)

    # Sign in.
    emailBox = Find_Element(driver, By.NAME, 'username')
    emailBox.send_keys(email)
    sleep(0.5)
    passwordBox = Find_Element(driver, By.NAME, 'password')
    passwordBox.send_keys(password)
    loginButton = Find_Element(driver, By.XPATH, '/html/body/div[1]/main/div/section/form/div[2]/button')
    driver.execute_script('arguments[0].click();', loginButton)
    sleep(1)

    with open(f'prompt-{driver_num}.json', 'r') as file:
        prompts = json.load(file)

    # Input text in textBox and Enter.
    for i, element in enumerate(prompts, start = 1):
        sleep(2)
        enter_prompt = Find_Element(driver, By.TAG_NAME, 'textarea')
        enter_prompt.send_keys(element[f'prompt{i}'])
        sleep(1)
        enter_prompt.send_keys(Keys.ENTER)
        print(f'Browser-{driver_num}, Prompt {element[f"prompt{i}"]}')
        sleep(60)

        # Save answers as a text file.
        answers = driver.find_elements(By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div/div')
        with open(f'answer_{driver_num}.txt', 'a') as file:
            file.write(f'{"-" * 5} Answer {i} {"-" * 5}\n\n')
            file.write(f'Prompt {i} : {element[f"prompt{i}"]}\n')
            file.write(f'Answer {i} : {answers[i * 2 - 1].text}\n\n')

    driver.quit()

if __name__ == '__main__':

    input_prompt()

    accounts = [
        {'email': 'dalmaciotelfair@gmail.com', 'password': 'lxoviatiuspiM1'},
        {'email': 'dalmakempinski@gmail.com', 'password': 'M11dn45jf7wx'},
        {'email': 'damarispastano@gmail.com', 'password': 'M1ttt92x1sjxvn'},
        {'email': 'damasodavenport@gmail.com', 'password': 'M18xeze0knldds'},
        {'email': 'dambergervicky@gmail.com', 'password': 'M1ei1xa0m59l82'},
        {'email': 'damiogilbert@gmail.com', 'password': 'M1ehbgith6e6wqlv'},
        {'email': 'damnneal813@gmail.com', 'password': 'M1gombqq1zel'},
        {'email': 'damoclesstratman@gmail.com', 'password': 'M1ncgfmxohw0b'},
        {'email': 'daniastoldt@gmail.com', 'password': '7M1j9n4wgtgddsd'},
        {'email': 'danielamiddents@gmail.com', 'password': 'M1626rqpigzgslaj'},
        {'email': 'daniellequinchia89@gmail.com', 'password': 'M1pjs8hh04ajbe'},
        {'email': 'darcivirtue58@gmail.com', 'password': 'M1y92ze3jb72wiq'},
        {'email': 'dariarosalind245@gmail.com', 'password': 'M1mrvv9obwss'},
        {'email': 'darrickscoobz@gmail.com', 'password': 'M1589lnuptgdsd'},
        {'email': 'dativaalexandre@gmail.com', 'password': 'M1lpk32tpm5cpe'},
        {'email': 'dauntstarr@gmail.com', 'password': 'M1hhg2m6gesasdff'},
        {'email': 'davionemoncus@gmail.com', 'password': 'M1pbhde37fju'},
        {'email': 'davorspalitto@gmail.com', 'password': 'M1j1vfvtw24kw1'},
        {'email': 'dawsonsatordi@gmail.com', 'password': 'M11ruoy3c6dsdf'},
        {'email': 'dayaniraphaneuf@gmail.com', 'password': 'M1j3ojre951r8z'}
    ]

    processes = []
    for i, account in enumerate(accounts):
        process = Process(target = run_bot, args = (i + 1, account["email"], account["password"]))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()