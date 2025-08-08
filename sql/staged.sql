-- staged canadian antibody
CREATE TABLE IF NOT EXISTS silver.ca_antibody AS
SELECT
    "_record_id" AS id,
    REF_DATE,
    DGUID,
    "Measure",
    "Sex at birth",
    "Age group",
    "Characteristics",
    VECTOR,
    COORDINATE,
    VALUE AS PERCENT,
    CASE
        WHEN STATUS = 'x' THEN 'suppressed to meet the confidentiality requirements of the Statistics Act'
        WHEN STATUS = 'E' THEN 'use with caution'
        ELSE STATUS
    END AS DATA_QUALITY_RATING
FROM bronze.ca_antibody_raw
WHERE GEO = 'Canada';

-- staged canadian rapid test demand
CREATE TABLE IF NOT EXISTS silver.ca_rapidtestdemand AS
SELECT
    "_record_id" AS id,
    REF_DATE,
    DGUID,
    "North American Industry Classification System (NAICS)",
    "COVID-19 rapid test kits demand and usage",
    VECTOR,
    COORDINATE,
    VALUE as PERCENT,
    CASE
        WHEN STATUS = 'A' THEN 'excellent'
        WHEN STATUS = 'B' THEN 'very good'
        WHEN STATUS = 'C' THEN 'good'
        WHEN STATUS = 'D' THEN 'acceptable'
        WHEN STATUS = 'E' THEN 'use with caution'
        WHEN STATUS = 'F' THEN 'too unreliable to be published'
        WHEN STATUS = '..' THEN 'not available for reference period'
        ELSE STATUS
    END AS DATA_QUALITY_RATING
FROM bronze.ca_rapidtestdemand_raw
WHERE GEO = 'Canada';

-- staged UK COVID cases by day
CREATE TABLE IF NOT EXISTS silver.uk_covcasesbyday AS
SELECT
    "_record_id" AS id,
    STRPTIME("date", '%Y-%m-%d')::DATE AS "date",
    "epiweek",
    "metric_value"::INTEGER AS "daily_case_count"
FROM bronze.uk_covcasesbyday_raw;

-- staged US death counts
CREATE TABLE IF NOT EXISTS silver.us_deathcounts AS
SELECT
    "_record_id" AS id,
    "year",
    "month",
    "group",
    "subgroup1",
    "subgroup2",
    "COVID_deaths" AS "covid_deaths",
    "crude_COVID_rate" AS "crude_covid_death_rate",
    "aa_COVID_rate" AS "age_adjusted_covid_death_rate",
    "crude_COVID_rate_ann" AS "annualized_crude_covid_death_rate",
    "aa_COVID_rate_ann" AS "annualized_age_adjusted_covid_death_rate",
    "footnote"
FROM bronze.us_deathcounts_raw
WHERE "jurisdiction_residence" = 'United States';

-- staged API MetaData
CREATE TABLE IF NOT EXISTS silver.api_metadata AS
SELECT
    "_record_id" AS id,
    dataset_id,
    country,
    dataset_name,
    description,
    last_updated
FROM bronze.api_metadata_raw;