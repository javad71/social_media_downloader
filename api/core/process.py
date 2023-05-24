import requests
import json

from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def download_from_linkedin(post_link=None):
    try:
        # Prompt user for LinkedIn credentials and post link
        username = "javad.rezaei1371@gmail.com"
        password = "javad891"

        # Log in to LinkedIn
        session = requests.session()
        login_url = 'https://www.linkedin.com/login'
        login_page = session.get(login_url)
        soup = BeautifulSoup(login_page.content, 'html.parser')
        csrf_token = soup.find('input', {'name': 'loginCsrfParam'}).get('value')
        login_data = {'session_key': username, 'session_password': password, 'loginCsrfParam': csrf_token}
        session.post(login_url, data=login_data)

        # Send request to post page
        post_page = session.get(post_link)

        # Parse HTML content with BeautifulSoup
        soup = BeautifulSoup(post_page.content, 'html.parser')

        # Extract desired information
        author_name = soup.find('a', {'class': 'text-sm link-styled no-underline leading-open'}).text.strip()
        author_headline = soup.find('p', {
            'class': 'attributed-text-segment-list__content text-color-text !text-sm whitespace-pre-wrap break-words'}).text.strip()
        post_content = soup.find('div',
                                 {'class': 'attributed-text-segment-list__container relative mt-1 mb-1.5'}).text.strip()

        # Find the video player element and extract the video URL
        video_tag = soup.find('video', {'class': 'share-native-video__node video-js'})
        tag_string = video_tag['data-sources']
        url_link = json.loads(tag_string)

        data = {
            'author_name': author_name,
            'post_content': post_content,
            'video_url': url_link[0]['src'],
            'status': '200'
        }
        return data
    except Exception as e:
        error = {
            'message': str(e),
            'status': '1001'
        }
        return json.dumps(error)


def download_from_instagram(post_link=None):
    opts = webdriver.FirefoxOptions()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(options=opts)
    driver.get("https://snapinsta.app/")

    try:
        url = post_link
        income = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='form-control']"))
        )
        income.send_keys(url)

        submit = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-get flex-center']"))
        )
        submit.click()

        submit = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-secondary']"))
        )
        submit.click()

        image = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//img[@alt='Preview']"))
        )

        video = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='btn download-media flex-center']"))
        )

        data = {
            'video_url': video.get_attribute('href'),
            'image': image.get_attribute('src'),
            'status': '200'
        }
        return data

    except TimeoutException:
        error = {
            'message': 'Video not found',
            'status': '1002'
        }
        return error
    finally:
        driver.quit()


def download_from_youtube(post_link=None):
    try:
        with YoutubeDL() as ydl:
            info_dict = ydl.extract_info(post_link, download=False)
            video_title = info_dict.get('title', None)
            video_url = info_dict.get("url", None)

        data = {
            'video_title': video_title,
            'video_url': video_url,
            'status': '200'
        }
        return data
    except Exception as e:
        error = {
            'message': 'Video not found',
            'status': '1003'
        }
        return error


def download_from_twitter(post_link=None):
    opts = webdriver.FirefoxOptions()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(options=opts)
    driver.get("https://ssstwitter.com/")

    try:
        url = post_link
        income = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='form-control input-lg']"))
        )
        income.send_keys(url)

        submit = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='pure-button pure-button-primary u-fw']"))
        )
        submit.click()

        videos = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH,
                                                 "//a[@class='pure-button pure-button-primary is-center u-bl "
                                                 "dl-button download_link without_watermark vignette_active']"))
        )

        data = {
            'video_url_720': videos[0].get_attribute('href'),
            'video_url_480': videos[1].get_attribute('href'),
            'video_url_240': videos[2].get_attribute('href'),
            'status': '200'
        }
        return data

    except TimeoutException:
        error = {
            'message': 'Video not found',
            'status': '1004'
        }
        return error
    finally:
        driver.quit()


def download_from_tiktok(post_link=None):
    opts = webdriver.FirefoxOptions()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(options=opts)
    driver.get("https://snaptik.app/")

    try:
        url = post_link
        income = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='link-input']"))
        )
        income.send_keys(url)

        submit = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='button button-go is-link']"))
        )
        submit.click()

        video1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='button download-file']"))
        )

        video2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='button download-file is-secondary mt-3']"))
        )

        # find image
        image = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[@id='thumbnail']"))
        )

        data = {
            'video_url1': video1.get_attribute('href'),
            'video_url2': video2.get_attribute('href'),
            'image': image.get_attribute('src'),
            'status': '200'
        }
        return data

    except TimeoutException:
        error = {
            'message': 'Video not found',
            'status': '1005'
        }
        return error
    finally:
        driver.quit()
