# 
from time import sleep
import os.path
import datetime
import glob


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
Options = webdriver.ChromeOptions()
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from secrets import pw



class InstaBot:
    def __init__(self, username, pw):
        self.chrome_options = Options
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=self.chrome_options)
        self.driver.get('https://instagram.com')
        self.username = username

    # Login page
        print('🌐 Logging in... \n')
        
        # Wait for login fields to be visible
        WebDriverWait(self.driver, 20)\
            .until(EC.presence_of_element_located((\
                By.XPATH, "//input[@name=\"username\"]"\
                )))\
                .send_keys(username)

        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)

        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()

    # Landing homepage feed
        print('🧍 Going to profile... \n')
        # WebDriverWait(self.driver, 20)\
        #     .until(EC.presence_of_element_located((\
        #         By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button'\
        #         )))\
        #         .click()
        WebDriverWait(self.driver, 20)\
            .until(EC.presence_of_element_located((\
                By.XPATH, '//button[.="Not Now"]'\
                    
                )))\
                .click()
        WebDriverWait(self.driver, 20)\
                    .until(EC.presence_of_element_located((\
                        By.XPATH, '//button[.="Not Now"]'\
                            
                        )))\
                        .click()
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()


    def save_file(self, content):
        
        print('📂 Saving file... \n')
        dirname = os.getcwd()
        save_path = os.path.join(dirname, 'archived-lists/')
        dateStr = datetime.datetime.now().strftime("%Y-%m-%d-")
        fname = dateStr + 'new-list.txt'
        completeName = os.path.join(save_path, fname)
        f = open(completeName, 'w')
        f.write(content)
        print('✅ Successfully saved file to: \n' + completeName)

    def get_lines(self, file):
        with open(file) as f:
            lines = [line.rstrip() for line in f]
        return lines

    def get_changed(self):
        list_of_files = glob.glob('archived-lists/*')
        sorted_files = sorted(list_of_files,  key=os.path.getctime)
        latest_file = sorted_files[-1]
        second_latest_file = sorted_files[-2]
        file_1_lines = self.get_lines(latest_file)
        file_2_lines = self.get_lines(second_latest_file)
        changed=[item for item in file_1_lines if item not in file_2_lines]
        print(changed)


    def get_unfollowers(self):

        WebDriverWait(self.driver, 20)\
            .until(EC.presence_of_element_located((\
                By.XPATH, "//a[contains(@href,'/following')]"\
                )))\
                .click()
        following = self._get_names()
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        followers = self._get_names()
        not_following_back = [user for user in following if user not in followers]
        listToStr = '\n'.join(map(str, not_following_back))
        print(not_following_back)
        self.save_file( listToStr )
        # self.get_changed()
        

    def _get_names(self):
        print('✍️ Collecting names... \n')
        sleep(2)
        # sugs = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
        # self.driver.execute_script('arguments[0].scrollIntoView()', sugs)
        # sleep(2)
        # scroll_box = self.driver.find_element_by_xpath("/html/body/div[@role=\"presentation\"]/div/div/div[2]")
        # scroll_box = WebDriverWait(self.driver, 20)\
        #     .until(EC.presence_of_element_located((By.XPATH, "/html/body/div[@role=\"presentation\"]/div/div/div/div[last()]")))
        scroll_box = WebDriverWait(self.driver, 20)\
            .until(EC.presence_of_element_located((By.XPATH, "//div[@style=\"max-height: 400px; min-height: 200px;\"]/div[last()]")))

        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("//div[@role=\"dialog\"]//div[@style=\"height: 100%; width: 100%;\"]/following-sibling::div[node()]//button")\
            .click()
            
        return names

my_bot = InstaBot('the_kjax', pw)
my_bot.get_unfollowers()
