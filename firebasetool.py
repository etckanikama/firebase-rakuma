import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from base64 import a85encode
import os
from pandas.core.algorithms import mode
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
    # IMG_PATH = 'C:\\Users\\hirayama\\src\\firebase-rukuma\\img\\dog.jpg'
    
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


    df = pd.read_csv("./custom.csv")
    for i in range(len(df)):
        driver.get(FIST_URL)
        time.sleep(2)
        
        # 何がsend_keysに入るかわからんからいったんこのまま
        driver.find_element_by_id("image_tmp").send_keys(*list(df["画像url"])[i:i+1])
        time.sleep(2)
        driver.find_element_by_id("name").send_keys(*list(df["商品タイトル"])[i:i+1])
        time.sleep(2)
        driver.find_element_by_id("detail").send_keys(*list(df["商品説明"])[i:i+1])
        # time.sleep(2)

        # カテゴリのところ
        driver.find_elements_by_link_text("指定なし")[0].click()
        time.sleep(1)
        driver.find_element_by_link_text(*list(df["カテゴリ1"])[i:i+1]).click()
        driver.find_element_by_link_text(*list(df["カテゴリ2"])[i:i+1]).click()
        time.sleep(1)
        driver.find_element_by_link_text(*list(df["カテゴリ3"])[i:i+1]).click()
        time.sleep(1)
        # サイズ指定(上で指定なしが消えるからまた0番目になる→要素一つでいいような気がするけど)
        # driver.find_elements_by_link_text("指定なし")[0].click()
        # time.sleep(1)
        # 洋服はあり得ない
        # driver.find_element_by_link_text("S").click()


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
        driver.find_element_by_id("sell_price").send_keys(int(*list(df["金額"])[i:i+1]))
        time.sleep(2)
        driver.find_element_by_id("confirm").click()
        time.sleep(1)
        driver.find_element_by_id("submit").click()
        # 一番上のurlと出品した時点の日付を取得してcsvに書きこみ
        time.sleep(2)
        sell_time = datetime.datetime.today()
        detail_url = driver.find_element_by_class_name("media-left").find_element_by_tag_name("a").get_attribute("href")
        print(detail_url)
        time.sleep(2)
        write_csv(sell_time,detail_url)
        # urlだけ保持しておくなら開く必要はない。
        # driver.get(f'{detail_url}')
        
        print("終了")
        if i==0:
            break

@eel.expose
def nesage():
    



    # driverの起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)


   
    # log.csvを読み込み
    df = pd.read_csv("./url_data_log.csv")
    # 商品の詳細urlを開く
    # このとき例外があるはず。→データがない時とか
    # 
    # a=出品した時のログ商品期日を確認
    # b=現在の日付を確認
    # aとbを比較→n日 or n時間
    #  # x,yはあとで変更できるようにする？？
    # if (n＞x日以上){
    # → 詳細url内の金額情報を取得（スクレイピング）→intに変換
    # →金額情報とurl情報をcsvから削除
    # →商品の値段をy%下げる
    # →下げた値段でsend_keys
    # →更新ボタンを押す
    # →再度urlと期日をcsvに書きこみ
    # →
    # }
    # 
    # 
    # 
    # elseならスルーする→次の商品urlを開く


    pass

def write_csv(sell_time,detail_url):
    to_str = str(sell_time)
    sell_time = to_str.replace('.','')
    colum = ['出品期日','商品URL']
    df = pd.DataFrame([[sell_time,detail_url]])
    df.to_csv("url_date_log.csv",index=False,mode='a',header=False)

# if __name__ == "__main__":
#     login()