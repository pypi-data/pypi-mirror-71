<h3 align='center'>clicov</h3>
<p align='center'>Quickly view and/or download COVID-19 case data from your Terminal.
    <br><a href='https://github.com/hhandika/clicov/issues'>Report issues</a></br>
    <br>
    <img src="https://img.shields.io/pypi/v/clicov" alt="PyPI version">
    <img src='https://img.shields.io/github/license/hhandika/clicov'>
    <img src='https://img.shields.io/pypi/pyversions/clicov'>
    <img src='https://img.shields.io/pypi/implementation/clicov'>
    <img src='https://img.shields.io/github/languages/code-size/hhandika/clicov'>
    <img src='https://img.shields.io/pypi/wheel/clicov'>
    </br>
    <!-- <br>
    <img alt='https://github.com/hhandika/clicov/blob/master/static/screenshot-2.png' src='https://github.com/hhandika/clicov/blob/master/static/screenshot-2.png'>
    </br> -->
</p>
<hr/>
Clicov is a multi-platform command-line application to track COVID-19 cases. The data are available for global and per country cases. The U.S cases are also available in per state basis and include positive and negative testing results.

## Installation

For MacOS and Linux, you could install clicov directly from pip. You may also consider to setup virtual environment using <a href='https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands'>conda</a> or <a href='https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/'>pip</a> virtual environments. To install clicov, use this command in your Terminal shell:

```
pip install clicov
```

For Windows, you could install clicov on <a href= https://docs.microsoft.com/en-us/windows/wsl/install-win10>Windows Subsystem for Linux</a>. The installation process is similar as above. Alternatively, you could also install it natively on Windows. One way to install it is using Anaconda/Miniconda. If you don't have either application yet, the instructions to install them are available <a href='https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html'>here</a>. Download Anaconda/Miniconda for python version 3.7 or above. After installation, open Anaconda command prompt. Then, install clicov by following the installation procedure for Linux and MacOS above.

## Usages
### Global Cases

To view summary of global cases:

```
clicov summary -w
```

To view summary of a selected country's cases, use the command -c and add the country two-letter <a href='https://www.iban.com/country-codes'>ISO2 code</a>. You can also use the country name, but ISO2 codes are less prone to errors, particularly for multi-word country names.

```
clicov summary -c [country-iso2-code]
```

You can check ISO2 codes using this command:

```
clicov id
```

For example, to view total U.S. cases:

```
clicov summary -c us
```

You can also chain the command with global cases:

```
clicov summary -w -c us
```

All countries' current cases can be saved into a spreadsheet:

```
clicov summary -sv
```

Cases from day one for a country is also available for download:

```
clicov download -c [country-iso2-code]
```

All files will be saved in your current working directory as a comma-separated values (.csv) format.

### U.S Cases

This option is available to dig dive into the U.S states' cases. You can view a summary of all states' cases in the U.S or in per state basis. The data are available for current cases and historical data for each state. For the total U.S. cases, use 'clicov summary -c us' command instead.

To view a list of all states' current  cases:

```
clicov usa
```

To view current cases per state:

```
clicov usa -s [state-code]
```

For example, to view New York cases:

```
clicov usa -s ny
```

To download all states' current cases:

```
clicov usa -sv
```

To download cases from day one for a selected state:

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
 
