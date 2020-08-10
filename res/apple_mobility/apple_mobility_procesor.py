import pandas as pd

"""data = "GIT/group11/res/apple_mobility/processed/apple_mobility_trends.csv"

df = pd.read_csv(data)

countries_pd = df[df["geo_type"] == "country/region"]
del countries_pd["alternative_name"]
del countries_pd["sub-region"]
del countries_pd["country"]

del countries_pd["geo_type"]
countries_pd.to_csv("GIT/group11/res/apple_mobility/processed/global_apple_mobility_trends.csv", index = False)


processed_pd = pd.DataFrame(columns={"country","date","transportation_type", "value"})
country = 0
print(processed_pd)
for region in countries_pd["region"]:
    print(region)
    trp = countries_pd.at[country, "transportation_type"]
    print(trp)
    for date in countries_pd:
        if date != "region" and date != "transportation_type":
          
            value = countries_pd.at[country, date]
            row = {"country": region,"date": date, "transportation_type": trp,"value": value}
            processed_pd = processed_pd.append(row, ignore_index = True)
    country += 1"""
#processed_pd.to_csv("GIT/group11/res/apple_mobility/processed/countries_apple_mobility_trends.csv", index = False)
processed_pd = pd.read_csv("GIT/group11/res/apple_mobility/processed/countries_apple_mobility_trends.csv")
print(processed_pd)
for trp in ["walking", "driving", "transit"]:
    pd = processed_pd[processed_pd["transportation_type"] == trp].groupby("date").mean()
    pd.to_csv("GIT/group11/res/apple_mobility/processed/global_apple_mobility_trends_{}.csv".format(trp), index = True)



#How is the data preffered 104% or 4% change?
