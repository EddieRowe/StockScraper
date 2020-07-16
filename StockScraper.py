import requests
from bs4 import BeautifulSoup
import time
from tkinter import *

# init Tkinter
root = Tk()
root.geometry("350x75")
root.title("Stock Scraper")
frame = Frame(root)
frame.pack()

label = Label(frame, text = "Current Value")
label.pack()
label1 = Label(frame, text = "Change Today")
label1.pack()
label2 = Label(frame, text = "Last Update")
label2.pack()

# Set url to scrape data from
url = 'https://www.hl.co.uk/shares/shares-search-results/v/vanguard-funds-plc-ftse-100-ucits-etf-gbp'

# Init timer for updates
timer = 0
timeOrigin = time.perf_counter()

def doUpdate():
    
    # Connect
    response = requests.get(url)
    
    # Convert to BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Scrape the data we want
    stockPrice = soup.find(id="ls-ask-VUKE-L").string
    dayChange = soup.find(id="ls-perc-VUKE-L").string

    # The website uses lots of weird whitespace
    dayChange = dayChange.strip() 
    
    # Update UI
    label.configure(text = 'Current Value: ' + stockPrice)
    label1.configure(text = 'Change Today: ' + dayChange)
    
    # Reset timer
    timer = 0
    timeOrigin = time.perf_counter()

# Initial scrape
doUpdate()

while True:
    
    timer = time.perf_counter() - timeOrigin
    label2.configure(text = 'Last update: ' + str(int(round(timer/60))) + ' mins ago.')
    
    # Run doUpdate every 15 minutes
    if timer >= 900:
        timer = 0
        timeOrigin = time.perf_counter()
        doUpdate()
    
    # This isn't the proper way of doing it
    # Should use mainloop() but need to learn more!
    root.update_idletasks()
    root.update()
    # Update every 30s
    time.sleep(30)
