import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

json_file = 'scraped_json_format_data.json'
csv_data = []


def main():
    browser = webdriver.Firefox()
    file_name = create_csv_file()

    try:
        with open('amazon scraping data.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for data in reader:
                product_details_list = []
                product_list = []

                product_title = None
                image_url_link = None
                price = None
                asin = data[0]
                country = data[1]

                try:

                    browser.get(f'https://www.amazon.{country}/dp/{asin}')
                    time.sleep(3)

                except Exception as e:
                    print(f'https://www.amazon.{country}/dp/{asin} not available : {e}')
                    print(e)
                try:
                    browser.find_element(By.ID, 'sp-cc-accept').click()
                except Exception as e:
                    print(e)
                try:
                    image_url = browser.find_element(By.ID, 'landingImage')
                    image_url_link = image_url.get_attribute('src')

                except Exception as e:
                    print(e)
                try:
                    product_title = browser.find_element(By.ID, 'productTitle').text
                except Exception as e:
                    print(e)
                try:
                    try:
                        price = browser.find_element(By.XPATH, "//span[@class='a-color-base']").text
                    except Exception as e:
                        print(e)
                    try:
                        price = browser.find_element(By.XPATH,
                                                     "//span[@class='a-price aok-align-center "
                                                     "reinventPricePriceToPayMargin priceToPay']").text
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)
                try:
                    product_lists = browser.find_elements(By.XPATH,
                                                          "//div[@id='detailBullets_feature_div']/ul/li/span/span")

                    for product_list_item in product_lists:
                        product_details_list.append(product_list_item.text)
                except Exception as e:
                    print(e)

                product_list = [product_title, image_url_link, price, product_details_list]

                with open(file_name, 'a') as file:
                    writer = csv.writer(file)
                    writer.writerow(product_list)
                    csv_data.append(product_list)

                with  open(json_file, 'w') as file:
                    json.dump(csv_data, file, indent=4)

    except Exception as error:
        print(error)


def create_csv_file():
    '''This function is used for create csv file by considering datetime'''
    try:
        # Here we use datetime module which used to found unique number for our csv file name
        current_time_span = datetime.now().strftime("%f")
        # we store in file name variable and use f string to use datetime microseconds
        file_name = f"Amazon Product Details {current_time_span}.csv"
        # This header list used to display in csv heading for column head name
        header = ['Product Title', 'Product Image URL', 'Price of the Product', 'Product Details']
        with open(file_name, 'w') as file:
            # here we use open function to open and write our file
            writer = csv.writer(file)
            # here we write our csv file
            writer.writerow(header)
            # here we add header first row
        return file_name
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
