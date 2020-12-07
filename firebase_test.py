import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from base64 import a85encode
import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import datetime
import pandas as pd
import sys

cred = credentials.Certificate('./firstdatabase-19295-firebase-adminsdk-c7g6z-c758718277.json')
app = firebase_admin.initialize_app(cred)

db = firestore.client()



def main():
    users_ref = db.collection(u'users')
    docs = users_ref.stream()
    print("Firebaseを参照にパスワードとなるkeyを入力してください：")
    for doc in docs:
        # print(u'{} => {}'.format(doc.id, doc.to_dict()))
        # print(doc.to_dict().values())
        for mykey in doc.to_dict().values():
            # print(mykey)
            while (True):
                inp = input()
                if inp != mykey:
                    print('パスワードが違います。再度入力してください。')
                else:
                    print('ログイン成功')
                    # 何かしらの関数
                    print(myprint(inp))
                    listing()
                    
                    break



def myprint(a):
    return 'Hello '+a+' !'

def set_driver(driver_path, headless_flg):
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
    # options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)


def listing():

    FIST_URL = "https://fril.jp/"
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
    login_button_get = driver.find_element_by_xpath("//li[@class='loginMenu__listItem']/a[@class='button button--NoBorderSmall ga-class ga-login-button ga-guest']")
    
    time.sleep(10)
    print(login_button_get.text)
    login_url = login_button_get.get_attribute("href")
    # print(login_url)
    driver.get(f'{login_url}')
    time.sleep(10)

    # mailアドレスの所と、パスワードのところの要素をとってくる機能
    # その要素に特定の値を書きこむ関数

    # ある状態になるまで（今回は画像認証が終わるまで＝＝次の画面に行く）待機する関数
    

if __name__ == "__main__":
    main()