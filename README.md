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

![alt text](https://github.com/yossigolan/data-mining-project/blob/yossi_branch/MiningProject.png?raw=true)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
Free to use :)
