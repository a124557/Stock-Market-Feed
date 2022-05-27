# Requests allows us to retrieve data from a webpage, and BeautifulSoup allows us to extract specific data
import tkinter

import requests
from bs4 import BeautifulSoup
from tkinter import *
import ctypes
from threading import Timer

# Using ctypes to improve resolution
ctypes.windll.shcore.SetProcessDpiAwareness(1)

root = Tk()
root.title("Stock Scraper")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}

# Create title
title = Label(root, text="Stock Market Feed", font=("Arial", 20))

# Textbox label
stockName = Label(root, text="Enter Ticker Symbol:")

# Add Textbox
t = Text(root, height=1, width=20)

bold = '\33[1m'


def clicked():
    userInput = t.get("1.0", END)
    userInput.strip()
    names = []
    temp = ""
    i = 0
    while i < len(userInput):
        if userInput[i] == " ":
            i += 1
        elif userInput[i] == "," or userInput[i] == "-" or i == len(userInput) - 1:
            if temp == "":
                i += 1
            else:
                names.append(temp.upper())
                temp = ""
                i += 1
        else:
            temp += userInput[i]
            i += 1

    a = 0
    stockItems = []
    while a < len(names):
        url = 'https://ca.finance.yahoo.com/quote/' + names[a]
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        # Add stock title
        stockTitle = soup.find('h1', {'class': 'D(ib) Fz(18px)'}).text
        openPrice = soup.find('td', {'class': 'Ta(end) Fw(600) Lh(14px)'}).text
        price = soup.find('fin-streamer', {'data-symbol': names[a]}).text
        daysRange = soup.find('td', {'data-test': 'DAYS_RANGE-value'}).text
        fiftyTwoRange = soup.find('td', {'data-test': 'FIFTY_TWO_WK_RANGE-value'}).text
        forwardDividend = soup.find('td', {'data-test': 'DIVIDEND_AND_YIELD-value'}).text
        exDividend = soup.find('td', {'data-test': 'EX_DIVIDEND_DATE-value'}).text

        stockItems.append("                \nTicker: " + stockTitle + "\n\n" +
                          "           Opening Price: " + openPrice + "\n" +
                          "           Current Price: " + price + "\n" +
                          "             Day's Range: " + daysRange + "\n" +
                          "           52 Week Range: " + fiftyTwoRange + "\n" +
                          "Forward Dividend & Yield: " + forwardDividend + "\n" +
                          "        Ex-Dividend Date: " + exDividend + "\n")
        a += 1

    stockBox.delete('1.0', END)
    for x in stockItems:
        stockBox.insert(INSERT, x)
    Timer(5, clicked).start()


# Add button
btn = Button(root, text="Check", command=clicked)

# Order Elements

title.place(x=280, y=10)
stockName.place(x=220, y=100)
t.place(x=500, y=100)
btn.place(x=900, y=85)

stockBox = Text(root, height=60, width=50)
stockBox.place(x=140, y=180)

# Window size
root.geometry('900x1500')

# Create main loop
root.mainloop()
