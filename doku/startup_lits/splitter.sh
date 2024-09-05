#!/bin/bash

# Check if a filename was provided as an argument
if [ "$#" -ne 1 ]; then
	echo "Usage: $0 <csv_filename>"
	exit 1
fi

# Assign the first argument to a variable
csv_file="$1"

# Define output filenames
company_file="company_links.csv"
person_file="person_links.csv"

# Use awk to process the CSV file
awk -F';' '
BEGIN {
    # Print the header to both output files
    print "Company;Gründer;Type;Year;Link" > "'"$company_file"'"
    print "Company;Gründer;Type;Year;Link" > "'"$person_file"'"
}
NR > 1 {
    # Check if the link contains "company" and write to company_file
    if ($5 ~ /company/) {
        print $0 > "'"$company_file"'"
    }
    # Check if the link contains "in" and write to person_file
    else if ($5 ~ /in/) {
        print $0 > "'"$person_file"'"
    }
}' "$csv_file"

# Inform the user that the files have been created
echo "Filtered data has been written to $company_file and $person_file"
