-- Connect to the db, not the catalog

-- Load extensions
LOAD ducklake;

-- Attach your DuckLake
ATTACH 'ducklake:/Users/michaelgalo/Workspace/data-engineering/projects/ducklake-marvan-pipeline/catalog.ducklake'
AS my_ducklake (DATA_PATH '/Users/michaelgalo/Workspace/data-engineering/projects/ducklake-marvan-pipeline/data');

USE my_ducklake;

-- Now you can query your tables
SELECT * FROM gold.us_deathcounts