# from flask import Flask    
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import os
# import requests  
# import time
# from bs4 import BeautifulSoup as bs 
from urllib.request import urlopen as uReq
# import pymongo
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
application = Flask(__name__)
app = application
@application.route('/',methods=['GET'])
@cross_origin() # its purpose is to be available to different countries
def index():
    return render_template("index.html")


@application.route('/results',methods=['POST','GET'])
@cross_origin() # its purpose is to be available to different countries
def result():
    if request.method == 'POST':
        try: 
            searchString = request.form['content']
            print(searchString)
#             options = Options()
#             options.add_argument("--headless")
#             chrome_driver_path = os.environ.get('CHROME_DRIVER_PATH')
#             print(chrome_driver_path)
                
#             driver = webdriver.Chrome(executable_path='/usr/var/app/current/chromedriver.exe',options=options)
#             driver = webdriver.Chrome(executable_path=chrome_driver_path,options=options)
#             chrome_driver_path = os.environ.get('CHROME_DRIVER_PATH')
            chrome_options = webdriver.ChromeOptions()
#             chrome_options.binary_location = '/usr/bin/google-chrome'
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
#             chrome_options.add_argument('--disable-dev-shm-usage')
#             chrome_options.add_argument("--disable-extensions")
            
            driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',options=chrome_options)
            driver.get("https://www.youtube.com/@linuxhint/videos")
            driver.add_cookie({'name': 'CONSENT', 'value': 'YES+1', 'domain': '.youtube.com'})
            driver.refresh()
            yt = searchString
            driver.get(yt)
#             try:
#     # wait until the "Accept all" button is present
# #                 cookie_consent_form = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "cookieconsent")))

# # find the "Accept all" button and click it
#                 accept_all_button =   driver.page_source.find_element_by_xpath("//button[contains(@class, 'ytp-button') and contains(text(), 'Accept all')]")
#                 accept_all_button.click()
#             except:
#     # handle exceptions if the "Accept all" button is not found or cannot be clicked
#                 pass
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # time.sleep(5)  # Add a sleep time to wait for more videos to load

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            box = soup.findAll('div', {'class': 'ytd-rich-grid-media'})
#             box = soup.findAll('div',id = 'contents')


            # Print the number of videos found
            print(f"Found {len(box)} videos")

            driver.quit()
            urls = []
            thumbnails = []
            for i in range(len(box)):
                try:
                    if("https://www.youtube.com"+box[i].a["href"] not in urls):
                        p =box[i].a["href"]
                        q = p[9:]
                        thumbnails.append("http://img.youtube.com/vi/"+q+"/hqdefault.jpg")
                        urls.append("https://www.youtube.com"+box[i].a["href"])
                except Exception as e:
                    pass
            vid_titles =[]
            for i in range(len(box)):
                try:
                    if(box[i].findAll('a',id="video-title-link")[0].text not in vid_titles):
                        vid_titles.append(box[i].findAll('a',id="video-title-link")[0].text)
                except Exception as e:
                    pass
            views=[]
            for i in range(0,len(box)):
                try:
                    if(box[i].findAll('span',{'class':'inline-metadata-item style-scope ytd-video-meta-block'})[0].text not in views):
                        views.append(box[i].findAll('span',{'class':'inline-metadata-item style-scope ytd-video-meta-block'})[0].text)
                except Exception as e:
                    pass
            time = []
            for i in range(0,len(box),3):
                try:
                    # if(box[i].findAll('span',{'class':'inline-metadata-item style-scope ytd-video-meta-block'})[1].text not in time):
                    time.append(box[i].findAll('span',{'class':'inline-metadata-item style-scope ytd-video-meta-block'})[1].text)
                except Exception as e:
                    pass
            url5 = urls[0:6]
            thumb5 = thumbnails[0:6]
            title5 = vid_titles[0:6]
            view5 = views[0:6]
            time5 = time[0:6]
            final = []
            for i in range(6):
                mydict = {"Video Urls": url5[i], "Thumbnail Urls": thumb5[i], "Title": title5[i], "Views": view5[i],
                          "Upload time": time5[i]}
                final.append(mydict)
            # client = pymongo.MongoClient("mongodb+srv://breakratr:breakratr@cluster0.ln0bt5m.mongodb.net/?retryWrites=true&w=majority")
            # db = client['review_scrap']
            # review_col = db['review_scrap_data']
            # review_col.insert_many(mydict)
            if(len(final)>0):
                return render_template('results.html', videos=final[0:len(final)])
            else:
                return "BHai scene hogaya!!!!"
                
        except  Exception as e:
            error_message = str(e)
            return f"An error occurred: {error_message,len(box),page_source}"
    else:
        render_template('index.html')
if __name__ == '__main__':
    application.run(debug=True)
# if __name__ == "__main__":
#     app.run(host='127.0.0.1', port=8000, debug=True)
 
