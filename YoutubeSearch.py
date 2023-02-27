from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import json
from datetime import datetime


class YoutubeSearch:

    def __init__(self, driver_url, headless):
        self.keywords = ''

        self.min_subscribers_filter = 0
        self.max_subscribers_filter = 1000000000

        self.min_views_filter = 0
        self.max_views_filter = 100000000000

        self.joined_start_date_filter = datetime(2005, 1, 1)
        self.joined_end_date_filter = datetime.today()

        self.location_filter = None

        self.video_counts_start_filter = 0
        self.video_counts_end_filter = 100000

        self.average_video_views_start_filter = 0
        self.average_video_views_end_filter = 100000000000

        self.result_record_count = 20

        self.__username = None
        self.__password = None
        
        self.options = Options()
        self.options.headless = headless
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("start-maximized")
        self.driver = webdriver.Chrome(driver_url, options=self.options)


    # run
    def run(self, keywords):
        self.driver.get('https://www.youtube.com/')
        # self.driver.maximize_window()
        self.keywords = keywords
        
        time.sleep(5)
        search_box =self.driver.find_elements(By.TAG_NAME, "input")      
        search_box[0].send_keys(keywords)
        search_box[0].send_keys(Keys.ENTER)
        
        time.sleep(5)
        search_box =self.driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/div/ytd-toggle-button-renderer/yt-button-shape/button")      
        search_box.click()
        
        time.sleep(1)
        channel_search_mode =self.driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/ytd-search-filter-group-renderer[2]/ytd-search-filter-renderer[2]/a")      
        channel_search_mode.click()
        
        time.sleep(3)
        channel_list_counter = 1
        resulting_channels = []
                            
        while(True):            
            channels_parent =self.driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[{channel_list_counter}]")             
            channels_list = channels_parent.find_elements(By.TAG_NAME,"ytd-channel-renderer")

            for i in range(len(channels_list)):                
                channel_link = channels_list[i].find_elements(By.TAG_NAME,"a")[0].get_attribute("href")
                channel_avatar = channels_list[i].find_elements(By.TAG_NAME,"img")[0].get_attribute("src") 
                channel_name = channels_list[i].find_element(By.ID,"channel-title").find_element(By.ID,"text-container").text
                channel_subscriber = channels_list[i].find_element(By.ID,"video-count").text.split(" ")[0]
                channel_brief_description = channels_list[i].find_element(By.ID,"description").text
                subscriber = 0
                if('G' in channel_subscriber):
                    subscriber = float(channel_subscriber[0:len(channel_subscriber)-1]) * 1000000000
                elif('M' in channel_subscriber):
                    subscriber = float(channel_subscriber[0:len(channel_subscriber)-1]) * 1000000
                elif('K' in channel_subscriber):
                    subscriber = float(channel_subscriber[0:len(channel_subscriber)-1]) * 1000
                else:
                    if(channel_subscriber == ''):
                        channel_subscriber = 0
                        subscriber = 0
                    else:
                        subscriber = float(channel_subscriber)
                                
                # filter 01
                if(subscriber>=self.min_subscribers_filter and subscriber<=self.max_subscribers_filter):                    
                    
                    # go channel
                    self.driver.execute_script("window.open();")
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    self.driver.get(channel_link)
                    
                    try:
                        # about tab
                        final_tab = len(self.driver.find_elements(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/tp-yt-app-toolbar/div/div/tp-yt-paper-tabs/div/div/tp-yt-paper-tab"))
                        about_page = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH,f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/tp-yt-app-toolbar/div/div/tp-yt-paper-tabs/div/div/tp-yt-paper-tab[{final_tab-1}]")))
                        while("about" not in about_page.text.lower()):
                            about_page = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH,f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/tp-yt-app-toolbar/div/div/tp-yt-paper-tabs/div/div/tp-yt-paper-tab[{final_tab}]")))
                        
                        about_page.click()
                        time.sleep(3)                    
                        joined_date_read = self.driver.find_element(By.ID,"right-column").find_elements(By.TAG_NAME,"span")[1].text
                        joined_date = datetime.strptime(joined_date_read, '%b %d, %Y')
                        views = self.driver.find_element(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-about-metadata-renderer/div[2]/yt-formatted-string[3]").text
                        if(' ' in views):
                            views = views.split(" ")[0]
                        if(',' in views):
                            views = views.replace(',','')
                            views = int(views)
                            
                        full_description = self.driver.find_element(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-about-metadata-renderer/div[1]/div[1]/yt-formatted-string[2]").text                      
                        location = self.driver.find_element(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-about-metadata-renderer/div[1]/div[4]/table/tbody/tr[2]/td[2]/yt-formatted-string").text   
                        link_titles = self.driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-about-metadata-renderer/div[1]/div[5]/div').find_elements(By.CSS_SELECTOR, "a.yt-simple-endpoint")
                        links = []
                        for c in range(len(link_titles)):         
                            if(len(link_titles[c].text)>1):            
                                links.append({link_titles[c].text:link_titles[c].get_attribute("href")})     
                                                
                        average_views = 0   
                        video_counter = 0                          

                        # videos tab
                        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/tp-yt-app-toolbar/div/div/tp-yt-paper-tabs/div/div/tp-yt-paper-tab[2]"))).click()

                        time.sleep(2)

                        # scroll till end
                        while True:
                            start = self.driver.execute_script("return window.scrollY")
                            html = self.driver.find_element(By.TAG_NAME, 'html')
                            html.send_keys(Keys.END)                                                        
                            time.sleep(0.5)                                
                            end = self.driver.execute_script("return window.scrollY")
                            if start-end==0:
                                break
                        
                        rec_rows_count = len(self.driver.find_elements(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row'))
                        for r in range(rec_rows_count):
                            col_count = len(self.driver.find_elements(By.XPATH,f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[{r+1}]/div/ytd-rich-item-renderer'))
                            for c in range(col_count):
                                view_label = self.driver.find_element(By.XPATH,f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[{r+1}]/div/ytd-rich-item-renderer[{c+1}]/div/ytd-rich-grid-media/div[1]/div[2]/div[1]/ytd-video-meta-block/div[1]/div[2]/span[1]').text.split(' ')[0]
                                view_label = view_label.replace('.','')
                                view_num = 0
                                if('G' in view_label):
                                    view_num = int(view_label[0:len(view_label)-1]) * 1000000000
                                elif('M' in view_label):
                                    view_num = int(view_label[0:len(view_label)-1]) * 1000000
                                elif('K' in view_label):
                                    view_num = int(view_label[0:len(view_label)-1]) * 1000
                                else:
                                    view_num = int(view_label)
                                video_counter+=1
                                average_views += view_num
                        average_views = int(average_views/video_counter)
                                            
                        # filter 02                                            
                        if((views>=self.min_views_filter and views<=self.max_views_filter) and
                           (joined_date>=self.joined_start_date_filter and joined_date<=self.joined_end_date_filter) and
                           (self.location_filter == None or location.lower() in self.location_filter) and 
                           (video_counter>=self.video_counts_start_filter and video_counter<=self.video_counts_end_filter) and
                           (average_views>=self.average_video_views_start_filter and average_views<=self.average_video_views_end_filter) ):
                            # add to result
                            temp = {"channel name":channel_name,"subscriber":subscriber,"avatar":channel_avatar,"link":channel_link,"description":full_description,"joined date":joined_date.strftime("%Y-%m-%d"),"views":views,"location":location,"links":links,"average view":average_views, "video count": video_counter}
                        
                        resulting_channels.append(temp)         
                    except:
                        print("ignored!")                                                                                
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                channel_list_counter += 1 
                # self.driver.find_element(By.TAG_NAME,"html").send_keys(Keys.END)  

                if(len(resulting_channels)>=self.result_record_count):
                    break                
            
            if(len(resulting_channels)>=self.result_record_count):
                break    
            
                                
            self.driver.execute_script("window.scrollTo(0, 0)")  
            time.sleep(2)
            
        json_data = json.dumps(resulting_channels)            
        try:
            json.loads(json_data)
            print("Valid JSON data")
        except ValueError as e:
            print("Invalid JSON data:", e)

        # self.driver.close()
        return json_data    

        # write the JSON data to a file
        # with open('data.json', 'w') as f:
        #     f.write(json_data)

    
# youtube = YoutubeSearch('C:\Apps\chrome_110\chromedriver.exe',False)
    
# youtube.result_record_count = 35
# youtube.run('zahra dairy turkey')
