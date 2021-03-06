# WheresMyVideoCard
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)  
WheresMyVideoCard (WMVC) is a simple script used to monitor the online stock avaliablity of video cards from
popular online electronics retailers.  
So far it's just for personal use.  

## Supported online electronics retailers

- [**BestBuy**](https://www.bestbuy.ca/en-ca)
- [**NewEgg**](https://www.newegg.ca/)
- [**PCCanada**](https://www.pc-canada.com/)


## Installation

`pip install -r requirements.txt`

## Run

- Add the website of the product you would like to monitor into `web_list.csv`
some examples are given in the csv file already.
- Run `run.bat` file.
- Once the monitor found the product is in stock, you should hear 3 sweeping sound.
- You can adjust the server params in `wmvc.py`

## Updates

#### v0.1.3 (Mar.05.2021)
- Add query of bitcoin price every time the program starts.
- Add WMVC support to PCCanada

#### v0.1.2 (Mar.04.2021)
- Fix an Runtime bug when the information is loaded not as expected.
- Add auto configure functionality, now users can just add url to the csv without providing
web_type and entry_name.
- Fix a lot of other Runtime issues when things went bad.

#### v0.1.1 (Mar.03.2021)
- Implement the run script, now WMVC monitor can run without IDE (...).
- Fix some naming issue.

#### v0.1 (Mar.02.2021)
- Implement the basic framework for WMVC.
- WMVC now supports reading from BestBuy and NewEgg.
- You can load new entries by adding them to 'web_list.csv'.


## License

This project is released under the [Apache 2.0 license](LICENSE).

## Contact

This repo is developed and maintained by Han Zhou ([@albat3ross](https://github.com/albat3ross))

