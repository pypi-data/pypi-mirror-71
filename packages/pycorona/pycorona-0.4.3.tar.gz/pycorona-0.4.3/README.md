# pycorona
pycovid is a library that is used to get coronavirus condition (i.e. active cases, deaths, etc) of any country.

# Usage
```python
from pycorona import Country
    
country = Country("USA")
cases = country.total_cases()
print(cases)
> 2,234,475
```

Attributes available -
```python
continent()
flag()
total_cases()
today_cases()
total_deaths()
today_deaths()
recovered()
critical_cases()
active_cases()
tests()
```
The package raises KeyError if the given country is not found

Note - This package is currently under development