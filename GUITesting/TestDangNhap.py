import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login_test(email, password, expect_success):
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/login")

    try:
        # Nhập email và mật khẩu
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        ).send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submitLogin']").click()

        # Đợi một chút để xử lý đăng nhập
        time.sleep(2)

        if expect_success:
            # ✅ Chờ cho URL chuyển hướng đến trang chính
            WebDriverWait(driver, 10).until(EC.url_contains("/"))
            print("Đăng nhập thành công!")
        else:
            # ❌ Nếu vẫn ở trang /login, tức là đăng nhập thất bại
            if "/login" in driver.current_url:
                print("Đăng nhập thất bại!")
            else:
                print("Lỗi không xác định!")

    except Exception as e:
        print("Lỗi xảy ra:", str(e))
    finally:
        time.sleep(2)
        driver.quit()


# Test case 1: Thành công
login_test("shine04112004@gmail.com", "1", expect_success=True)

# Test case 2: Thất bại
login_test("aaaa@gmail.com", "1", expect_success=False)
