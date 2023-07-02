import pyautogui
# Set the desired width and height






def screen():
    width = 1980
    height = 1080
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    # Resize the screenshot to the desired width and height
    screenshot = screenshot.resize((width, height))
    myScreenshot = pyautogui.screenshot()
    # Save the screenshot to a file
    screenshot.save("screenshot.png")