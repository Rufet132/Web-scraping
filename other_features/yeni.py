from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from csv import writer
from time import sleep
import time

from urllib3.util import wait

# İstifadəçidən marka adı alınır
car_brand = input("Axtarmaq istədiyiniz maşın markasını daxil edin (məs: BMW): ")

# WebDriver-i işə salırıq
driver = webdriver.Chrome()

# Turbo.az saytını açırıq
driver.get("https://turbo.az/")

# Saytın tam yüklənməsi üçün bir az gözləyək
time.sleep(3)

# Marka sahəsinə klik edirik
brand_dropdown = driver.find_element(By.CSS_SELECTOR, "div[data-id='q_make']")
brand_dropdown.click()
time.sleep(2)

# Açılan markalar arasında axtarış inputunu tapırıq
search_input = driver.find_element(By.CSS_SELECTOR, "input.tz-dropdown__search")
search_input.send_keys(car_brand)
search_input.click()


time.sleep(1.5)

# İstifadəçinin daxil etdiyi marka çıxır və ilk uyğun nəticəyə klik edirik
brand_items = driver.find_element(By.CSS_SELECTOR, "div.tz-dropdown__option")


submit_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name='commit'].main-search__btn"))
)
submit_btn.click()


key = True;
liste = []
with open('yeni1.csv', 'w') as scrapping_csv:
    csv_writer = writer(scrapping_csv)
    csv_writer.writerow(['Name','Price', 'Year', 'Motor', 'Distance','DateTime'])

    while (True):  # her sehifede butun masinlari tapmali oldugu ucun asagdaki melumatlar her sehife ucun tekrarlanmalidir deye bura while yaziriq
        trucks = driver.find_elements(By.CLASS_NAME, 'products-i__bottom')
        for truck in trucks:
            datetime = (truck.find_element(By.CLASS_NAME,'products-i__datetime').text).split(' ')
            if(datetime[1] == 'bugün'):
                name = truck.find_element(By.CLASS_NAME, 'products-i__name').text
                price = truck.find_element(By.CLASS_NAME, 'product-price').text
                other_elements_of_truck = truck.find_element(By.CLASS_NAME,'products-i__attributes').text  # Bunlar mesafe,muherrik ve ilin umumi halidir
                if(len(other_elements_of_truck.split(', ')) == 3):
                    year, motor, distance = other_elements_of_truck.split(', ')  # Bunlar ise tek tek
                    if other_elements_of_truck not in liste:
                        csv_writer.writerow([name, price, year, motor, distance, datetime[1]])
                        liste.append(other_elements_of_truck)

                else:
                    year,distance = other_elements_of_truck.split(', ')
                    csv_writer.writerow([name,price, year, "it isn't exist", distance, datetime[1]])
            else:
                key=False
        if(key==False):
            break

        try:
            next_button = driver.find_element(By.CLASS_NAME, 'next')
            next_button.click()
            sleep(5)  # from time import sleep den gelir
        except:
            driver.quit()

# input=("Enter: ")
print("The program finished succesfully")
driver.quit()