from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
import csv

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

driver.get("https://worklenz.com/auth")
driver.maximize_window()
doing_status_tasks_details = []
done_status_tasks_details = []


def main():
    login()
    project_tab()


def login():
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Email']"))).send_keys(
        "coyonic318@hupoi.com")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Password']"))).send_keys(
        "Test@12345")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Log in']"))).click()
    time.sleep(10)


def project_tab():
    wait.until(
        EC.visibility_of_element_located((By.XPATH, "//strong[normalize-space()='Projects']"))).click()
    time.sleep(10)


def check_project_segment():
    segments = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-segmented-group")))
    all_segment = segments.find_elements(By.TAG_NAME, "label")[0]
    all_segment_class_name = all_segment.get_attribute("class")
    if "item-selected" not in all_segment_class_name:
        all_segment.click()


def go_to_need_project_inside():
    t_body = driver.find_element(By.TAG_NAME, "tbody")
    t_body.find_elements(By.TAG_NAME, "tr")[0].click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Board']"))).click()
    time.sleep(6)


def before_get_doing_status_tasks():  # before drag and drop get doing status tasks and store
    before_doing_status_tasks = {
        "status_name": "DOING_before_drag_drop",
        "tasks": []
    }
    board_wrapper = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "board-wrapper")))
    doing_status = board_wrapper.find_elements(By.CLASS_NAME, "board-column")[1]
    tasks = doing_status.find_elements(By.CLASS_NAME, "task")
    for task in tasks:
        task_name = task.find_element(By.CLASS_NAME, "task-name-kanban").text
        before_doing_status_tasks["tasks"].append(task_name)
    doing_status_tasks_details.append(before_doing_status_tasks)
    time.sleep(1)
    return


def before_get_done_status_tasks():  # before drag and drop get done status tasks and store
    before_done_status_tasks = {
        "status_name": "DONE_before_drag_drop",
        "tasks": []
    }
    board_wrapper = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "board-wrapper")))
    doing_status = board_wrapper.find_elements(By.CLASS_NAME, "board-column")[2]
    tasks = doing_status.find_elements(By.CLASS_NAME, "task")
    for task in tasks:
        task_name = task.find_element(By.CLASS_NAME, "task-name-kanban").text
        before_done_status_tasks["tasks"].append(task_name)
    done_status_tasks_details.append(before_done_status_tasks)
    time.sleep(1)
    return


def task_drag_and_drop():
    board_wrapper = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "board-wrapper")))
    doing_status = board_wrapper.find_elements(By.CLASS_NAME, "board-column")[1]
    fromElement = doing_status.find_elements(By.CLASS_NAME, "task")[0]

    board_wrapper = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "board-wrapper")))
    done_status = board_wrapper.find_elements(By.CLASS_NAME, "board-column")[2]
    toElement = done_status.find_element(By.CLASS_NAME, "tasks-container")

    actions = ActionChains(driver)
    actions.click_and_hold(fromElement).move_to_element(toElement).release(toElement).perform()


def after_get_doing_status_tasks():  # after drag and drop get doing status tasks and store
    after_doing_status_tasks = {
        "status_name": "DOING_after_drag_drop",
        "tasks": []
    }
    board_wrapper = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "board-wrapper")))
    doing_status = board_wrapper.find_elements(By.CLASS_NAME, "board-column")[1]
    tasks = doing_status.find_elements(By.CLASS_NAME, "task")
    for task in tasks:
        task_name = task.find_element(By.CLASS_NAME, "task-name-kanban").text
        after_doing_status_tasks["tasks"].append(task_name)
    doing_status_tasks_details.append(after_doing_status_tasks)
    return


def after_get_done_status_tasks():  # after drag and drop get done status tasks and store
    after_done_status_tasks = {
        "status_name": "DONE_after_drag_drop",
        "tasks": []
    }
    board_wrapper = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "board-wrapper")))
    doing_status = board_wrapper.find_elements(By.CLASS_NAME, "board-column")[2]
    tasks = doing_status.find_elements(By.CLASS_NAME, "task")
    for task in tasks:
        task_name = task.find_element(By.CLASS_NAME, "task-name-kanban").text
        after_done_status_tasks["tasks"].append(task_name)
    done_status_tasks_details.append(after_done_status_tasks)
    return


def write_doing_CSV1():
    file_path1 = 'check_DOING_tasks_count.csv'

    with open(file_path1, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=doing_status_tasks_details[0].keys())
        writer.writeheader()
        writer.writerows(doing_status_tasks_details)
        writer.writerow({})


def write_doing_CSV2():
    file_path2 = 'check_DONE_tasks_count.csv'
    with open(file_path2, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=done_status_tasks_details[0].keys())
        writer.writeheader()
        writer.writerows(done_status_tasks_details)
        writer.writerow({})


main()
check_project_segment()
go_to_need_project_inside()
before_get_doing_status_tasks()
before_get_done_status_tasks()
task_drag_and_drop()
after_get_doing_status_tasks()
after_get_done_status_tasks()
write_doing_CSV1()
write_doing_CSV2()

