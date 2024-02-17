from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
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

def Find_Elements(driver : webdriver.Chrome, by, value : str) -> list[WebElement]:
    while True:
        try:
            elements = driver.find_elements(by, value)
            if len(elements) > 0:
                break
        except:
            pass
        sleep(0.1)
    return elements

# Determine the number of prompt
numberPrompt = input('Please input the number of prompt : ')
prompts = []
for inputID in range(1, int(numberPrompt) + 1):
    prompt = input(f'Please input prompt{inputID} : ')
    prompts.append({f'prompt{inputID}' : prompt})

with open('prompt.json', 'w') as file:
    json.dump(prompts, file)

# Run Chrome driver.
# service = Service(executable_path="C:\chromedriver-win64\chromedriver.exe")
# options = Options()
# options.add_experimental_option("debuggerAddress", "127.0.0.1:9030")
# driver = webdriver.Chrome(service=service, options=options)
driver = webdriver.Chrome()
driver.maximize_window()
chat_url = 'https://huggingface.co/chat/'
driver.get(chat_url)
sleep(1)
print('Run driver')

# Click "Sign in with Hugging Face" button.
goToSignBar = Find_Element(driver, By.XPATH, '/html/body/div[2]/div/div/div/div/form/button')
driver.execute_script('arguments[0].click();', goToSignBar)
print('Click sign in')
sleep(1)

# Sign in.
emailBox = Find_Element(driver, By.NAME, 'username')
emailBox.send_keys('javidev2022@gmail.com')
sleep(0.5)
passwordBox = Find_Element(driver, By.NAME, 'password')
passwordBox.send_keys('kdlkwhrDFER45$')
loginButton = Find_Element(driver, By.XPATH, '/html/body/div[1]/main/div/section/form/div[2]/button')
driver.execute_script('arguments[0].click();', loginButton)
print('Success login')
sleep(1)

# Input text in textBox and Enter.
for i, element in enumerate(prompts, start = 1):
    sleep(2)
    enter_prompt = Find_Element(driver, By.TAG_NAME, 'textarea')
    enter_prompt.send_keys(element[f'prompt{i}'])
    sleep(1)
    enter_prompt.send_keys(Keys.ENTER)
    sleep(20)

# Save answers as jon file.
answers = driver.find_elements(By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div/div')
answer = []
for i in range(1, len(answers), 2):
    answer.append({f'answer {int((i - 1)/2 + 1)}' : answers[i].text})
with open('answer.json', 'w') as file:
    json.dump(answer, file)