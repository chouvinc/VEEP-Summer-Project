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

### Visualization:
-User can Pan, Zoom, Save and Reset the graph by using the Bokeh Tools on the right of each plot.
-The four plots shown are:
1. Multiple Line: Annual VEEP Statistics from 2016 to 2019
2. Vertical Bar: VEEP StudentS Distribution by Year of Study in 2019
3. Pie/Wedge: VEEP Students Distribution by Disciplines in 2019
4. Horizontal Bar: VEEP Project Completion Rate in 2019

## Known Issues (TBD)

### Visualization:
-Cannot resolve the error by passion "from bokeh.palettes import all_palettes "
-Need to replace the testing data with actual imported data
