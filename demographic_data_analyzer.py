import pandas as pd
from collections import Counter

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv("adult.data.csv")

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = pd.Series(Counter(df["race"]))

    # What is the average age of men?
    average_age_men = round(df["age"][df["sex"] == "Male"].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    education = Counter(df["education"])
    percentage_bachelors = round((df["education"][df["education"] == "Bachelors"].count() / df["education"].count()) * 100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?
    # with and without `Bachelors`, `Masters`, or `Doctorate`
    df_high_ed = df[(df["education"] == "Bachelors") | (df["education"] == "Masters") | (df["education"] == "Doctorate")]
    df_lower_ed = df[(df["education"] != "Bachelors") & (df["education"] != "Masters") & (df["education"] != "Doctorate")]

    # percentage with salary >50K
    higher_education_rich = round((df_high_ed["salary"][df_high_ed["salary"] == ">50K"].count() / len(df_high_ed)) * 100, 1)
    lower_education_rich = round((df_lower_ed["salary"][df_lower_ed["salary"] == ">50K"].count() / len(df_lower_ed)) * 100, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df["hours-per-week"].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df["salary"][(df["hours-per-week"] == df["hours-per-week"].min())].count()
    rich_percentage = round((df["salary"][(df["hours-per-week"] == df["hours-per-week"].min()) & (df["salary"] == ">50K")].count() / num_min_workers) * 100, 1)

    # What country has the highest percentage of people that earn >50K?
    countries_by_rich = Counter(df["native-country"][df["salary"] == ">50K"])
    countries_by_pop = Counter(df["native-country"])

    def custom_map(dict_a, dict_b):
        dict_c = {}
        for key_a in dict_a.keys():
            for key_b in dict_b.keys():
                if key_a == key_b:
                    dict_c[key_a] = dict_b[key_b] / dict_a[key_a]
        return dict_c

    def dict_max(dict, opt="value"):
        max_key = ""
        max_value = 0
        for key, value in dict.items():
            if value > max_value:
                max_value = value
                max_key = key
        return max_key if opt == "key" else max_value

    countries_by_rich_pct = custom_map(countries_by_pop, countries_by_rich)
    highest_earning_country = dict_max(countries_by_rich_pct, "key")
    highest_earning_country_percentage = round(dict_max(countries_by_rich_pct) * 100, 1)
    
    # Identify the most popular occupation for those who earn >50K in India.
    indian_occupations = Counter(df["occupation"][(df["native-country"] == "India") & (df["salary"] == ">50K")])
    top_IN_occupation = dict_max(indian_occupations, "key")

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
