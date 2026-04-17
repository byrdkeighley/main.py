from playwright.sync_api import sync_playwright
import time
import os
from twilio.rest import Client

TEST_MODE = True
send_text("✅ TEST ALERT: Ticket bot is working and SMS is connected.")

URL = "https://www.ticketmaster.com/event/0E006441FD01CA39"
MAX_PRICE = 315

# Twilio credentials (from Railway env vars)
client = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_AUTH"])

TO_NUMBER = os.environ["TO_NUMBER"]
FROM_NUMBER = os.environ["FROM_NUMBER"]

def send_text(msg):
    client.messages.create(
        body=msg,
        from_=FROM_NUMBER,
        to=TO_NUMBER
    )

def check_tickets(page):
    page.goto(URL, timeout=60000)
    page.wait_for_timeout(5000)

    content = page.content().lower()

    # Basic filtering (safe starting point)
    if "standard ticket" in content or "verified resale" in content:
        if "$3" in content or "$2" in content:  # catches under 315 range
            send_text(f"🚨 Tickets possibly available under $315!\n{URL}")
            return True
    return False

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    last_alert = 0

#    while True:
  #      try:
    #        found = check_tickets(page)

            # prevent spam (1 alert per 5 min max)
     #       if found:
     #           now = time.time()
       #         if now - last_alert > 300:
       #             last_alert = now
print("Test run complete")
        except Exception as e:
            print("Error:", e)

        time.sleep(20)
