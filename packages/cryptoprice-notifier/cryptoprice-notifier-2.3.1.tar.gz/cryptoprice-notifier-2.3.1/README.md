# cryptoprice-notifier
![Bitcoin](https://www.pngitem.com/pimgs/m/520-5207199_cryptocurrency-ethereum-blockchain-altcoins-bitcoin-cryptocurrency-png-transparent.png)

__This is a python script that notify crypto currency price regularly on email, telegram, and IFTTT app notifications. It provide a response after a certain time interval which you can specify. By default time interval and threshold price is set to 5 in minutes and Rs.1000000 respectively. The user has option to choose Where he want to recieve updates.__

# DESCRIPTION
__*Crypto Currency price is very flactuating. So why not be get updated regulary and instead of checking the price , this package will make sure you get notified of the Price Change On time.*__

<ul>
  <li>We Have Implemented Price + News Notifications of crypto currency.</li>
  <li>And Also To make sure that you get High Priority alert if price reach a certain lower level we have integrated email service which will send a email to you once price goes above the threshold price</li>
  <li>Our Python Package will make an HTTP request to the webhook URL which will trigger an action.</li>
  <li>We Getting The Price Update From coinmarketcap API and news updates from NEWS API</li>
</ul>

## Project Overview:
•	This Project will send notification of bitcoin latest price for every one hour.
•	The notifications will be sent to telegram channel “AttainU Bitcoin IFTTT”.
•	The channel is global and anyone can access the channel and get regular updates of bitcoin prices. 


## Features: 
•	Anyone with the link can join and chat along the channel.
•	Will Update news over twitter handle
•	And also if the price is greater than the threshold price it will send a notification on email



## Working Procedure:
  -	Parse Command line arguements
  -	Get Crypto Price And Crypto News
  -	Format The Data
  -	Send Data to IFTTT 

## Modules:
•	The Project is Divided into Six Modules:
  -	Main Module :- To parse command line arguement
  -	Get Data Module :- To Collect Price and news from api
  -	Format Data Module :- to format price data recieved
  -	Notification Module : to send price and news update
  - Emergency Update Module :- To send email update for alert price
  - config module :- Where all the configuration file are available

## IFTTT Applets:
  -	Webhooks and Telegram & Twitter services  are used here. 
  -	When an event is occurred in the webhooks it will send the event value to telegram
  - And Also A news Update Is being sent to twitter

## Prerequisite

  - Python3 & PIP
  - Telegram App  <a href="https://t.me/projectcomplete"> Click Here To Join</a> 
  - Twitter, For news Updates <a href="https://twitter.com/BitcoinUpdate2"> Click Here to Follow</a> 
  - An email account for emergency price alert
   
### Installation

Install cryptoprice-notifier package using PIP,
```sh
pip install cryptoprice-notifier 
```
For Help Menu
```
cryptonotifier --help
```
you will see a Response like this
```

usage: cryptonotifier [-h] [-a alert_price] [-t time_interval]
               [-l resp_limit resp_limit] [-c coin] [-d destination]
               [-cur curr]

Crypto Price Notify App.

optional arguments:
  -h, --help            show this help message and exit
  -a alert_price, --alert_price alert_price
                        threshold price of coin, default is ₹1000000
  -t time_interval, --time_interval time_interval
                        interval between entries, default is 60 min
  -l resp_limit resp_limit, --resp_limit resp_limit resp_limit
                        No. Of record and time gap between record in Single
                        Response, default 5record and 20sec time gap
  -c coin, --coin coin  For Selecting a Crypto Coin : -c btc/xrp/eth
  -d destination, --destination destination
                        Select a Destination : -d telegram/ifttt
  -cur curr, --currency curr
                        For Selecting a Currency : -cur INR/USD/GBP/EUR

Welcome To crypto price notify app by Anurag Gothi


```
to run the app type the following command
```
cryptonotifier -a 250 -t 60 -l 5 20 -d telegram -c eth -cur USD
```
*  -a : alert limt amount in CURRENCY YOU SELECT
*  -t : time interval in Seconds
*  -l : No of entries and timegap between entries per response
* -d : For destination app like IFTTT App / Telegram 
* -c : For crypto currency Like ETH/BTC/XRP
* -cur : For selecting a currency INR/USD/GBP/EUR


##### Author: Anurag Gothi.
