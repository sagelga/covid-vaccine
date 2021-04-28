# COVID-19 Data Explorer
COVID-19 Data Explorer is a dashboard-data explorer for COVID-19 data around the world; running on Python using Plotly/Dash framework.

- Health Data 
  - Pulled from Our World in Data [https://github.com/owid/covid-19-data/](https://github.com/owid/covid-19-data/)
- Vaccine Purchase &  Manufacturing Arrangements data 
  - Pulled from Graduate Institute [https://www.knowledgeportalia.org/covid19-vaccine-arrangements](https://www.knowledgeportalia.org/covid19-vaccine-arrangements)
    - Data is manually pulled and converted to `.csv`.
- Mobility Trends
  - Apple Mobility Trends Reports from [https://covid19.apple.com/mobility](https://covid19.apple.com/mobility)
  - Google Community Mobility Trends Reports from [https://www.google.com/covid19/mobility/](https://www.google.com/covid19/mobility/)
  - Waze COVID-19 Impact Reports [https://www.waze.com/covid19](https://www.waze.com/covid19)
  - Tom Tom Traffic Index Reports [https://www.tomtom.com/en_gb/traffic-index/](https://www.tomtom.com/en_gb/traffic-index/)
    - Pulled from Processed data source : [https://github.com/ActiveConclusion/COVID19_mobility](https://github.com/ActiveConclusion/COVID19_mobility)

## Deployment
Repository development deliverables will be automatically deployed to Heroku after merge/push commit.

Official version is available on [covid.sagelga.com](http://covid.sagelga.com)

For bleeding-edge website, we also hosted on [dev.covid.sagelga.com](http://dev.covid.sagelga.com/).

## Project Roadmaps
We stored roadmaps here : [https://github.com/sagelga/covid-vaccine/projects](https://github.com/sagelga/covid-vaccine/projects)
## Develop
To locally develop this project, here's what you need 
1. Python >= 3.6
2. Python Virtual Environment (venv) (Strongly Recommended)
3. IDE or Text Editor you are familiar with
4. Modern Internet Browser (i.e. Google Chrome (or Chromium-based Browser), Mozilla Firefox, Apple Safari)

### Installation
1. Install the required packages
    ``` bash
    pip3 install -r requirements.txt
    ```
2. then run the app using
    ``` bash
    python index.py
    ```
3. Your app will run in `localhost` and `debug` mode. Please refer to Plotly/Dash documentation for more detail.

### Directory
For maintenance
- `.vscode` for VSCode automation and configurations
- `LICENSE` for legal things

## Contributor
![Contributor bubble](https://contrib.rocks/image?repo=sagelga/covid-vaccine)

## Donations
If you like to support us via donation, please leave a donations here : [https://commerce.coinbase.com/checkout/aed305a0-d6ae-4d98-b993-b1e85e0a99f6](https://commerce.coinbase.com/checkout/aed305a0-d6ae-4d98-b993-b1e85e0a99f6)

All of the donations goes to fund Operation (and soon the future) cost.

---

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/contains-cat-gifs.svg)](https://forthebadge.com)