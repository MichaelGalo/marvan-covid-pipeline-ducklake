-- antibody
CREATE TABLE IF NOT EXISTS gold.ca_antibody AS
SELECT
    id,
    REF_DATE,
    DGUID,
    "Measure",
    "Sex at birth",
    "Age group",
    "Characteristics",
    VECTOR,
    COORDINATE,
    PERCENT,
    DATA_QUALITY_RATING,
    CURRENT_TIMESTAMP AS LAST_UPDATED
FROM silver.ca_antibody;

-- rapid test demand
CREATE TABLE IF NOT EXISTS gold.ca_rapidtestdemand AS
SELECT
    "id",
    REF_DATE,
    DGUID,
    "North American Industry Classification System (NAICS)",
    "COVID-19 rapid test kits demand and usage",
    VECTOR,
    COORDINATE,
    PERCENT,
    DATA_QUALITY_RATING,
    CURRENT_TIMESTAMP AS LAST_UPDATED
FROM silver.ca_rapidtestdemand;

-- UK COVID cases by day
CREATE TABLE IF NOT EXISTS gold.uk_covcasesbyday AS
SELECT
    "id",
   "date",
   "epiweek",
   "daily_case_count",
    CURRENT_TIMESTAMP AS LAST_UPDATED
FROM silver.uk_covcasesbyday;

-- US death counts
CREATE TABLE IF NOT EXISTS gold.us_deathcounts AS
SELECT
    "id",
    "year",
    "month",
    "group",
    "subgroup1",
    "subgroup2",
    "covid_deaths",
    "crude_covid_death_rate",
    "age_adjusted_covid_death_rate",
    "annualized_crude_covid_death_rate",
    "annualized_age_adjusted_covid_death_rate",
    "footnote",
    CURRENT_TIMESTAMP AS LAST_UPDATED
FROM silver.us_deathcounts;

-- api metadata
CREATE TABLE IF NOT EXISTS gold.api_metadata AS
SELECT
    dataset_id,
    country,
    dataset_name,
    description,
    last_updated
FROM silver.api_metadata;