import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tkinter import Tk, Label, Text, Entry, Button

#from webdriver_manager.chrome import ChromeDriverManager

# Auto Install Driver
#driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

chrome_options = Options()
#chrome_options.add_argument("--headless")

service = ChromeService(executable_path="R:\Documents - Storage Disk\PythonProjects\Selenium\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)



now = datetime.now() # current date and time


def CalculateFeesByVIN(vin, price, month, day, year, county, city, zipcode):
    # Opening Website
    driver.get("https://www.dmv.ca.gov/wasapp/FeeCalculatorWeb/usedVehicleForm.do")

    # Vehicle Information
    NoLicensePlate = '//*[@id="FeeRequestForm"]/fieldset[1]/div/ul/li[2]/label'
    VINinput = '//*[@id="vehicleVinFull"]'

    # Purchase Information
    PurchaseButton = '// *[ @ id = "acquiredFrom"] / li[1] / label'
    Price = '//*[@id="purchasePrice"]'

    DateM = Select(driver.find_element(By.XPATH, '//*[@id="purchaseMonth"]'))
    #DateM = '//*[@id="purchaseMonth"]'

    DateD = '//*[@id="purchaseDay"]'
    DateY = '//*[@id="purchaseYear"]'

    # Home Address Information
    County = Select(driver.find_element(By.XPATH, '//*[@id="countyCode"]'))
    #County = '//*[@id="countyCode"]'

    City = Select(driver.find_element(By.XPATH, '//*[@id="cityNameSelect"]'))
    #City = '//*[@id="cityNameSelect"]'

    Zipcode = '//*[@id="zipCode"]'

    Calculate = '//*[@id="FeeRequestForm"]/div/button[1]'

    TestForTitle = '// *[ @ id = "main"] / div[2] / div[2] / h2'

    try:
        elem = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, TestForTitle))
        )
        #print("Waiting to Load")
    finally:
        pass

    driver.find_element(By.XPATH, NoLicensePlate).click()
    driver.find_element(By.XPATH, VINinput).send_keys(vin)

    driver.find_element(By.XPATH, PurchaseButton).click()
    driver.find_element(By.XPATH, Price).send_keys(price)
    DateM.select_by_visible_text(month)
    driver.find_element(By.XPATH, DateD).send_keys(day)
    driver.find_element(By.XPATH, DateY).send_keys(year)

    County.select_by_visible_text(county)
    City.select_by_visible_text(city)
    driver.find_element(By.XPATH, Zipcode).send_keys(zipcode)

    driver.find_element(By.XPATH, Calculate).click()




    try:
        elem = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, TestForTitle))
        )
        #print("Waiting to Load")
    finally:
        pass

    Registration_Fee_Path = '// *[ @ id = "main"] / div[2] / div[2] / fieldset[1] / div / dl / dd[3]'

    try:
        Registration_Fee_Value = driver.find_element(By.XPATH, Registration_Fee_Path).text
        print(Registration_Fee_Value)
        return Registration_Fee_Value
    except:
        pass

    DangerAlertPathSalvage = '//*[@id = "main"]/div[2]/div[2]/fieldset/div/div[3]'
    DangerAlertPathPlate = '//*[@id="main"]/div[2]/div[2]/fieldset/div/div[2]'
    UnableToDetmermine = '//*[@id = "main"]/div[2]/div[2]/fieldset/div/div'

    try:
        DangerAlertPathSalvage = driver.find_element(By.XPATH, DangerAlertPathSalvage).text
        print(DangerAlertPathSalvage)
        return DangerAlertPathSalvage
    except:
        pass

    try:
        DangerAlertPathPlate = driver.find_element(By.XPATH, DangerAlertPathPlate).text
        print(DangerAlertPathPlate)
        return DangerAlertPathPlate
    except:
        pass

    try:
        UnableToDetmermine = driver.find_element(By.XPATH, UnableToDetmermine).text
        print(UnableToDetmermine)
        return UnableToDetmermine
    except:
        print("Failure Occurred")
        return -1

def ShowFees():
    vinUnproccessed = userVIN.get("1.0","end-1c")
    vins = vinUnproccessed.split("\n")
    #print(repr(vin))



    Label(root, text="Your Fees:").grid(row=2)
    blank = Text(root, width=47, height=20)
    blank.delete(0.0, "end-1c")



    #print('\t', CalculateFeesByVIN(vin, Price, Month, Day, Year, County, City, Zipcode), end=' ')
    for vin in vins:
        blank.insert("end-1c", "%s\n"%CalculateFeesByVIN(vin, Price, Month, Day, Year, County, City, Zipcode))

    blank.grid(row=2, column=1)
    print()


def close():
   root.destroy()
   root.quit()


# vin, price, month, day, year, county, city, zipcode
VIN = "1HGEJ8148TL064973"
Price = "1000"

Year = now.strftime("%Y")
Month = now.strftime("%B")
Day = now.strftime("%d")

County = "Los Angeles"
City = "Pasadena"
Zipcode = "91107"
#CalculateFeesByVIN(VIN, Price, Month, Day, Year, County, City, Zipcode)
#CalculateFeesByVIN("1HGCD7234RA052418", Price, Month, Day, Year, County, City, Zipcode)
#CalculateFeesByVIN("JTDKB20U587746660", Price, Month, Day, Year, County, City, Zipcode)



root = Tk()
root.iconbitmap("favicon.ico")
root.title('DMV Registration Fee Calculator - Ricky Ho')

root.geometry('600x800')

Label(root, text="Enter VIN(s):").grid(row=0)
#Label(root, text="Enter Random:").grid(row=1)


#userVIN = Entry(root)
userVIN = Text(root, width=20, height=20)
userVIN.grid(row=0, column=1)

#numcol = Entry(main)



Button(root, text='Quit', command=close).grid(row=4, column=0, pady=4)
Button(root, text='Calculate', command=ShowFees).grid(row=4, column=1, pady=4)

#w = Label(root, text="Hello, world!")
#w.pack()
root.mainloop()



#time.sleep(10)
driver.quit()