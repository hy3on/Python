from selenium import webdriver
from bs4 import BeautifulSoup
import sys

driver = webdriver.Chrome('C:\chromedriver.exe')#크롬 드라이버
driver.get('https://nid.naver.com/nidlogin.login')#네이버 로그인페이지
delay = 3# 3초 딜레이 주기
driver.implicitly_wait(delay)

driver.find_element_by_name('id').send_keys(sys.argv[1])#id 인자로 받기
driver.find_element_by_name('pw').send_keys(sys.argv[2])#pw 인자로 받기
driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()#버튼 클릭


driver.get('https://mail.naver.com')#메일 페이지이동
driver.implicitly_wait(delay)

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')#메일페이지 소스 긁어오기

Maillist = soup.select('ol.mailList > li > div.mTitle > div.subject > a > span.text > strong.mail_title')#메일리스트(제목) 가져오기

for n in Maillist:#출력
    print("\n")
    print(n.text.strip())

driver.close()#드라이버 종료
