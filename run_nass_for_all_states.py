import subprocess


states = ["AL", "AK", "AZ",	"AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA",	"HI", "ID",
          "IL",	"IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO",
          "MT", "NE", "NV", "NH", "NJ", "NM", "NY",	"NC", "ND",	"OH", "OK", "OR", "PA",
          "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI",	"WY"]

crops = ["CORN", "BARLEY", "SOYBEANS", "OATS"]


for state in states:
    print(state)
    for crop in crops:
        print(crop)
        subprocess.run(["python", "nass_quick_stat.py", "-so", "SURVEY","-st", f"{state}",
                         "-yr", "1997", "-cr", f"{crop}", "-stc", "YIELD", "-u", "COUNTY"])

