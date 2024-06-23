from selenium import webdriver
from time import sleep

from selenium.webdriver.common.by import By

URL = "http://127.0.0.1:8000/"


def login(driver):
    driver.get(URL + "login/")
    data = {
        'username': 'mandarinka',
        'password': '0347469_Wasd'
    }
    driver.find_element(By.NAME, 'username').send_keys(data['username'])
    driver.find_element(By.NAME, 'password').send_keys(data['password'])
    driver.find_element(By.NAME, 'submit').click()


def test_registration():
    driver = webdriver.Firefox()
    data = {
        'username': 'test',
        'first_name': 'test',
        'last_name': 'test',
        'password': 'test_1234'
    }
    driver.get(URL + 'register/')
    username = driver.find_element(By.NAME, 'username')
    username.send_keys(data['username'])
    password = driver.find_element(By.NAME, 'password1')
    password.send_keys(data['password'])
    password = driver.find_element(By.NAME, 'password2')
    password.send_keys(data['password'])
    first_name = driver.find_element(By.NAME, 'first_name')
    first_name.send_keys(data['first_name'])
    last_name = driver.find_element(By.NAME, 'last_name')
    last_name.send_keys(data['last_name'])
    submit = driver.find_element(By.NAME, 'submit')
    submit.click()
    driver.close()


def test_login():
    driver = webdriver.Firefox()
    data = {
        'username': 'mandarinka',
        'password': '0347469_Wasd'
    }
    driver.get(URL + "login/")
    driver.find_element(By.NAME, 'username').send_keys(data['username'])
    driver.find_element(By.NAME, 'password').send_keys(data['password'])
    driver.find_element(By.NAME, 'submit').click()
    if not (driver.current_url == URL + "profile/"):
        driver.close()
        raise Exception('Failed to url')
    if data['username'] in driver.find_element(By.ID, 'username').text:
        driver.find_element(By.NAME, 'logout').click()
        driver.close()
    else:
        raise Exception("Failed to test")


def test_car_create():
    driver = webdriver.Firefox()
    login(driver)

    data = {
        'mark': 'test',
        'model': 'test',
        'price': 100,
        'date_of_issue': '2001-01-01',
        'description': 'test',
    }
    driver.get(URL + "car/create/")

    for key, value in data.items():
        driver.find_element(By.ID, key).send_keys(value)

    sleep(2)
    driver.find_element(By.ID, 'accept').click()

    driver.close()


def test_car_settings():
    driver = webdriver.Firefox()
    login(driver)
    data_search = '59fa7a1b-b9c0-4859-b726-32e987d99691'
    data_update = {
        'mark': 'test2',
        'model': 'test2',
        'price': 1000,
        'date_of_issue': '2002-01-01',
        'description': 'test2',
    }

    driver.find_element(By.ID, 'view_cars').click()
    for val in driver.find_elements(By.NAME, 'car_id'):
        if val.get_attribute('value') == data_search:
            val.click()
            break
    driver.find_element(By.NAME, 'car_id').click()

    for key, value in data_update.items():
        driver.find_element(By.ID, key).send_keys(value)

    driver.find_element(By.NAME, 'car_id').click()

    driver.close()


def test_replenishment():
    driver = webdriver.Firefox()
    money = 100

    login(driver)

    driver.get(URL + "profile/")
    start_money = driver.find_element(By.ID, 'money').text.replace(',', '.').replace(' ', '')
    start_money = str((float(start_money) + money))
    start_money = start_money.replace('.', ',')

    driver.find_element(By.ID, 'replenishment').click()

    driver.find_element(By.ID, 'repl').send_keys(str(money))
    driver.find_element(By.NAME, 'accept').click()

    if not (start_money in driver.find_element(By.ID, 'money').text):
        driver.close()
        raise Exception("Failed to test")
    driver.close()


def test_car_create_with_sr():
    driver = webdriver.Firefox()
    login(driver)
    data = {
        'mark': 'test3',
        'model': 'test3',
        'price': 100,
        'date_of_issue': '2001-01-01',
        'description': 'test3',
    }
    data_sr = {
        'type_work0': 'test',
        'price0': '100',
        'the_date_of_the0': '2001-01-01',
    }

    driver.get(URL + "car/create/")

    for key, value in data.items():
        driver.find_element(By.ID, key).send_keys(value)

    driver.find_element(By.NAME, 'add_sr').click()

    for key, value in data_sr.items():
        driver.find_element(By.NAME, key).send_keys(value)

    driver.find_element(By.ID, 'accept').click()

    driver.close()


def test_register_page():
    driver = webdriver.Firefox()
    driver.get(URL + 'register/')
    data = ['username', 'first_name', 'last_name', 'password1', 'password2']
    for value in data:
        driver.find_element(By.NAME, value)

    driver.find_element(By.ID, 'login').click()
    if not (driver.current_url == URL + 'accounts/login/?next=/login/'):
        driver.close()
        raise Exception('Failed to url')
    driver.close()


def test_login_page():
    driver = webdriver.Firefox()
    driver.get(URL + 'login/')
    data = ['username', 'password']
    for value in data:
        driver.find_element(By.NAME, value)

    driver.find_element(By.ID, 'register').click()
    if not (driver.current_url == URL + 'register/'):
        driver.close()
        raise Exception('Failed to url')
    driver.close()


def test_profile_page():
    driver = webdriver.Firefox()
    login(driver)

    data_url = [
        ('replenishment', 'profile', 'replenishment'),
        ('create_car', 'car', 'create'),
        ('view_cars', 'car', 'views'),
        ('settings', 'profile', 'settings')
    ]
    data_id = ['username', 'name', 'money']
    data_id.extend([value[0] for value in data_url])
    data_name = ['logout']
    for value in data_id:
        driver.find_element(By.ID, value)

    for value in data_name:
        driver.find_element(By.NAME, value)

    for value in data_url:
        driver.find_element(By.ID, value[0]).click()
        if not (driver.current_url == URL + f'{value[1]}/{value[2]}/'):
            driver.close()
            raise Exception('Failed to url')
        driver.find_element(By.ID, 'profile').click()
        if not (driver.current_url == URL + 'profile/'):
            driver.close()
            raise Exception('Failed to url')

    for value in data_name:
        driver.find_element(By.NAME, value).click()
        if not (driver.current_url == URL + 'accounts/login/?next=/login/'):
            driver.close()
            raise Exception('Failed to url')
    driver.close()


def test_car_create_page():
    driver = webdriver.Firefox()
    login(driver)

    driver.find_element(By.ID, 'create_car').click()
    data_car = ['model', 'mark', 'date_of_issue', 'price', 'description', 'for_sale']
    data_but = ['add_sr', 'del_sr']
    data_sr = ['sr_type_work', 'sr_the_date_of_the', 'sr_price']

    for value in data_car:
        driver.find_element(By.NAME, value)

    for value in data_but:
        driver.find_element(By.NAME, value)

    driver.find_element(By.NAME, data_but[0]).click()
    for value in data_sr:
        driver.find_element(By.ID, value)

    driver.close()


def test_view_cars_page():
    driver = webdriver.Firefox()
    login(driver)

    driver.find_element(By.ID, 'view_cars').click()
    data = ['car_id']
    for value in data:
        driver.find_element(By.NAME, value)

    driver.find_element(By.NAME, 'car_id').click()
    if not (driver.current_url == URL + 'car/view-car/'):
        driver.close()
        raise Exception('Failed to url')

    driver.close()


def test_car_delete_page():
    driver = webdriver.Firefox()
    login(driver)
    driver.get(URL + "car/delete/")
    msg = 'Вы не указали машину!'
    if driver.find_element(By.ID, 'msg').text != msg:
        driver.close()
        raise Exception('Failed to url')
    driver.close()


def test_car_view_page():
    driver = webdriver.Firefox()
    login(driver)
    driver.get(URL + "car/views/")
    driver.find_element(By.NAME, 'car_id').click()
    data = ['mark', 'model', 'date_of_issue', 'price', 'description']
    for value in data:
        driver.find_element(By.ID, value)

    driver.close()


def test_car_settings_page():
    driver = webdriver.Firefox()
    login(driver)
    data = ['mark', 'model', 'date_of_issue', 'price', 'description']
    driver.get(URL + "car/views/")
    driver.find_element(By.NAME, 'car_id').click()
    driver.find_element(By.NAME, 'car_id').click()
    for value in data:
        driver.find_element(By.ID, value)

    driver.close()


def test_replenishment_page():
    driver = webdriver.Firefox()
    login(driver)
    driver.get(URL + "profile/replenishment/")
    driver.find_element(By.ID, 'repl')
    driver.close()
