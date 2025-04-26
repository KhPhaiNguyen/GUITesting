import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

LOGIN_URL = "https://lms.neu.edu.vn/login/index.php"

@pytest.fixture(scope="module")
def driver():
    # Khởi tạo WebDriver (đảm bảo chromedriver hoặc webdriver-manager đã được cài)
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Bỏ comment nếu muốn chạy ẩn danh
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get(LOGIN_URL) # Đi đến trang login cụ thể

    # Chờ một element cơ bản (ví dụ: ô username) xuất hiện để chắc chắn trang đã tải
    try:
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "username"))
        )
        print("Trang đăng nhập đã tải thành công.")
    except TimeoutException:
        print("Lỗi: Trang đăng nhập tải quá lâu hoặc không tìm thấy ô username.")
        driver.quit()
        pytest.skip("Không thể tải trang đăng nhập, bỏ qua các test còn lại.")

    yield driver # Trả về driver cho các test functions sử dụng

    # Dọn dẹp sau khi tất cả test trong module chạy xong
    print("Đóng trình duyệt...")
    driver.quit()

# --- Test Cases ---

def test_website_load(driver: webdriver.Chrome):
    """Kiểm tra xem URL hiện tại có đúng là trang login không."""
    assert LOGIN_URL in driver.current_url
    print("PASS: Đã tải đúng URL trang đăng nhập.")

def test_page_title(driver: webdriver.Chrome):
    """Kiểm tra tiêu đề trang đăng nhập."""
    # Tiêu đề có thể thay đổi, kiểm tra một phần đặc trưng
    expected_title_part = "NEU - LEARNING MANAGEMENT SYSTEM: Log in to the site" # Phần tiêu đề thường thấy của Moodle login
    actual_title = driver.title
    assert expected_title_part in actual_title
    print(f"PASS: Tiêu đề trang '{actual_title}' chứa '{expected_title_part}'.")

def test_logo_displayed(driver: webdriver.Chrome):
    """Kiểm tra logo NEU có hiển thị không."""
    wait = WebDriverWait(driver, 10)
    # Thử tìm logo bằng class navbar-brand chứa thẻ img (phổ biến trong Moodle)
    # Hoặc thử lại alt text nếu bạn chắc chắn về nó: (By.CSS_SELECTOR, "img[alt='Tên ALT chính xác']")
    logo_locator = (By.CSS_SELECTOR, ".navbar-brand img")
    try:
        logo = wait.until(EC.visibility_of_element_located(logo_locator))
        assert logo.is_displayed()
        print("PASS: Logo NEU hiển thị.")
    except TimeoutException:
        pytest.fail(f"FAIL: Không tìm thấy hoặc logo không hiển thị sau 10 giây. Locator: {logo_locator}")

def test_login_form_displayed(driver: webdriver.Chrome):
    """Kiểm tra các trường username, password có hiển thị không."""
    wait = WebDriverWait(driver, 10)
    username_locator = (By.ID, "username")
    password_locator = (By.ID, "password")
    try:
        username_input = wait.until(EC.visibility_of_element_located(username_locator))
        password_input = wait.until(EC.visibility_of_element_located(password_locator))
        assert username_input.is_displayed()
        assert password_input.is_displayed()
        print("PASS: Ô username và password hiển thị.")
    except TimeoutException:
        pytest.fail(f"FAIL: Không tìm thấy ô username hoặc password sau 10 giây.")

def test_login_empty(driver: webdriver.Chrome):
    """Kiểm tra thông báo lỗi khi đăng nhập với trường trống."""
    wait = WebDriverWait(driver, 10)
    login_button_locator = (By.ID, "loginbtn")
    # Locator cho thông báo lỗi chung của Moodle (thường nằm trong div có class alert)
    error_message_locator = (By.CSS_SELECTOR, ".loginerrors .alert.alert-danger")

    try:
        # Đảm bảo trang đang ở trạng thái gốc (nếu cần)
        if LOGIN_URL not in driver.current_url:
             driver.get(LOGIN_URL)
             wait.until(EC.visibility_of_element_located((By.ID, "username"))) # Chờ trang tải lại

        login_button = wait.until(EC.element_to_be_clickable(login_button_locator))
        login_button.click()
        print("Đã click nút Login (để trống).")

        # Chờ thông báo lỗi xuất hiện
        error_message = wait.until(EC.visibility_of_element_located(error_message_locator))
        assert error_message.is_displayed()
        print(f"PASS: Thông báo lỗi hiển thị khi để trống. Nội dung: {error_message.text[:100]}...") # In ra một phần lỗi

        # Quay lại trang login để chuẩn bị cho test sau (nếu cần)
        # driver.get(LOGIN_URL)

    except TimeoutException:
        pytest.fail(f"FAIL: Không tìm thấy nút login hoặc thông báo lỗi không xuất hiện sau 10 giây.")
    except Exception as e:
        pytest.fail(f"FAIL: Đã xảy ra lỗi khác trong test_login_empty: {e}")


def test_login_wrong_credentials(driver: webdriver.Chrome):
    """Kiểm tra thông báo lỗi khi đăng nhập sai tài khoản/mật khẩu."""
    wait = WebDriverWait(driver, 10)
    username_locator = (By.ID, "username")
    password_locator = (By.ID, "password")
    login_button_locator = (By.ID, "loginbtn")
    error_message_locator = (By.CSS_SELECTOR, ".loginerrors .alert.alert-danger") # Dùng lại locator lỗi

    try:
        # Đảm bảo trang đang ở trạng thái gốc
        if LOGIN_URL not in driver.current_url:
             driver.get(LOGIN_URL)

        username_input = wait.until(EC.visibility_of_element_located(username_locator))
        password_input = wait.until(EC.visibility_of_element_located(password_locator))
        login_button = wait.until(EC.element_to_be_clickable(login_button_locator))

        username_input.clear()
        password_input.clear()
        username_input.send_keys("user_khong_ton_tai")
        password_input.send_keys("matkhau_sai")
        print("Đã nhập thông tin đăng nhập sai.")
        login_button.click()
        print("Đã click nút Login (sai thông tin).")

        # Chờ thông báo lỗi xuất hiện
        error_message = wait.until(EC.visibility_of_element_located(error_message_locator))
        assert error_message.is_displayed()
        print(f"PASS: Thông báo lỗi hiển thị khi sai thông tin. Nội dung: {error_message.text[:100]}...")

        # Quay lại trang login để chuẩn bị cho test sau (nếu cần)
        # driver.get(LOGIN_URL)

    except TimeoutException:
        pytest.fail(f"FAIL: Không tìm thấy form đăng nhập hoặc thông báo lỗi không xuất hiện sau 10 giây.")
    except Exception as e:
        pytest.fail(f"FAIL: Đã xảy ra lỗi khác trong test_login_wrong_credentials: {e}")


def test_forgot_password_link(driver: webdriver.Chrome):
    """Kiểm tra link 'Quên mật khẩu'."""
    wait = WebDriverWait(driver, 10)
    # Sử dụng PARTIAL_LINK_TEXT để đỡ bị ảnh hưởng bởi thay đổi nhỏ trong văn bản
    forgot_link_locator = (By.PARTIAL_LINK_TEXT, "Forgotten your username or password?") # Text phổ biến của Moodle

    try:
         # Đảm bảo đang ở trang login chính
        if LOGIN_URL not in driver.current_url:
             driver.get(LOGIN_URL)
             wait.until(EC.visibility_of_element_located(forgot_link_locator)) # Chờ link xuất hiện lại

        forgot_link = wait.until(EC.element_to_be_clickable(forgot_link_locator))
        print("Đã tìm thấy link quên mật khẩu.")
        forgot_link.click()
        print("Đã click link quên mật khẩu.")

        # Chờ URL thay đổi và chứa 'forgot_password.php'
        wait.until(EC.url_contains("updatepassword"))
        assert "updatepassword" in driver.current_url
        print("PASS: Đã chuyển đến trang quên mật khẩu.")

        # Quay lại trang trước đó
        driver.back()
        wait.until(EC.url_contains(LOGIN_URL)) # Chờ quay lại trang login
        print("Đã quay lại trang đăng nhập.")

    except TimeoutException:
        pytest.fail(f"FAIL: Không tìm thấy link quên mật khẩu hoặc trang không chuyển hướng đúng sau 10 giây.")
    except Exception as e:
        pytest.fail(f"FAIL: Đã xảy ra lỗi khác trong test_forgot_password_link: {e}")

def test_responsive_mobile(driver: webdriver.Chrome):
    """Kiểm tra xem navbar có hiển thị ở chế độ mobile không."""
    wait = WebDriverWait(driver, 10)
    navbar_locator = (By.CLASS_NAME, "navbar-inner") # Giữ nguyên locator này, cần kiểm tra lại nếu fail

    original_size = driver.get_window_size()
    print(f"Kích thước cửa sổ ban đầu: {original_size}")

    try:
        driver.set_window_size(375, 667) # Kích thước iPhone 6/7/8
        print("Đã đổi kích thước cửa sổ sang mobile.")

        # Chờ navbar hiển thị sau khi resize
        navbar = wait.until(EC.visibility_of_element_located(navbar_locator))
        assert navbar.is_displayed()
        print("PASS: Navbar hiển thị ở chế độ mobile.")

    except TimeoutException:
         pytest.fail(f"FAIL: Không tìm thấy navbar sau khi đổi kích thước sang mobile.")
    except Exception as e:
         pytest.fail(f"FAIL: Đã xảy ra lỗi khác trong test_responsive_mobile: {e}")
    finally:
        # Khôi phục kích thước cửa sổ ban đầu hoặc maximize lại
        # driver.set_window_size(original_size['width'], original_size['height'])
        driver.maximize_window()
        print("Đã khôi phục kích thước cửa sổ.")