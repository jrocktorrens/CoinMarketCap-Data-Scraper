# CMP-Mining : CoinMarketCap Data Mining Project

CMP-M is a data mining project, done on popular CoinMarketCap site, one of the most popular crypto-ecosystems sites.
The project offers a method of mining data about crypot-coins which are listed on CMP.

Right now the project is in develop and offers only some of its features.

Features:
- printing iformation and details for each coin listed in MCP. The information includes short info + statistics from it's (the coin) market and prices.

## Installation

The project runs on python3.
To use the code, download the code .py file and run it using python3.
See requirements.txt for list of packages needed to run the code.

```bash
pip install -r requirements.txt 
```

## Usage

Go to https://coinmarketcap.com/currencies/ and pick a coin to be mined, eg:bitcoin - https://coinmarketcap.com/currencies/bitcoin/.
Edit the url in the code to be as your choice.
Run it.

```python
r = requests.get("https://coinmarketcap.com/currencies/bitcoin/")
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
Free to use :)
