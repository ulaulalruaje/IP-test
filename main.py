import undetected_chromedriver as uc
from time import sleep
from os import path
import requests, zipfile, os

try: __file__
except: __file__ = os.getcwd()

base_dir=path.dirname(path.abspath(__file__))
ext_file=path.join(base_dir, 'ext.crx')
ext_dir=path.join(base_dir, 'ext')
prext_dir=path.join(base_dir, 'pr_ext')

PROXY = 'http://73738zbpcibedc0-session-jrndridneidbw-lifetime-20:okjz6fk9nkkx3rc@rp.proxyscrape.com:6060'

if PROXY:
    up, hp = PROXY.replace('http://','').replace('https://','').split('@')
    username, password = up.split(':')
    host, port = hp.split(':')
    
    try:
        os.mkdir(prext_dir)
    except FileExistsError:
        pass
    
    manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Proxies",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
    """
    
    background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };
    
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
    
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
    """ % (host, port, username, password)
    
    with open(path.join(prext_dir, "manifest.json"), 'w') as m_file:
        m_file.write(manifest_json)
    with open(path.join(prext_dir, "background.js"), 'w') as b_file:
        b_file.write(background_js)




options = uc.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-notifications')
options.add_argument("--remote-debugging-port=9222")
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')

with open(ext_file, 'wb') as f:
    f.write(requests.get('https://archive.org/download/ext_20231006/ext.crx').content)
with zipfile.ZipFile(ext_file, 'r') as zip:
    zip.extractall(ext_dir)

if PROXY:
    options.add_argument(f'--load-extension={ext_dir},{prext_dir}')
else:
    options.add_argument(f'--load-extension={ext_dir}')

driver = uc.Chrome(options=options)

driver.maximize_window()
driver.execute_script('window.open("https://vzu.us")')

sleep(30)

driver.switch_to.window(driver.window_handles[1])
if not 'LoanOrHost' in driver.page_source:
        raise Exception('30sec passed but captcha couldn\'t solve.')

user_agent = driver.execute_script("return navigator.userAgent;")
cf_clearance = ''

for c in driver.get_cookies():
    if c['name'] == 'cf_clearance':
        cf_clearance = c['value']

print(user_agent)
print(cf_clearance)
driver.quit()


# Done
