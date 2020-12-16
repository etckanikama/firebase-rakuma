import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from base64 import a85encode
import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time
import datetime
import pandas as pd
import sys
import eel

cred = credentials.Certificate('./firstdatabase-19295-firebase-adminsdk-c7g6z-c758718277.json')
app = firebase_admin.initialize_app(cred)

db = firestore.client()



def login(inp):
    
    users_ref = db.collection(u'users')
    docs = users_ref.stream()
    print("Firebaseを参照にパスワードとなるkeyを入力してください：")
    for doc in docs:
        # print(u'{} => {}'.format(doc.id, doc.to_dict()))
        # print(doc.to_dict().values())
        for mykey in doc.to_dict().values():
            # print(mykey)
            while (True):
                # inp = input()
                if inp != mykey:
                    print('パスワードが違います。再度入力してください。')
                    eel.undisplay()
                    eel.write("{}はいません.再度入力してください".format(inp))
                    break
                    
                else:
                    print('ログイン成功')
                    eel.display()
                    eel.write("Hello {} ! ログイン成功".format(inp))
                    
                    time.sleep(1)
                    # 何かしらの関数
                    # print(myprint(inp))
                    eel.run()
                    
                    break


def myprint(a):
    return 'Hello '+a+' !'

def set_driver(driver_path, headless_flg):
    # これは自分の場合のログインを保持するためのChromeのぱす
    PROFILE_PATH = "C:\\Users\\hirayama\\AppData\\Local\\Google\\Chrome\\User Data"
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--user-data-dir=C:\\Users\\hirayama\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
    # options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

@eel.expose
def listing():

    FIST_URL = "https://fril.jp/item/new"
    # 絶対パス？？
    IMG_PATH = 'C:\\Users\\hirayama\\src\\firebase-rukuma\\dog.jpg'
    
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)

    # Webサイトを開く
    driver.get(FIST_URL)
    time.sleep(5)

    # 文字列ログイン探す
    # （あったらログインボタンを開く→その後に手動ログインをする）
    # なくなるまで待機
    # なかったらその後の処理を実行
    # login_button_get = driver.find_element_by_xpath("//li[@class='loginMenu__listItem']/a[@class='button button--NoBorderSmall ga-class ga-login-button ga-guest']")
    
    # time.sleep(10)
    # print(login_button_get.text)
    # login_url = login_button_get.get_attribute("href")
    # print(login_url)
    # driver.get(f'{login_url}')
    # time.sleep(10)
    #指定したdriverに対して最大で10秒間待つように設定する
    wait = WebDriverWait(driver, 1000)
    element = wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "headerMenu__text")))
    driver.get(FIST_URL)
    time.sleep(10)

    # 何がsend_keysに入るかわからんからいったんこのまま
    driver.find_element_by_id("image_tmp").send_keys(IMG_PATH)
    time.sleep(2)
    driver.find_element_by_id("name").send_keys("ゲーム")
    time.sleep(2)
    driver.find_element_by_id("detail").send_keys("ps4")
    # time.sleep(2)

    # カテゴリのところ
    driver.find_elements_by_link_text("指定なし")[0].click()
    time.sleep(1)
    driver.find_element_by_link_text("レディース").click()
    driver.find_element_by_link_text("トップス").click()
    time.sleep(1)
    driver.find_element_by_link_text("Tシャツ(半袖/袖なし)").click()
    time.sleep(1)
    # サイズ指定(上で指定なしが消えるからまた0番目になる→要素一つでいいような気がするけど)
    driver.find_elements_by_link_text("指定なし")[0].click()
    time.sleep(1)
    driver.find_element_by_link_text("S").click()


    time.sleep(2)
    driver.find_element_by_id("status").send_keys("未使用に近い")
    time.sleep(2)
    driver.find_element_by_id("carriage").send_keys("着払い（購入者が負担）")
    time.sleep(2)
    driver.find_element_by_id("delivery_method").send_keys("着払い（購入者が負担）")
    time.sleep(2)
    driver.find_element_by_id("delivery_date").send_keys("支払い後、2～3日で発送")
    time.sleep(2)
    driver.find_element_by_id("delivery_area").send_keys("沖縄")
    time.sleep(2)
    driver.find_element_by_id("request_required").send_keys("あり")
    time.sleep(2)
    driver.find_element_by_id("sell_price").send_keys(1000)
    time.sleep(2)
    print("終了")
    

# if __name__ == "__main__":
#     login()