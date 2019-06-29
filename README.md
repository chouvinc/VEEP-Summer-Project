# VEEP Internal Database Tool

Welcome to the internal database tool, a VEEP-developed piece of software used to track metrics about the club.
The application is currently under development, so please open a pull request if an issue is found, or for feature
requests.

### Table of Contents

[Schemas](#schemas)

[Pages](#pages)

[User Guide (TBD)](#user-guide-tbd)

[Known Issues (TBD)](#known-issues-tbd)

## Schemas

### Students

* Student ID
* Name
* Discipline
* Year
* Project - The name of the project they were on
* Email

### Teams

* Team Name - Name of the project OR name of the executive team
* Number of Members - # of Members on the team
* Average Year of Study
* Most Common Discipline

### Projects

* Project Name
* Client Name
* Completion Rate \[%\] - (0~100)
* Project Type - Software/Hardware/Consulting/Other

### Not-for-profits (NFPs)

* NFP Name
* Years With VEEP
* Number of Projects
* Number of Projects Completed
* Primary Email

## Pages

The tool has a couple pages that users can use:

1) Database/Table search and display tool - lists all of the rows of a table by default and then paginates them.
We should probably consider limiting the number of results loaded and pull records based on proximity to current page.
2) Summaries - lists a couple of the more important metrics of each table (mean, median, avg, IQR, std. dev.)
3) Visualization - pretty graphs and charts
4) Import/Export - allows users to link a google sheet for import as a new table, or export to another supported file format.

Of the above only 1) is semi-built, but we plan to crank out lots of 2, 3, and 4 in the near future.

## User Guide (TBD)

### Import/Export

Import can support a couple of different formats from Google Sheets. They are:

1) Independent - Import the given sheet as a new table with the defined columns as the table columns.
Data within the sheet is validated to be made uniform -- if there are exceptions they are either converted,
or deleted if unable to be converted.

Eg. Given a "Year" column, if the given value was "\"3\"", it would successfully convert and be stored in 
the database.

2) Match Intersection - Import the given sheet as compared to another existing table within the database. 
Only columns with names that form an exact match are imported into the existing table. Other un-matched columns are deleted.

3) Match Union - Import the given sheet as compared to another existing table within the database. The new
table will have both sets of columns.

4) Map - Import the given sheet as compared to another existing table within the database. The new table 
will have its data imported as defined by user mappings.

## Known Issues (TBD)