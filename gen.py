import requests,subprocess,platform
s=requests.session()
from pathlib import Path
import os
import random,time,re,binascii
#دالة توليد mc ةهمي
def getrandommc():
    mcrandom = ["a", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    mc = '{}:{}:{}:{}:{}:{}'.format("".join(random.choices(mcrandom, k=2)), "".join(random.choices(mcrandom, k=2)),
                                    "".join(random.choices(mcrandom, k=2)), "".join(random.choices(mcrandom, k=2)),
                                    "".join(random.choices(mcrandom, k=2)), "".join(random.choices(mcrandom, k=2)))
    return mc
#دالة تحديد نوع نضام
def getsystem():
    system = platform.system()
    if system.startswith("Win"):
        return "win" + platform.machine()[-2:]
    elif system.startswith("Lin"):
        return "linux" + platform.machine()[-2:]
    else:
        return "osx64"
  #اهم دالة تولد جب قصدي جهاز وتشغل ملفات java
def generate_device():
    system = getsystem()

    nativate_path = Path(__file__).resolve().parent / "Libs"
    jni_path = nativate_path / "prebuilt" / system
    
    os.chdir(nativate_path)


    gentime = str(int(time.time() * 1000))
    ud_id = str(random.randint(221480502743165, 821480502743165))
    openu_did = "".join([random.choice("0123456789abcdef")
                         for i in range(16)])
    mc = getrandommc()

    message = " ".join([gentime, ud_id, openu_did, mc])

    command = r"java -jar -Djna.library.path={} -Djava.library.path={} unidbg.jar {}".format(jni_path, jni_path, message)
    stdout, stderr = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    hex_str = re.search(r'hex=([\s\S]*?)\nsize', stdout.decode()).group(1)

    def hexStrtostr(hex_str):
        hexadecimal = hex_str.encode('utf-8')
        str_bin = binascii.unhexlify(hexadecimal)
        return str_bin

    astr = hexStrtostr(hex_str)
    return astr

url = "https://api-boot.tiktokv.com/service/2/device_register/?tt_data=a&ac=WIFI&channel=googleplay&aid=1233&app_name=musical_ly&version_code=370805&version_name=37.8.5&device_platform=android&os=android&ab_version=37.8.5&ssmix=a&device_type=SM-S908E&device_brand=samsung&language=en&os_api=28&os_version=9&openudid=d4fa1d663a7c0914&manifest_version_code=2023708050&resolution=1600*900&dpi=240&update_version_code=2023708050&_rticket=1753198336597&is_pad=0&app_type=normal&sys_region=US&last_install_time=1753198325&mcc_mnc=44010&timezone_name=Asia%2FBaghdad&carrier_region_v2=440&app_language=en&carrier_region=JP&ac2=wifi&uoo=1&op_region=JP&timezone_offset=10800&build_number=37.8.5&host_abi=arm64-v8a&locale=en-GB&region=GB&ts=1753198335&cdid=e150b6b4-a5f6-4da4-be18-d3a55c4ea097&okhttp_version=4.2.210.6-tiktok&use_store_region_cookie=1"

payload = generate_device()
headers = {
  'User-Agent': "com.zhiliaoapp.musically/2023708050 (Linux; U; Android 9; en_US; SM-S908E; Build/TP1A.220624.014;tt-ok/3.12.13.16)",

  'Content-Type': "application/octet-stream;tt-data=a",

}

response = requests.post(url, data=payload, headers=headers)

print(response.text)
if "device_id" in response.text:
    print(f"device id : {response.json()["device_id"]} | install id : {response.json()["install_id"]}")
else:
    print("error")
#code write : S1 and Loukious
