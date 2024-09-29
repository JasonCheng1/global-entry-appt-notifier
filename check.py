import time
import subprocess

PHONE_NO = "" # TODO import from .env

OASSCRIPT_TEMPLATE = f"""osascript -e 'tell application "Messages" to send "{{message}}" to buddy "{{phone_no}}"'"""


while True:
    cmd = OASSCRIPT_TEMPLATE.format(message="你好， 我是🐼!",  phone_no=PHONE_NO)
    subprocess.run(cmd, shell=True)
    print(f"Successfully sent {cmd}")
    time.sleep(60)