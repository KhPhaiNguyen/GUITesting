import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("http://localhost:5000/login")

# Đăng nhập
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys("shine04112004@gmail.com")
driver.find_element(By.NAME, "password").send_keys("1")
driver.find_element(By.CSS_SELECTOR, "button[type='submitLogin']").click()
WebDriverWait(driver, 10).until(EC.url_contains("/"))

# Chọn danh mục
driver.find_element(By.LINK_TEXT, "Laptop").click()

# Thêm sản phẩm vào giỏ hàng
add_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "add-to-cart"))
)
add_btn.click()

print("✅ Thêm sản phẩm vào giỏ hàng thành công!")

# Chuyển sang trang giỏ hàng
cart_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/cart']"))  # Tìm liên kết có href="/cart"
)
cart_link.click()

time.sleep(10)
driver.quit()