<h3 align='center'>clicov</h3>
<p align='center'>Quickly view and/or download COVID-19 case data from your Terminal.
    <br><a href='https://github.com/hhandika/clicov/issues'>Report issues</a></br>
    <br><img src='static/screenshot-2.png'></br>
</p>
<hr/>
Clicov is multi-platform command line app to track COVID-19 cases. The data are available for global and per country COVID-19 cases. The U.S cases are also available in per state basis and include positive and negative testing results.

## Installation

From github:

```
git clone https://github.com/hhandika/clicov.git
cd clicov/
pip install --editable .
```

## Usages
### Global Cases

To view summary of global cases:

```
clicov -w
```

To view summary of user selected country cases, use the command -c and add the country two-letter <a href='https://www.iban.com/country-codes'>iso2 code</a>. You can also use the country name, but iso2 codes will yield more consistent results, particularly for multi-word country names.

```
clicov -c [country-iso2-code]

#To view country iso2 codes:
clicov id

#For example, US cases:
clicov -c us

#You can chain it with global cases:
clicov -w -c us
```

To download a summary of all countries' current cases:

```
clicov summary -sv
```

Per country cases from day one is also available for download:

```
clicov download -c [country-iso2-code]
```
All files will be saved in a comma-separated values (.csv) format.

### U.S Cases

This option is available to dig dive into the U.S states' cases. You can view a summary of all states' cases in the U.S or in per state basis. The data are available for current cases and historical data for each state. For the U.S. cases in a country basis use the 'clicov summary' command instead.

To view all states' current  cases:

```
clicov usa
```

To view current cases per state:

```
clicov usa -s [state-code]

#For New York
clicov usa -s ny
```

To download all states' current cases:

```
clicov usa -sv
```

To download per state cases from day one:

```
clicov usa -s [state-code] -sv
```

## Data Providers

### Global cases

Data aggregation: https://covid19api.com/

Data sources and terms of use: <a href='https://github.com/CSSEGISandData/COVID-19'>the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University</a>

### U.S. state cases

Data aggregation and providers: <a href='https://covidtracking.com/api'>the COVID Tracking Project at the Atlantic</a>

Learn more about the data: https://covidtracking.com/data

Terms of use: https://covidtracking.com/license

## License:
The app is under <a href='https://github.com/hhandika/clicov/blob/master/LICENSE'>MIT license</a>, meaning you are free to do however you want to the app. For the data usages, please refers to the terms of use provided by the data providers.

## Contributions
This project was started as a hobby project. We are welcome for anyone to contribute. Please, send pull requests on <a href='https://github.com/hhandika/clicov/pulls'>Github</a>. 
 
