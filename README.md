# CMP-Mining : CoinMarketCap Data Mining Project
Project by: Aviad (rikicodes@gmail.com) & Yossi Golan (yossigolan@gmail.com)

CMP-M is a data mining project, done on popular CoinMarketCap site, one of the most popular crypto-ecosystems sites.
The project offers a method of mining data about crypot-coins which are listed on CMP.

Right now the project is in develop and offers only some of its features.

### Features:
- printing iformation and details for each coin listed in MCP. The information includes short info + statistics of the coin market including prices.

## Installation

The project runs on python3.
To use the code, download the code .py file and run it using python3.
See requirements.txt for list of packages needed to run the code.

```bash
pip install -r requirements.txt 
```

## Usage

Call the function get_coin_info(coin_name) with a coin name.
Currently, the following coins are supported:

- bitcoin
- ethereum
- tether
- binance-coin
- cardano
- dogecoin
- xrp
- usd-coin
- polkadot-new
- uniswap
- litecoin
- solana
- theta

### How the function works?

First it will create the url out of https://coinmarketcap.com/currencies/ and add the coin name to it. 
eg:bitcoin - https://coinmarketcap.com/currencies/bitcoin/.

Then it will scrap the information on the page and display it on the screen.

### DB Documentation

## ERD:

![alt text](https://github.com/yossigolan/data-mining-project/blob/yossi_branch/MiningProject%20.png?raw=true)

DataBase name: crypto

Table coins include these columns:
                   "id INT AUTO_INCREMENT PRIMARY KEY," 
                   "name VARCHAR,"
                   
Table coin_price_today include these columns:
                   "id INT AUTO_INCREMENT PRIMARY KEY," 
                   "coin_id INT," 
                   "price FLOAT," 
                   "price_change FLOAT," 
                   "low FLOAT," 
                   "high FLOAT," 
                   "volume FLOAT," 
                   "volume_market_cap FLOAT," 
                   "market_dominance FLOAT," 
                   "market_cap FLOAT," 
                   "fully_diluted_market_cap FLOAT," 
                   "rank INT," 
                   "data_summery VARCHAR," 
                   
Table coin_price_yesterday include these columns:
                   "id INT AUTO_INCREMENT PRIMARY KEY," 
                   "coin_id INT," 
                   "price FLOAT," 
                   "low FLOAT," 
                   "high FLOAT," 
                   "open FLOAT," 
                   "close FLOAT," 
                   "change FLOAT," 
                   "volume FLOAT,"              

Table coin_price_history include these columns:
                   "id INT AUTO_INCREMENT PRIMARY KEY," 
                   "coin_id INT," 
                   "7d_low FLOAT," 
                   "7d_high FLOAT," 
                   "30d_low FLOAT," 
                   "30d_high FLOAT," 
                   "90d_low FLOAT," 
                   "90d_high FLOAT," 
                   "52w_low FLOAT," 
                   "52w_high FLOAT," 
                   "all_time_low FLOAT," 
                   "all_time_high FLOAT," 
                   "roi FLOAT," 
                   "circulating_supply INT," 
                   "total_supply INT," 
                   "max_supply INT," 

Table coin_information include these columns:
                   "id INT AUTO_INCREMENT PRIMARY KEY," 
                   "info VARCHAR," 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
Free to use :)
