from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
import pandas as pd
import os
import time
import getpass
from datetime import datetime

# Browser options
chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)
save_location = os.getcwd()

print("=" * 60)
print("RIT ATTENDANCE SUMMARY GENERATOR")
print("=" * 60)
print(f"\n💾 Files will be saved to:")
print(f"   {save_location}")
print("=" * 60)

# All URLs to try
urls = [
    "http://210.212.171.172/ritcms/Default.aspx",
    "http://172.22.4.115/ritcms/Default.aspx",
    "http://ritage.ritindia.edu/RITCMS/Default.aspx"
]

connected = False
current_url = None

print("\n🔌 Connecting to RIT CMS...")

# Try each URL
for idx, url in enumerate(urls, 1):
    try:
        print(f"📡 Attempting {idx}/3: {url.split('//')[1].split('/')[0]}", end=" ")
        driver.get(url)
        driver.set_page_load_timeout(8)
        
        # Check if login page loaded
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "txt_UserId"))
            )
            print("✅")
            connected = True
            current_url = url
            break
        except:
            print("❌")
            continue
            
    except Exception as e:
        print("❌")
        continue

if not connected:
    print("\n❌ Failed to connect to any RIT CMS portal!")
    print("Please check your internet connection and try again.")
    driver.quit()
    input("\nPress ENTER to exit...")
    exit()

print("\n" + "=" * 60)

# Login with retry logic
login_successful = False
max_attempts = 3
attempt = 0

while not login_successful and attempt < max_attempts:
    attempt += 1
    
    print(f"\n🔐 LOGIN ATTEMPT {attempt}/{max_attempts}")
    print("-" * 60)
    
    if attempt == 1:
        user_id = input("Enter your User ID (e.g., 2303026): ").strip()
        password = getpass.getpass("Enter your Password: ")
    else:
        print("❌ Previous login failed. Please try again.")
        user_id = input("Enter your User ID: ").strip()
        password = getpass.getpass("Enter your Password: ")
    
    print("-" * 60)
    
    try:
        time.sleep(1)
        
        # Enter User ID
        print("📝 Entering credentials...", end=" ")
        username_field = driver.find_element(By.ID, "txt_UserId")
        username_field.clear()
        username_field.send_keys(user_id)
        
        # Enter Password
        password_field = driver.find_element(By.ID, "txt_password")
        password_field.clear()
        password_field.send_keys(password)
        
        # Click Login
        login_button = driver.find_element(By.ID, "cmd_LogIn")
        login_button.click()
        
        print("⏳ Verifying...")
        time.sleep(3)
        
        # Check for error message
        try:
            error_msg = driver.find_element(By.ID, "lbl_err")
            if error_msg.is_displayed() and "Invalid" in error_msg.text:
                print(f"\n❌ {error_msg.text}")
                if attempt < max_attempts:
                    print(f"\n⚠️  You have {max_attempts - attempt} attempt(s) remaining")
                    driver.refresh()
                    time.sleep(2)
                continue
        except:
            pass
        
        # Check if dashboard loaded
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//img[@src='../images/attendance1.jpg']"))
            )
            print("✅ Login successful!")
            login_successful = True
        except:
            print("\n❌ Login failed - Dashboard not loaded")
            if attempt < max_attempts:
                print(f"⚠️  You have {max_attempts - attempt} attempt(s) remaining")
                driver.refresh()
                time.sleep(2)
            
    except Exception as e:
        print(f"\n❌ Error during login: {str(e)[:50]}")
        if attempt < max_attempts:
            driver.refresh()
            time.sleep(2)

if not login_successful:
    print("\n❌ Maximum login attempts reached. Exiting...")
    driver.quit()
    input("\nPress ENTER to exit...")
    exit()

try:
    print("\n" + "=" * 60)
    
    # Click on Attendance Dashboard
    print("📊 Opening Attendance Dashboard...")
    attendance_image = driver.find_element(By.XPATH, "//img[@src='../images/attendance1.jpg']")
    attendance_image.click()
    print("  ✓ Attendance dashboard opened")
    
    time.sleep(3)
    
    print("\n🤖 Extracting attendance data...\n")
    print("=" * 60)
    
    select_buttons = driver.find_elements(By.XPATH, "//input[@type='button' and @value='Select']")
    num_subjects = len(select_buttons)
    
    print(f"✓ Found {num_subjects} subjects\n")
    
    subject_stats = []
    
    for i in range(num_subjects):
        select_buttons = driver.find_elements(By.XPATH, "//input[@type='button' and @value='Select']")
        
        print(f"[{i+1}/{num_subjects}] Processing...", end=" ")
        
        select_buttons[i].click()
        time.sleep(2.5)
        
        try:
            tables = pd.read_html(driver.page_source, attrs={'id': 'GridViewAttendedance'})
            
            if tables:
                df = tables[0]
                df.columns = ['StaffCode', 'SubjectCode', 'TheoryPractical', 'AttenDate', 'LectureTime', 'Attendance']
                
                # Get subject name
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                caption = soup.find('table', {'id': 'GridViewAttendedance'}).find('caption')
                subject_name = caption.text.strip() if caption else "Unknown"
                
                # Parse dates and find latest
                df['AttenDate'] = pd.to_datetime(df['AttenDate'], format='%d/%m/%Y', errors='coerce')
                latest_date = df['AttenDate'].max()
                
                # Calculate stats
                total_classes = len(df)
                present_count = len(df[df['Attendance'] == 'P'])
                absent_count = len(df[df['Attendance'] == 'A'])
                percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
                
                # Calculate classes needed for 75%
                if percentage < 75:
                    classes_needed = int((0.75 * total_classes - present_count) / 0.25) + 1
                else:
                    classes_needed = 0
                
                subject_stats.append({
                    'Subject': subject_name,
                    'SubjectCode': df['SubjectCode'].iloc[0] if len(df) > 0 else 'N/A',
                    'TotalClasses': total_classes,
                    'Present': present_count,
                    'Absent': absent_count,
                    'AttendancePercentage': round(percentage, 2),
                    'LatestAttendanceDate': latest_date.strftime('%d/%m/%Y') if pd.notna(latest_date) else 'N/A',
                    'ClassesNeededFor75': classes_needed
                })
                
                print(f"✓ {subject_name[:30]}")
                
        except Exception as e:
            print(f"❌ Failed: {str(e)[:30]}")
        
        # Click Back
        try:
            back_buttons = driver.find_elements(By.XPATH, "//input[@type='button' and @value='Back']")
            if back_buttons:
                back_buttons[0].click()
                time.sleep(1.8)
        except:
            pass
    
    print("\n" + "=" * 60)
    
    if subject_stats:
        # Create summary DataFrame (WITHOUT OVERALL ROW)
        summary_df = pd.DataFrame(subject_stats)
        
        # Save summary file
        summary_path = os.path.join(save_location, 'attendance_summary.csv')
        summary_df.to_csv(summary_path, index=False)
        
        # Calculate overall stats (for console display only)
        total_classes = summary_df['TotalClasses'].sum()
        total_present = summary_df['Present'].sum()
        total_absent = summary_df['Absent'].sum()
        overall_percentage = (total_present / total_classes * 100) if total_classes > 0 else 0
        
        # Calculate overall classes needed
        if overall_percentage < 75:
            overall_classes_needed = int((0.75 * total_classes - total_present) / 0.25) + 1
        else:
            overall_classes_needed = 0
        
        print("✅ SUMMARY GENERATED!")
        print("=" * 60)
        
        print(f"\n📊 OVERALL ATTENDANCE:")
        print(f"{'=' * 60}")
        print(f"Total Classes: {total_classes}")
        print(f"Present: {total_present}")
        print(f"Absent: {total_absent}")
        print(f"📈 Percentage: {overall_percentage:.2f}%")
        
        if overall_percentage < 75:
            print(f"⚠️  You need to attend {overall_classes_needed} consecutive classes to reach 75%")
        else:
            print(f"✅ Great! You're above 75%")
        print(f"{'=' * 60}")
        
        print(f"\n📋 SUBJECT-WISE SUMMARY:")
        print(f"{'=' * 60}")
        for stat in subject_stats:
            status = "⚠️" if stat['AttendancePercentage'] < 75 else "✅"
            print(f"\n{status} {stat['Subject']}")
            print(f"  Code: {stat['SubjectCode']}")
            print(f"  Attendance: {stat['AttendancePercentage']}% ({stat['Present']}/{stat['TotalClasses']})")
            print(f"  Latest Class: {stat['LatestAttendanceDate']}")
            if stat['ClassesNeededFor75'] > 0:
                print(f"  Need to attend: {stat['ClassesNeededFor75']} classes for 75%")
        
        print(f"\n{'=' * 60}")
        print(f"\n📄 FILE SAVED:")
        print(f"   ✓ {summary_path}")
        print(f"{'=' * 60}")
        
    else:
        print("\n❌ No attendance data extracted!")
        
except Exception as e:
    print(f"\n❌ Error occurred: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    print("\n🔒 Closing browser...")
    time.sleep(2)
    driver.quit()
    print("✓ Browser closed successfully!")

print("\nPress ENTER to exit...")
input()
