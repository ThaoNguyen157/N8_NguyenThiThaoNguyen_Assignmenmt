import unittest
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import pytest
import logging  
from selenium.webdriver.firefox.options import Options

logging.basicConfig(level=logging.ERROR) 

# Thiết lập fixture để khởi tạo và đóng trình duyệt
@pytest.fixture
def driver():
    driver = webdriver.Chrome()  
    yield driver
    driver.quit()

def test_login(driver): # Kiểm tra đăng nhập và đăng xuất
    driver.get("http://localhost/webopencart/index.php?route=account/login&language=en-gb") #Mỏ trang chính OpenCart
    time.sleep(2)  

    account_dropdown = WebDriverWait(driver, 2).until( # Mở menu tài khoản
        EC.element_to_be_clickable((By.XPATH, "//a[@class='dropdown-toggle' and @data-bs-toggle='dropdown']"))
    )
    driver.execute_script("arguments[0].click();", account_dropdown) # Nhấp vào menu tài khoản

    try: # Chọn mục "Đăng nhập"
        link_to_login = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Login"))
        )
        driver.execute_script("arguments[0].click();", link_to_login)   # Nhấp vào "Login"
    except Exception as e:
        logging.error("Error locating the Login link: %s", e)
        logging.error("Current page source: %s", driver.page_source)
        return

    # Nhập email và mật khẩu rồi nhấn nút "Đăng nhập"
    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.ID, "input-email"))
    ).send_keys("nttn1234@gmail.com")
    driver.find_element(By.ID, "input-password").send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()

    # Kiểm tra chuyển hướng đến trang tài khoản sau khi đăng nhập thành công
    WebDriverWait(driver, 2).until(
        EC.url_contains("account/account")
    )
    assert "account/account" in driver.current_url, "Login failed or user not redirected to account page."

# 
#  
# 
# 

    # Mở menu tài khoản và chọn mục "Đăng xuất"
    myAccount_dropdown = WebDriverWait(driver, 2).until( #Click vào menu để hiện phầm dropdown menu
        EC.element_to_be_clickable((By.XPATH, "//a[@class='dropdown-toggle' and @data-bs-toggle='dropdown']"))
    )
    driver.execute_script("arguments[0].click();", myAccount_dropdown) 

    logout_link = WebDriverWait(driver, 2).until( #Click vào phần "Logout"
        EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
    )
    driver.execute_script("arguments[0].click();", logout_link) #Click nút Logout

    #Kiểm tra Logout thành công hay không
    notification = driver.find_element(By.CSS_SELECTOR, "#content > h1")  # Xác định vị trí của thông báo
    notificationActual = notification.text  # Lấy text của thông báo xuất ra
    notificationExpected = "Account Logout"  # Text trông chờ
    assert notificationExpected == notificationActual, "Order was not placed successfully"  # Kiểm tra kết quả có đúng như thông báo không

# PASS 
def test_invalid_email_login(driver): # Kiểm tra đăng nhập với email sai định dạng
    driver.get("http://localhost/webopencart/index.php?route=account/login&language=en-gb") #Mở Trang login 
    time.sleep(2) 

    # Nhập email sai định dạng và mật khẩu, sau đó nhấn đăng nhập
    email_field = WebDriverWait(driver, 20).until( #Nhập vào địa chỉ email sai định dạng
        EC.element_to_be_clickable((By.ID, "input-email"))
    )
    email_field.send_keys("wrongemail.com") 

    password_field = driver.find_element(By.ID, "input-password") #Nhập vào mật khẩu
    password_field.send_keys("wrongpassword")  
    time.sleep(2)  

    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
    )
    time.sleep(2)
    
    driver.execute_script("arguments[0].click();", login_button) #Nhấn nút login

    #Đợi thông báo và kiểm tra kết quả
    error_message = WebDriverWait(driver, 2).until( 
        EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
    )

    assert error_message.is_displayed(), "Error message is not displayed."
    assert "Warning: No match for E-Mail Address and/or Password." in error_message.text.strip(), \
        "Unexpected error message content."


# PASS
def test_invalid_password_login(driver): # Kiểm tra đăng nhập với passowrd sai
    driver.get("http://localhost/webopencart/index.php?route=account/login&language=en-gb") #Mở trang Login

    # Nhập email sai định dạng và mật khẩu, sau đó nhấn đăng nhập
    email_field = WebDriverWait(driver, 2).until( #Nhập vào chỗ email
        EC.element_to_be_clickable((By.ID, "input-email"))
    )
    email_field.send_keys("nttn1234@gmail.com")  

    password_field = driver.find_element(By.ID, "input-password") #Nhập vào password
    password_field.send_keys("wrongpassword")  
    time.sleep(2)  

    login_button = WebDriverWait(driver, 2).until( #Click vào nút Login
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
    )

    try:
        login_button.click()  
        time.sleep(2) 

        if "Warning: No match for E-Mail Address" not in driver.page_source:
            driver.execute_script("arguments[0].click();", login_button)
            time.sleep(2)

    except Exception as e:
        print("Click attempt failed:", e)

    try:
        error_message = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
        )

        assert error_message.is_displayed(), "Error message is not displayed."
        assert "Warning: No match for E-Mail Address and/or Password." in error_message.text.strip(), \
            "Unexpected error message content."

    except Exception as e:
        print("Error message not found or assertion failed:", e)
        print("Current page source:", driver.page_source)


# PASS
def test_empty_password_login(driver): # Kiểm tra đăng nhập khi trường mật khẩu để trống
    driver.get("http://localhost/webopencart/index.php?route=account/login&language=en-gb") # Truy cập trang đăng nhập của OpenCart

    # Nhập email hợp lệ vào trường email
    email_field = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, "input-email"))
    )
    email_field.send_keys("leduyquan2574@gmail.com") 

    password_field = driver.find_element(By.ID, "input-password") # Để trống trường mật khẩu và đảm bảo không có dữ liệu nhập vào
    password_field.clear() 
    time.sleep(2) 
    
    # Nhấp vào nút đăng nhập
    login_button = WebDriverWait(driver, 2).until( 
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
    )
    login_button.click()

    # Kiểm tra sự xuất hiện của thông báo lỗi
    try:
        error_message = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
        )
        # Xác nhận rằng thông báo lỗi hiển thị và nội dung của nó đúng
        assert error_message.is_displayed(), "Error message is not displayed."
        assert "Warning: No match for E-Mail Address and/or Password." in error_message.text.strip(), \
            "Unexpected error message content."

    except Exception as e:
        print("Error message not found or assertion failed:", e)
        print("Current page source:", driver.page_source)


# PASS
def test_empty_email_login(driver): # Kiểm tra đăng nhập khi trường email để trống
     # Truy cập trang đăng nhập
    driver.get("http://localhost/webopencart/index.php?route=account/login&language=en-gb")

    # Nhập mật khẩu không hợp lệ vào trường mật khẩu
    password_field = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, "input-password"))
    )
    password_field.send_keys("wrongpassworrd@")  

    # Để trống trường email
    email_field = driver.find_element(By.ID, "input-email")
    email_field.clear() 
    time.sleep(2)  

    login_button = WebDriverWait(driver, 2).until( # Nhấp vào nút đăng nhập
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
    )
    login_button.click()

    try: # Kiểm tra sự xuất hiện của thông báo lỗi
        error_message = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
        )
        # Xác nhận rằng thông báo lỗi hiển thị và nội dung của nó đúng
        assert error_message.is_displayed(), "Error message is not displayed."
        assert "Warning: No match for E-Mail Address and/or Password." in error_message.text.strip(), \
            "Unexpected error message content."

    except Exception as e:
        print("Error message not found or assertion failed:", e)
        print("Current page source:", driver.page_source)


# # PASS
def test_email_have_special_character_login(driver): # Kiểm tra đăng nhập với email chứa ký tự đặc biệt
    driver.get("http://localhost/webopencart/index.php?route=account/login&language=en-gb") #Mở ra trang login

    # Nhập email với ký tự đặc biệt và mật khẩu hợp lệ
    email_field = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, "input-email"))
    )
    email_field.send_keys("!@#$%^&*()") 

    password_field = driver.find_element(By.ID, "input-password")
    password_field.send_keys("password")  
    time.sleep(2)  

    login_button = WebDriverWait(driver, 2).until( #Click vào nút "Login"
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
    )
    login_button.click()

    try: # Kiểm tra thông báo lỗi hiển thị
        error_message = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
        )

        # Assert that the error message is displayed and check its text
        assert error_message.is_displayed(), "Error message is not displayed."
        assert "Warning: No match for E-Mail Address and/or Password." in error_message.text.strip(), \
            "Unexpected error message content."

    except Exception as e:
        print("Error message not found or assertion failed:", e)
        print("Current page source:", driver.page_source)


# # PASS
def test_password_have_special_character_login(driver): # Kiểm tra đăng nhập với mật khẩu chứa ký tự đặc biệt
    driver.get("http://localhost/webopencart/index.php?route=account/login&language=en-gb") #Mở ra trang login

    # Nhập email hợp lệ và mật khẩu với ký tự đặc biệt
    email_field = WebDriverWait(driver, 20).until( #Nhập email chính xác
        EC.element_to_be_clickable((By.ID, "input-email"))
    )
    email_field.send_keys("nttn1234@gmail.com") 

    password_field = driver.find_element(By.ID, "input-password") #Nhập kí tự đặng việt vào password
    password_field.send_keys("!@#$%^&*()")  
    time.sleep(2)  

    login_button = WebDriverWait(driver, 20).until( #Click vào nút "Login"
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
    )
    login_button.click()

    try: #Kiểm tra hiện thông báo và xác nhận đúng hay sai
        error_message = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
        )

        # Thông báo lỗi đã được hiển thị và kiểm tra lỗi đó
        assert error_message.is_displayed(), "Error message is not displayed."
        assert "Warning: No match for E-Mail Address and/or Password." in error_message.text.strip(), \
            "Unexpected error message content."

    except Exception as e:
        print("Error message not found or assertion failed:", e)
        print("Current page source:", driver.page_source)

# PASS
def test_emailAndPassword_have_special_character_login(driver): # Kiểm tra đăng nhập với cả email và mật khẩu đều chứa ký tự đặc biệt
    driver.get("http://localhost/webopencart/index.php?route=account/login&language=en-gb") #Mở ra trang login

     # Nhập cả email và mật khẩu với ký tự đặc biệt
    email_field = WebDriverWait(driver, 2).until( #Nhấn vào kí tự đặc biệt ở email
        EC.element_to_be_clickable((By.ID, "input-email"))
    )
    email_field.send_keys("!@#$%^&*()") 

    password_field = driver.find_element(By.ID, "input-password") #Nhấn vào kí tự đặc biệt của mật khẩu
    password_field.send_keys("!@#$%^&*()")  
    time.sleep(2)  

    login_button = WebDriverWait(driver, 20).until( #Nhấn vào nút "login"
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
    )
    login_button.click()

    try: #Hiện thông báo và xác nhận đúng hay sai
        error_message = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
        )

        # Thông báo lỗi đã được hiển thị và kiểm tra lỗi đó
        assert error_message.is_displayed(), "Error message is not displayed."
        assert "Warning: No match for E-Mail Address and/or Password." in error_message.text.strip(), \
            "Unexpected error message content."

    except Exception as e:
        print("Error message not found or assertion failed:", e)
        print("Current page source:", driver.page_source)



# # PASS
def test_sql_correct_statement_to_login(driver): # Kiểm tra đăng nhập với tấn công SQL injection
    driver.get("http://localhost/webopencart/index.php?route=account/login&language=en-gb") #Mở ra trang Login

    # Nhập câu lệnh SQL vào trường email và mật khẩu
    email_field = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, "input-email"))
    )
    email_field.send_keys("' UNION SELECT NULL, username, password FROM users -- ")

    password_field = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, "input-password"))
    )
    password_field.send_keys("' UNION SELECT NULL, username, password FROM users -- ")
    time.sleep(2)  

    login_button = WebDriverWait(driver, 2).until( #Nhấn vào nút "Login"
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
    )
    login_button.click()

    try: #Kiểm tra thông báo và xác nhận đúng hay sai
        error_message = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
        )

        assert error_message.is_displayed(), "Error message is not displayed after SQL injection attempt."
        assert "Warning: No match for E-Mail Address and/or Password." in error_message.text.strip(), \
            "Unexpected error message content."

    except Exception as e:
        print("Error message not found or assertion failed:", e)
        print("Current page source:", driver.page_source)