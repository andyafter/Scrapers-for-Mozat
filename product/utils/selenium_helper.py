from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumHelper(object):
    def get_elements_href_by_class_name_condition(self, web_url, class_condition):
        self.web_driver = webdriver.Chrome()
        assert type(class_condition) == str
        assert type(web_url) == str
        self.web_driver.get(web_url)
        try:
            elements = WebDriverWait(self.web_driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, class_condition))
            )
        except Exception as e:
            print e
        elements = self.web_driver.find_elements_by_class_name(class_condition)
        href_result = []
        for element in elements:
            href_result.append(element.get_attribute('href'))
        self.web_driver.close()
        return href_result

    def get_elements_attribute_by_x_path(self, web_url, xpath_to_element, attribute):
        self.web_driver = webdriver.Chrome()
        assert type(web_url) == str
        assert type(xpath_to_element) == str
        assert type(attribute) == str
        self.web_driver.get(web_url)
        try:
            elements = WebDriverWait(self.web_driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath_to_element))
            )
        except Exception as e:
            print e
        result = []
        for element in elements:
            result.append(element.get_attribute(attribute))
        self.web_driver.close()
        return result


    def get_elemetns_by_xpath_class_condition(self, web_url, xpath, class_condition):
        assert type(class_condition) == str
        assert type(web_url) == str
        self.web_driver.get(web_url)
        try:
            elements = WebDriverWait(self.web_driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, class_condition))
            )
        except Exception as e:
            print e
        elements = self.web_driver.find_elements_by_xpath(xpath)
        self.web_driver.close()
        return elements

    def get_href_attribute(self, elements):
        try:
            if type(elements) == list:
                result_list = []
                for element in elements:
                    print element.get_attribute('href')
                    result_list.append(element.get_attribute('href'))
                return result_list
            else:
                return elements.get_attribute('href')
        except Exception as e:
            print e
            return 'Error'

if __name__ == '__main__':
    selenium = SeleniumHelper()
    url = 'http://www.asos.com/women/dresses/cat/pgecategory.aspx?cid=8799&via=top#parentID=-1&pge=0&pgeSize=204&sort=-1'
    print selenium.get_elements_by_class_name_condition(url, 'productImageLink')
