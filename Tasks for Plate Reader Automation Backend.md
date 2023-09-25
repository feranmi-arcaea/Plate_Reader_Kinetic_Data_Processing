Tasks for Plate Reader Automation Backend

- Import exported plate reader results
- Import Plate map annotation
- Extract OD590 and OD700 for wells from imported results
- Subtract OD590-OD700 for each well
- Annotate well based on "Well, Condition and Microbe" columns in plate map annotation file
- Average triplicates (ideal would be to dynamically identify replicate wells and average them)
- Subtract blanks from actual values for each condition
- Calculate AUC for each Condition-microbe combination
- Graph growth curve for each microbe under the different conditions