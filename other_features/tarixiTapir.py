from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import date,timedelta
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from time import sleep  # Bu onu bildirirki bezen ola biler ki, bizde cox sehife olsun ve onlarin her birinden melumati ceke bilmesin bu zaman
# sleep den istifade ede bilerik.Lakin hal hazirda dartqilar az oldugundan bize sleep lazim olmayada bilerdi,amma tez tez sorgu gondermeyek deye qosmaliyiq
from csv import writer

secim = input("Tarix daxil edin(gün.ay.il): ")
liste = []
# WebManagerle driveri acdim,cunki 134 cu versiyani tapmadim
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://turbo.az/autos?q%5Bsort%5D=&q%5Bmake%5D%5B%5D=&q%5Bmodel%5D%5B%5D=&q%5Bused%5D=&q%5Bregion%5D%5B%5D=&q%5Bprice_from%5D=&q%5Bprice_to%5D=&q%5Bcurrency%5D=azn&q%5Bloan%5D=0&q%5Bbarter%5D=0&q%5Bcategory%5D%5B%5D=&q%5Bcategory%5D%5B%5D=16&q%5Byear_from%5D=&q%5Byear_to%5D=&q%5Bcolor%5D%5B%5D=&q%5Bfuel_type%5D%5B%5D=&q%5Bgear%5D%5B%5D=&q%5Btransmission%5D%5B%5D=&q%5Bengine_volume_from%5D=&q%5Bengine_volume_to%5D=&q%5Bpower_from%5D=&q%5Bpower_to%5D=&q%5Bmileage_from%5D=&q%5Bmileage_to%5D=&q%5Bonly_shops%5D=&q%5Bprior_owners_count%5D%5B%5D=&q%5Bseats_count%5D%5B%5D=&q%5Bmarket%5D%5B%5D=&q%5Bcrashed%5D=1&q%5Bpainted%5D=1&q%5Bfor_spare_parts%5D=0&q%5Bavailability_status%5D=")
submit_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name='commit'].main-search__btn"))
)
submit_btn.click()
#key = True;

with open('webScraping.csv', 'w', newline="", encoding="utf-8") as scrapping_csv:
    csv_writer = writer(scrapping_csv)
    csv_writer.writerow(['Name','Price', 'Year', 'Motor', 'Distance','DateTime'])

    while (True):  # her sehifede butun masinlari tapmali oldugu ucun asagdaki melumatlar her sehife ucun tekrarlanmalidir deye bura while yaziriq
        trucks = driver.find_elements(By.CLASS_NAME, 'products-i__bottom')
        for truck in trucks:
            datetime = (truck.find_element(By.CLASS_NAME,'products-i__datetime').text).split(' ')
            datetime_1 = ""
            if(datetime[1] == "bugün"):
                now = date.today()
                datetime[1] = now.strftime("%d.%m.%Y")
                k = [datetime[1][i] for i in range(2, len(datetime[1]))]
                datetime_1 = str((int(datetime[1][0] + datetime[1][1]) - 1)) + "".join(k)
            elif(datetime[1] == "dünən"):
                now = date.today() - timedelta(days=1)
                datetime[1] = now.strftime("%d.%m.%Y")
                k= [datetime[1][i] for i in range(2, len(datetime[1]))]
                datetime_1 = str((int(datetime[1][0] + datetime[1][1]) - 1)) + "".join(k)
            else:
                k = [datetime[1][i] for i in range(2, len(datetime[1]))]
                datetime_1 = str((int(datetime[1][0] + datetime[1][1]) - 1)) + "".join(k)

            if(secim == datetime[1]):
                name = truck.find_element(By.CLASS_NAME, 'products-i__name').text
                price = truck.find_element(By.CLASS_NAME, 'product-price').text
                other_elements_of_truck = truck.find_element(By.CLASS_NAME,'products-i__attributes').text  # Bunlar mesafe,muherrik ve ilin umumi halidir
                if (len(other_elements_of_truck.split(', ')) == 3):
                    year, motor, distance = other_elements_of_truck.split(', ')  # Bunlar ise tek tek
                    if other_elements_of_truck not in liste:
                        csv_writer.writerow([name, price, year, motor, distance, date.today()])
                        liste.append(other_elements_of_truck)
                    #print(name,price,year,motor,distance,datetime[1])
                else:
                    year, distance = other_elements_of_truck.split(', ')
                    csv_writer.writerow([name, price, year, "it isn't exist", distance, date.today()])

            '''else:
                if(datetime[1] == datetime_1):
                    key=False
        if(key==False):
            break '''

        try:
            next_button = driver.find_element(By.LINK_TEXT, 'Növbəti')
            next_button.click()
            sleep(5)  # from time import sleep den gelir
        except:
            driver.quit()

# input=("Enter: ")
print("The program finished succesfully")
driver.quit()