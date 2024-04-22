from selenium import webdriver
from selenium.common import NoSuchElementException
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

driver.get("https://uat.app.worklenz.com/auth")
driver.maximize_window()
doing_status_tasks_details = []
done_status_tasks_details = []


def main():
    login()
    project_tab()


def login():
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Email']"))).send_keys(
        "bsdcsd@v.com")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Password']"))).send_keys(
        "ceyDigital#00")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Log in']"))).click()


def project_tab():
    wait.until(
        EC.visibility_of_element_located((By.XPATH, "//strong[normalize-space()='Projects']"))).click()


def check_project_segment():
    segments = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-segmented-group")))
    segments_wait = WebDriverWait(segments, 10)
    all_segment = segments_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "label")))[0]
    all_segment_class_name = all_segment.get_attribute("class")
    if "item-selected" not in all_segment_class_name:
        all_segment.click()


def go_to_need_project_inside():
    t_body = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "tbody")))
    t_body_wait = WebDriverWait(t_body, 10)
    t_body_wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "tr")))[0].click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Board']"))).click()


def before_get_doing_status_tasks():  # before drag and drop get doing status tasks and store
    before_doing_status_tasks = {
        "status_name": "DOING_before_drag_drop",
        "tasks": []
    }
    board_wrapper = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "board-wrapper")))
    board_wrapper_wait = WebDriverWait(board_wrapper, 10)
    doing_status = board_wrapper_wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "board-column")))[1]
    doing_status_wait = WebDriverWait(doing_status, 10)
    tasks = doing_status_wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "task")))
    for task in tasks:
        task_wait = WebDriverWait(task, 10)
        task_name = task_wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "task-name-kanban"))).text
        before_doing_status_tasks["tasks"].append(task_name)
    doing_status_tasks_details.append(before_doing_status_tasks)
    return


def before_get_done_status_tasks():  # before drag and drop get done status tasks and store
    before_done_status_tasks = {
        "status_name": "DONE_before_drag_drop",
        "tasks": []
    }
    board_wrapper = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "board-wrapper")))
    board_wrapper_wait = WebDriverWait(board_wrapper, 10)
    doing_status = board_wrapper_wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "board-column")))[2]
    doing_status_wait = WebDriverWait(doing_status, 10)
    tasks = doing_status_wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "task")))
    for task in tasks:
        task_wait = WebDriverWait(task, 10)
        task_name = task_wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "task-name-kanban"))).text
        before_done_status_tasks["tasks"].append(task_name)
    done_status_tasks_details.append(before_done_status_tasks)
    return


def task_drag_and_drop():
    fromElement = ''
    board_wrapper = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "board-wrapper")))
    board_wrapper_wait = WebDriverWait(board_wrapper, 10)
    to_do_status = board_wrapper_wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "board-column")))[0]
    to_do_status_wait = WebDriverWait(to_do_status, 10)

    time.sleep(3)
    try:
        task = to_do_status.find_elements(By.CLASS_NAME, "task")[0]
        if task.is_displayed():
            fromElement = task
    except (NoSuchElementException, IndexError):
        add_task_btn = to_do_status_wait.until(
            EC.visibility_of_element_located((By.XPATH, "(//div[@class='column-footer'])[1]")))
        add_task_btn.click()
        enter_task_name = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter task name']")))
        enter_task_name.send_keys("testing_tasks", Keys.ENTER)
        fromElement = to_do_status_wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "task")))[0]

    board_wrapper = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "board-wrapper")))
    board_wrapper_wait = WebDriverWait(board_wrapper, 10)
    done_status = board_wrapper_wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "board-column")))[2]
    done_status_wait = WebDriverWait(done_status, 10)
    toElement = done_status_wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "tasks-container")))

    actions = ActionChains(driver)
    actions.click_and_hold(fromElement).move_to_element(toElement).release(toElement).perform()
    time.sleep(2)


def after_get_doing_status_tasks():  # after drag and drop get doing status tasks and store
    after_doing_status_tasks = {
        "status_name": "DOING_after_drag_drop",
        "tasks": []
    }
    board_wrapper = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "board-wrapper")))
    board_wrapper_wait = WebDriverWait(board_wrapper, 10)
    doing_status = board_wrapper_wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "board-column")))[1]
    doing_status_wait = WebDriverWait(doing_status, 10)
    tasks = doing_status_wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "task")))
    for task in tasks:
        task_wait = WebDriverWait(task, 10)
        task_name = task_wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "task-name-kanban"))).text
        after_doing_status_tasks["tasks"].append(task_name)
    doing_status_tasks_details.append(after_doing_status_tasks)
    return


def after_get_done_status_tasks():  # after drag and drop get done status tasks and store
    after_done_status_tasks = {
        "status_name": "DONE_after_drag_drop",
        "tasks": []
    }
    board_wrapper = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "board-wrapper")))
    board_wrapper_wait = WebDriverWait(board_wrapper, 10)
    doing_status = board_wrapper_wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "board-column")))[2]
    doing_status_wait = WebDriverWait(doing_status, 10)
    tasks = doing_status_wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "task")))
    for task in tasks:
        task_wait = WebDriverWait(task, 10)
        task_name = task_wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "task-name-kanban"))).text
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
