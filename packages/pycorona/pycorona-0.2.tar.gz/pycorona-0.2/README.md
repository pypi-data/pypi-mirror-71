# pycorona
pycovid is a library that is used to get coronavirus condition (i.e. active cases, deaths, etc) of any country.

# Usage

    from pycovid import Country<br>
    country = Country("USA")<br>
    cases = country.total_cases()<br>
    print(cases)<br>
> **__2,234,475__**

Attributes available -<br>
    continent()<br>
    flag()<br>
    total_cases()<br>
    today_cases()<br>
    total_deaths()<br>
    today_deaths()<br>
    recovered()<br>
    critical_cases()<br>
    active_cases()<br>
    tests()<br>

Note - This package is currently under development