import time
import pandas as pd
import numpy as np
import sys

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Month data only goes up to June.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some U.S. bikeshare data!')
    # Get user input for city (chicago, new york city, washington) and deal with invalid inputs
    while True:
        city = input("What city's data would you like to explore? (Chicago, New York City, or Washington): ").lower()
        if city.lower() in ('chicago', 'new york city', 'washington'):
            break
        else:
            print("Invalid city. Please try again.")
    # Get user input for jan to june, or all
    while True:
        month = input("For what month? Choose from January to June numerically (1 = January) For all months, type 'all': ")
        month = str(month)
        #check if month is valid:
        valid_months = ['1','2', '3', '4', '5', '6', 'all']
        if month in valid_months:
            break
        else:
            print("Invalid month. Please try again.")
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("For what day of the week? (0 = Monday, 6 = Sunday). For all days of the week, type 'all': ")
        day = str(day)
        #check if day is valid:
        valid_days = ['0','1','2','3','4','5','6','all']
        if day in valid_days:
            break
        else:
            print("Invalid day of the week. Please try again.")
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new column and convert into string type to match input
    df['month'] = df['Start Time'].dt.month
    df['month'] = df['month'].astype(str)
    df['day'] = df['Start Time'].dt.weekday
    df['day'] = df['day'].astype(str)

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    print('(1 = January;')
    print('0 = Monday, 1 = Tuesday, 2 = Wednesday, 3 = Thursday, 4 = Friday, 5 = Saturday, 6 = Sunday)\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['month'].mode()[0]
    print('Most common/chosen month: {}',.format(common_month))

    # Display the most common day of week
    common_day = df['day'].mode()[0]
    print('Most common/chosen day of week: {}',.format(common_day))

    # Convert to datetime and display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common start hour: {}',.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_stn = df['Start Station'].value_counts().idxmax()
    print('Most common Start Station: ', common_start_stn)

    # Display most commonly used end station
    common_end_stn = df['End Station'].value_counts().idxmax()
    print('Most common End Station: ', common_end_stn)

    # Display most frequent combination of start station and end station trip
    df['start_end'] = df['Start Station'] + ' to ' + df['End Station']
    common_start_end = df['start_end'].value_counts().idxmax()
    print('Most frequent combination of Start and End Stations: ', common_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time in seconds is: ', total_travel_time,)

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average travel time in seconds is: ', round(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats: Subscriber Type, Gender, and Birth Year...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender, excluding Washington
    try:
        column_data = df['Gender']
        gender = df['Gender'].value_counts()
        print(gender)
    except KeyError:
        print('\nWashington bikeshare program does not collect Gender data from its users.')

    # Display earliest, most recent, and most common year of birth, excluding Washington
    try:
        column_data = df['Birth Year']
        earliest_birth_year = df['Birth Year'].min()
        print('The earliest birth year is ', int(earliest_birth_year))
        
        last_birth_year = df['Birth Year'].max()
        print('The most recent birth year is ', int(last_birth_year))

        most_common_birth_year = df['Birth Year'].mode()
        print('The most common birth year is ', int(most_common_birth_year))

    except KeyError:
        print('\nWashington bikeshare program does not collect Birth Year data from its users.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        # ask user if they want to see raw data and if they want to restart or end program
        # define a start index that keeps adding 5 when user says yes to seeing more data
        start = 0
        end = 5 
        raw_data = input('\nWould you like to see five rows of raw data? Enter yes or no: \n').lower()
        # keep checking if there is more data to show
        while end < len(df):
            if raw_data.lower() == 'no':
                break
            elif raw_data.lower() == 'yes':
                print(df.iloc[start:end].to_string())
                #if there is more data, ask if user wants to see it
                more_data = input('\nWould you like to see the next five rows? Enter yes or no: \n').lower()
                #account for typos
                while more_data not in ('yes','no'):
                    print('Invalid input. Please try again.')
                    more_data = input('\nWould you like to see the next five rows? Enter yes or no: \n').lower()
                if more_data == 'no':
                    break
                elif more_data == 'yes': 
                    #increment start and end positions to keep showing the next 5
                    start += 5
                    end += 5
            else:
                print('Invalid input. Please try again')
                raw_data = input('\nWould you like to see five rows of raw data? Enter yes or no: \n').lower()
        #display this once while end < len(df) loop is no longer true
        print('No more data to display!')
            
            
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
            if restart.lower() == 'yes':
                break
            elif restart not in ('yes', 'no'):
                print('Invalid input. Please try again')
            elif restart.lower() == 'no':
                print('The program will now exit. Thanks for exploring U.S. bikeshare data!')
                sys.exit()

if __name__ == "__main__":
    main()
