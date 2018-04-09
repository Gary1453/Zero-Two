from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
from pykeyboard import PyKeyboard

keyboard = PyKeyboard()
driver = webdriver.Chrome()
driver.get('http://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias')
#driver.get('http://selenium-python.readthedocs.io/locating-elements.html') 

driver.implicitly_wait(5)



driver.switch_to_frame("leftFrame")

#temp = driver.find_elements_by_tag_name('img')

driver.find_element_by_name('search1').send_keys(10082112362)

#driver.find_element_by_css_selector('.form-button').click()


img = driver.find_element_by_tag_name('img')
#loc = img.location
#temp = driver.find_element_by_css_selector('.form-button')

actions = ActionChains(driver)
#actions.move_to_element(img).context_click().send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
actions.move_to_element(img).context_click(img).perform()
time.sleep(0.5)

actions.move_to_element(img).send_keys(Keys.ENTER)

#actions = ActionChains(driver)

#keyboard.tap_key("LEFT")

#driver.find_element_by_css_selector('.form-button').send_keys(Keys.ENTER)


#actions.perform()



#print(loc)

#browser.close()


 
