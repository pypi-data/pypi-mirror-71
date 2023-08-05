
# Web Scraper of COVID-19 data for Czechia

Python package [covid19czechia](https://pypi.org/project/covid19czechia/) provides access to COVID-19 data of Czechia.

The data is scraped from

* Ministery of Health, Czech Republic
* Czech Statistical Office

## Setup and usage

Install from [pip](https://pypi.org/project/covid19czechia/) with

```python
pip install covid19czechia
```

Importing module is done such as

```python
import covid19czechia as CZ

x = CZ.covid_deaths()
```

Package is regularly updated. Update with

```bash
pip install --upgrade covid19czechia
```