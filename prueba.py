from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver import ActionChains
#import time
#from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO


driver = webdriver.Chrome()
driver.maximize_window()

driver.get('http://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias')
#driver.get('http://selenium-python.readthedocs.io/locating-elements.html') 

driver.implicitly_wait(5)



driver.switch_to_frame("leftFrame")

#temp = driver.find_elements_by_tag_name('img')

driver.find_element_by_name('search1').send_keys(10082112362)

#driver.find_element_by_css_selector('.form-button').click()


img = driver.find_element_by_tag_name('img')
loc = img.location
size = img.size

#temp = driver.find_element_by_css_selector('.form-button')
"""
actions = ActionChains(driver)
actions.move_to_element(img).context_click().send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
actions.move_to_element(img).context_click(img).perform()
actions.move_to_element(img).context_click(img).perform()
time.sleep(0.5)
"""
#actions.move_to_element(img).send_keys(Keys.ENTER)
#'Temporales/screenshot.png'

png = driver.get_screenshot_as_png()
temp = Image.open(BytesIO(png))

left = loc['x']
top = loc['y']
right = loc['x'] + size['width']
bottom = loc['y'] + size['height']

temp = temp.crop((left, top, right, bottom)) 
temp.save('screenshot.png') 


#url = 'http://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias'
"""
x = loc.x
y = loc.y 
print(x)
"""
print( loc)
print( size)




#actions = ActionChains(driver)

#keyboard.tap_key("LEFT")

#driver.find_element_by_css_selector('.form-button').send_keys(Keys.ENTER)


#actions.perform()



#print(loc)

#browser.close()


 
