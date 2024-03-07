import pyautogui
import pygetwindow as gw
from AppOpener import open, close
import argparse
import datetime
import sys, os, time
from apscheduler.schedulers.background import BackgroundScheduler
import logging

# Constants
CHAT_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "Img", "Chat")
BUTTON_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "Img", "Button")
STATUS_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "Img", "Status")

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def start_script(start_time, step):
    # Run find_window_by_title at start_time and every step hours
    logger.info(f"Start time: {start_time}")
    logger.info(f"Step time: {step}")
    
    # Get current time
    current_time = datetime.datetime.now()
    logger.info(f"Current time: {current_time}")

    # If start time is passed, add step hours to start time
    if start_time < current_time:
        start_time = start_time + datetime.timedelta(hours=step)
        logger.info(f"Start time: {start_time}")

    # Else, run the program
    else:
        logger.info(f"Start time: {start_time}")

    # Run find_window_by_title at start_time and every step hours
    def log_next_claim_time():
        next_claim_time = start_time + datetime.timedelta(hours=step)
        logger.info(f"Next claim time: {next_claim_time}")
        print(f"Next claim time: {next_claim_time}")

    logger.info(f"Running find_window_by_title at {start_time} and every {step} hours")
    sched = BackgroundScheduler()
    sched.add_job(find_window_by_title, args=["TelegramDesktop"], trigger='interval', hours=step, start_date=start_time.replace(year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day))
    sched.add_job(log_next_claim_time, trigger='interval', hours=step, start_date=start_time.replace(year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day))
    sched.start()
    
    print("AutoClaim.py is running...")
    print("Press Ctrl+C to exit.")
    print("Start Claim at: ", start_time)

    try:
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        sched.shutdown()

def save_screenshot_window(title):
    try:
        # Get the first window that matches the title
        window = gw.getWindowsWithTitle(title)[0]  
        logger.info(f"Window found: {window.title}")
        
        # Bring the window to the front
        window.activate()  
        time.sleep(0.5)
        
        # Take a screenshot of the window
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        screenshot.save(f"{title}.png")
        
    except:
        logger.info(f"No window with title {title} found.")

def find_window_by_title(title):
    try:
        # Get the first window that matches the title
        window = gw.getWindowsWithTitle(title)
        
        if len(window) == 0:
            raise Exception("No window found.")
        else:
            for w in window:
                logger.info(f"Window found: {w.title}")
                w.activate()
                time.sleep(0.5)
                start_claim()
                w.minimize()
                
    except:
        logger.info(f"No window with title {title} found.")
        
        # Open Telegram
        logger.info("Opening Telegram...")
        open_telegram()
        
        # Call again
        find_window_by_title(title)
    
def open_telegram():
    open("Telegram")
    time.sleep(3)
    
    # Click near chat
    chat_path = os.path.join(CHAT_IMAGE_PATH, "NearChat.png")
    click_button_by_image(chat_path)
    time.sleep(0.5)
    
    # Click open Hot app
    hot_app_path = os.path.join(CHAT_IMAGE_PATH, "ClaimNow.png")
    click_button_by_image(hot_app_path)
    time.sleep(0.5)
    
    # Click Ok
    ok_path = os.path.join(CHAT_IMAGE_PATH, "Ok.png")
    click_button_by_image(ok_path)
    
    time.sleep(3)
    
def start_claim():
    can_return = True
    
    while can_return:
        # Click return
        return_path = return_path = os.path.join(BUTTON_IMAGE_PATH, "ButtonReturn.png")
        if click_button_by_image(return_path) == False:
            can_return = False
        time.sleep(0.5)
    
    # Click Storage
    storage_path = os.path.join(BUTTON_IMAGE_PATH, "ButtonStorage.png")
    click_button_by_image(storage_path)
    time.sleep(0.5)
    
    # Click Claim button
    active_path = os.path.join(BUTTON_IMAGE_PATH, "ButtonClaimActive.png")
    if click_button_by_image(active_path):
        time.sleep(0.5)
        check_button_state()
    else:
        logger.info("Can't Claim now.")  

def click_button_by_image(image):
    try:
        # Find the button
        button_location = pyautogui.locateOnScreen(image, confidence=0.9)
        logger.info(f"Button found at: {button_location}")
        time.sleep(0.5)
        
        # Click center of the button
        pyautogui.click(button_location.left + button_location.width / 2, button_location.top + button_location.height / 2)
        
        return True
        
    except:
        logger.info(f"Button not found.")
        return False
        
def check_button_state():
    logger.info("Checking button state...")
    status = True
    deactive_path = os.path.join(BUTTON_IMAGE_PATH, "ButtonClaimDeactive.png")
    
    while status:
        try:
            deactive_location = pyautogui.locateOnScreen(deactive_path, confidence=0.9)
            logger.info("Claim successful.")
            time.sleep(0.5)
            status = False
            
        except:
            logger.info("Checking no gas notification...")
            check_no_gas_notification()
    
    return status

def check_no_gas_notification():
    status = True
    notification_path = os.path.join(STATUS_IMAGE_PATH, "NoGas.png")
    
    while status:
        try:
            notification_location = pyautogui.locateOnScreen(notification_path, confidence=0.9)
            logger.info(f"No Gas notification found at: {notification_location}")
            
            # Move to center of the notification
            pyautogui.moveTo(notification_location.left + notification_location.width / 2, notification_location.top + notification_location.height / 2)
            time.sleep(0.5)
            
            # Sroll down
            pyautogui.scroll(-100)
            time.sleep(0.5)
            
            # Click the button claim with hot
            logger.info("Clicking claim with hot...")
            claim_hot_path = os.path.join(BUTTON_IMAGE_PATH, "ButtonClaimWithHot.png")
            click_button_by_image(claim_hot_path)
            time.sleep(0.5)
            status = False
            
        except:
            time.sleep(2)
            status = False
    
def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description='Auto Claim Hot Telegram.')
    parser.add_argument('--start', type=str, help='Start time. (HH:MM)')
    parser.add_argument('--step', type=int, help='Step time. (HH)')
    args = parser.parse_args()
    
    # Get arguments
    start = args.start
    step = args.step
    
    # Check arguments
    if start is None:
        logger.error("Start time is required.")
        sys.exit()
        
    if step is None:
        logger.error("Step time is required.")
        sys.exit()
    
    # Convert start time to datetime with current date
    current_date = datetime.datetime.now().date()
    start_time = datetime.datetime.strptime(start, "%H:%M").replace(year=current_date.year, month=current_date.month, day=current_date.day)
    
    logger.info("AutoClaim.py is running...")
    
    start_script(start_time, step)

if __name__ == '__main__':
    main()
