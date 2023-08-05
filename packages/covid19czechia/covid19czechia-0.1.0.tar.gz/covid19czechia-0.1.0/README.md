
# Web Scraper of COVID-19 data for Czechia

Python package [covid19czechia](https://pypi.org/project/covid19czechia/) provides access to COVID-19 data of Czechia.

The data is scraped from

* Ministry of Health, Czech Republic
* Czech Statistical Office

## Setup and usage

Install from [pip](https://pypi.org/project/covid19czechia/) with

```python
pip install covid19czechia
```

Importing module is done such as

```python
import covid19czechia as CZ

x = CZ.deaths_covid()
```

Package is regularly updated. Update with

```bash
pip install --upgrade covid19czechia
```

## COVID-19 Deaths

Get Covid-19 deaths in Czechia (weekly counts, by gender and age group)

```python
x = CZ.deaths_covid()
```

The function returns Pandas dataframe. It can be stored to csv file with

```python
x.to_csv("filename.csv", header = True, index = False)
```

### Administrative unit setting

Optional parameter `level` sets granularity of administrative units
the deaths are computed in.

Defaultly (`level = 1`) the deaths are taken from the whole Czechia.

```python
x = CZ.deaths_covid(level = 1) # same as no argument given (above)
```

Settings `level = 2` corresponds with deaths in regions (*kraje*, NUTS 3).

```python
x = CZ.deaths_covid(level = 2)
```

Setting `level = 3` means deaths per district (*okresy*, LAU 1).

```python
x = CZ.deaths_covid(level = 3)
```

Read more about administrive units of Czech Republic
[here](https://en.wikipedia.org/wiki/NUTS_statistical_regions_of_the_Czech_Republic).

## Total weekly deaths

**TODO**

