import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Khởi tạo trình điều khiển (driver) cho Chrome
driver = webdriver.Chrome()

# Mở trang đăng nhập
driver.get("http://localhost:5000/login")

# ✅ Đợi tối đa 10 giây để phần tử có name="username" xuất hiện, sau đó điền "admin"
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "email"))
).send_keys("shine04112004@gmail.com")

# Tìm ô mật khẩu theo name="password" và điền "admin"
driver.find_element(By.NAME, "password").send_keys("1")

# Tìm nút submit và click (gửi biểu mẫu đăng nhập)
driver.find_element(By.CSS_SELECTOR, "button[type='submitLogin']").click()

# ✅ Đợi tối đa 10 giây để URL thay đổi và chứa "/dashboard" (điều kiện sau khi đăng nhập thành công)
WebDriverWait(driver, 10).until(
    EC.url_contains("/")
)

# ✅ Kiểm tra xem từ "Trang chủ" có xuất hiện trong mã nguồn HTML của trang sau khi đăng nhập không
assert "Trang chủ" in driver.page_source

# Nếu không có lỗi xảy ra đến đây, in ra thông báo đăng nhập thành công
print("✅ Đăng nhập thành công!")

time.sleep(5)  # Hiện website trong 5s

# Đóng trình duyệt
driver.quit()
