# WheresMyVideoCard
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)  
WheresMyVideoCard (WMVC) is a simple script used to monitor the online stock avaliablity of video cards from
popular online electronics retailers.  
So far it's just for personal use.  

## Installation

`pip install -r requirements.txt`

## Run

- add the website of the product you would like to monitor into `web_list.csv`,
some example is given in the file already.
- run `run.bat` file
- Once the monitor found the product in stock, you should hear 3 sweeping sound.

## Updates

#### v0.1.1 (Mar.03.2021)
- Implement the run script, now WMVC monitor can run without IDE (...)
- Fix some naming issue

#### v0.1 (Mar.02.2021)
- Implement the basic framework for WMVC
- WMVC now supports reading from BestBuy and NewEgg
- You can load new entries by adding them to 'web_list.csv'


## License

This project is released under the [Apache 2.0 license](LICENSE).

## Contact

This repo is currently maintained by Han Zhou ([@albat3ross](https://github.com/albat3ross))

