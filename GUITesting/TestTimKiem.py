import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("http://localhost:5000")

# Nhập từ khóa cần tìm
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "query"))
)
search_box.send_keys("Phone")
search_box.submit()

# Chờ kết quả tìm kiếm hiện ra
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-item")))

print("✅ Tìm kiếm hiển thị kết quả thành công!")

time.sleep(10)
driver.quit()