
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import datetime
from datetime import timedelta
import time





#Attempts to direct to the new link. This will record the time before the link is chosen, and after the page is loaded to save the load time of the page
#Writes the wait time to a txt file, and writes error pages to a txt file





#Grabs a screenshot of the page and saves in .png format.
#You can specify the path for saving the screenshots by assigning the value to toggles['png_folder']. 
#Use '\\' for the folder path to correct the escape sequence
def png_screenshot(url, driver, toggles):
	S = lambda X: driver.execute_script('return document.body.parentNode.scroll’+X) driver.set_window_size(S(‘width’), S(‘height')
	driver.find_element(By .TAG_NAME, "body").screenshot(f"{toggles['png_folder']}{url[37:]}.png")

#This will open the links sent to it, and test for an error page
#In toggles['txt_folder'] you can determine the path for saving the text files
#When a link contains an error message, it will:
# 		print the attributes of the element it was in
#		save the html output of the page {url[37:]}_error.txt
# 		call png_screenshot to take a screen shot of the page
#		write logs from the console to the error_pages.txt document
#if the link does not contain an error message:
#		print the time it took to load the page
#		if toggles['gather_load_time'] == True, then it will save the load times to a file
#		if toggles['error_page_only'] == False, then it will save console logs to a file 
#				(depending on which toggle options have been set to True)

def open_link(url, driver, toggles):

	past = datetime.now()
	driver.get(url)
	present = datetime.now()
	ttl = present-past
	if ("ErrorException" in driver.page_source) or ("Error" in driver.page_source):
		print(f"{url[37:]} has failed us")
		print(driver.find_element(By.TAG_NAME, "a").get_attribute('innerHTML'))
		print(driver.find_element(By.TAG_NAME, "a").get_attribute('outerHTML'))
		#print(dir(driver.find_element(By.TAG_NAME, "a")))
		#print(vars(driver.find_element(By.TAG_NAME, "a")))		
		failures[url] = "error"
		with open(f"{toggles['txt_folder']}{url[37:]}_error.txt", "a", encoding="utf-8") as f:
			f.write(f"{url} \n\n")
			f.write(driver.find_element(By.XPATH, "/html/body").text)
			f.write("\n\n\n\n")	

		write_console_log(driver, f"{toggles['txt_folder']}{url[37:]}_error.txt", toggles)
		png_screenshot(url, driver, toggles)

	else:
		print(f"{url[37:]} is a success. Time To Load {timedelta.total_seconds(ttl)} seconds")
	#driver.get(url)
		if toggles['gather_load_time'] == True:
			with open(f"{toggles['txt_folder']}success_data.txt", "a", encoding="utf-8") as f:
				f.write(f"{url} \n\tLOAD TIME: {timedelta.total_seconds(ttl)} seconds\n")
		if toggles['error_page_only'] == False:		
			write_console_log(driver, f"{toggles['txt_folder']}success_data.txt", toggles)
'''


'''
#This is the function called to write the console logs to a text file
#The toggle option set in toggles{} will determine which logs will be written
#It begins the entry with "LOG DATA BEGINNING" and ends with "LOG DATA END", to make the beginning and end more easily searchable

def write_console_log(driver, doc, toggles):
	with open(doc, "a") as f:
		for line in driver.get_log('browser'):
			f.write("LOG DATA BEGINNING")
			#print(line)
			for key in line:
				if (toggles['all_console']):
					f.write(f"{line}\n")
				elif (toggles['anything_other_than_info']):
					if line['level'].lower() != 'info':	
						f.write(f"{line}\n")
				else:
					if toggles['error']:
						if line['level'].lower() == 'error':	
							f.write(f"{line}\n")
					if toggles['warn']: 
						if line['level'].lower() == 'warn':	
							f.write(f"{line}\n")
					if toggles['fatal']:
						if line['level'].lower() == 'fatal':	
							f.write(f"{line}\n")	
					if toggles['info']:
						if line['level'].lower() == 'info':	
							f.write(f"{line}\n")

			f.write("LOG DATA END")


#This will test iterate through the links present in the list Links[]
#if a page fails to load for any reason, like an error with the url, the try/except statements will prevent the script from crashing
#Sometimes elements in the list are not URL's at all. 
#		In this case, the if statements "if url == None:" and "if "http" not in url:" are meant to catch them


def test_all_links(driver, toggles, position = 1):

	failures = {}
	x=1
	links = driver.find_elements(By.TAG_NAME, "a")
	#print(links)


	for link in links:

		print(f"Progress: {round((x/len(links)*100), 2)}%")

		try:
			url =  link.get_attribute("href")
		except Exception as e:
			print(driver.current_url)
			print(f"Exception: {e}")
			continue	
		print(url)
		if url == None:
			continue
		if "http" not in url:
			continue	

		driver.execute_script(f"window.open('');")
		driver.switch_to.window(driver.window_handles[1])

		try:
			open_link(url, driver, toggles)
		except:

			print(f"Unable to load page {url}")	
			failures[url] = "Unable to load page"
			with open(f"{toggles['txt_folder']}error_pages.txt", "a", encoding="utf-8") as f:
				f.write(f"{url} \n\nPAGE DID NOT LOAD\n\n")
				f.write(driver.find_element(By.XPATH, "/html/body").text)
				f.write("\n\n\n\n")	
			png_screenshot(url, driver, toggles)	





		if (toggles['secondary_links'] == True):

			secondary_links = driver.find_elements(By.TAG_NAME, "a")

			for secondary_link in secondary_links:
				try:
					secondary_url =  secondary_link.get_attribute("href")					
				except Exception as e:
					print(driver.current_url)
					print(f"Exception: {e}")
					continue
				print(secondary_url)
				if secondary_url == None:
					continue
				if "http" not in secondary_url:
					continue	
				driver.execute_script(f"window.open('');")
				driver.switch_to.window(driver.window_handles[2])

				try:
					open_link(secondary_url, driver, toggles)
				except:
		
					print(f"Unable to load page {secondary_url}")
					print(f"Link found on {url}")	
					failures[secondary_url] = "Unable to load page"
					with open(f"{toggles['txt_folder']}{secondary_url[37:]}error.txt", "a", encoding="utf-8") as f:
						f.write(f"{secondary_url} \n\nPAGE DID NOT LOAD\n\n")
						f.write(driver.find_element(By.XPATH, "/html/body").text)
						f.write("\n\n\n\n")	
					png_screenshot(secondary_url, driver, toggles)	
		

				driver.close()
				driver.switch_to.window(driver.window_handles[1])
				#print(driver.window_handles)



		driver.close()
		driver.switch_to.window(driver.window_handles[0])		

		x+=1
		if (toggles['debug_script'] == True) and x >= 3:
			break

	return failures

#this is meant to log into the initial login page
	
def login(driver, un, ps):

	user_name = driver.find_element(By.NAME, "username")
	password = driver.find_element(By.NAME, "password")
	sign_in = driver.find_element(By.NAME, "sign-in")

	user_name.send_keys(un)
	password.send_keys(ps)
	sign_in.click()			



def main():
	
#the toggles keys 'error', 'fatal', 'warn', 'anything_other_than_info', 'info', and 'all_console' will set with console logs will be written
#		if 'info' = True, or if 'error', 'fatal', or 'warn' have been set to False, then 'anything_other_than_info' will be set to False
#				this prevents 'anything_other_than_info' from grabbing different logs than requested,
#				because it is called first in the if statements in write_console_log()
#

	toggles = {'error':True, 'fatal':True, 'warn':True,'anything_other_than_info':True, 
	'info':False, 'all_console': False, 'error_page_only': True, 'debug_script': False, 
	'gather_load_time': False, 'png_folder': 'screenshots\\', 'txt_folder': 'logs\\',
	'secondary_links': True}

	if not (toggles['error'] and toggles['fatal'] and toggles['warn']) or toggles['info']:
		toggles['anything_other_than_info'] = False

	d = DesiredCapabilities.EDGE
	d['ms:loggingPrefs'] = { 'browser':'ALL' }
	
	options = webdriver.EdgeOptions()

	options.add_argument('--headless')
	driver = webdriver.Edge(options = options)
	edge_options = EdgeOptions()
	edge_options.use_chromium = True
	edge_options.binary_location = R"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
	edge_options.set_capability("ms:edgeOptions",d)
	
	driver = webdriver.Edge(capabilities=d)

	driver.set_page_load_timeout(30)
	
	driver.get("https://<website>")

	login(driver, "<username>", "<password>")



	#Checks all links on a webpage to see if they will be route to an error page
	#Any link that routes to an error page will append that error to a test document.
	failures = test_all_links(driver, toggles)
	print(f"Failures: \n{failures}")

	driver.close()

if __name__ == '__main__':
	main()
