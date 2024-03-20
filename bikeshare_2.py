import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

 # Predefined list of valid cities, months, and days
valid_cities = ['chicago', 'new york city', 'washington']
valid_months = ['all','january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
valid_days = ['all', 'monday', 'tuesday', 'wendesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). 
    # Keep asking for input until valid input is provided
    city = input("Please enter a city (chicago, new york city, washington): ").lower()

    while city not in valid_cities :
            print("Invalid input. Please enter a city from Chicago, New York City, and Washington.")
            city = input("Please enter a city (chicago, new york city, washington): ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Please enter a month (all, january, february, ... , june): ").lower()

    while month not in valid_months :
            print("Invalid input. Please enter a month (all, january, february, ... , june).")
            month = input("Please enter a month (all, january, february, ... , june): ").lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please enter a day of week (all, monday, tuesday, ... sunday): ").lower()

    while day not in valid_days :
            print("Invalid input. Please enter a day of week (all, monday, tuesday, ... sunday).")
            day = input("Please enter a day of week (all, monday, tuesday, ... sunday): ").lower()

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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    #df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = valid_months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        #df = df[df['day_of_week']== day.capitalize()]
        df = df[df['day_of_week']== day.title()]

    # ask if want to display header
    disp_head = input('Do you want to check the first 5 lines of the dataset?(Yes, No):').lower()
    num = 0
    while disp_head in ('yes', 'y') :
        num += 1
        if (num-1)*5  < df.shape[0] :
            print(df.drop(columns=['month', 'day_of_week']).iloc[(num-1)*5:num*5])
            disp_head = input('Do you want to check the next 5 lines of the dataset?(Yes, No):').lower()
        else:
             print('There is no more data to display.')

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract new columns hour
    df['hour'] = df['Start Time'].dt.hour
    # display the most common month
    popular_month = valid_months[df['month'].mode()[0]-1].title()
    print('Most common month:', popular_month)
    
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most common day of week:', popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most common start hour:', popular_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Most commonly used start station:', popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('Most commonly used end station:', popular_end)

    # display most frequent combination of start station and end station trip
    df['combine']=df['Start Station'] + 'To' + df['End Station']
    popular_comb = df['combine'].mode()[0]
    print('Most frequent combination of start station and end station trip:', popular_comb)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: ', df['Trip Duration'].sum())

    # display mean travel time
    print('Mean travel time: ', df['Trip Duration'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        print('\nCounts of user type:')
        for type, count in df['User Type'].value_counts().items():
            print('\nCount of {} is:'.format(type), str(count))

    # Display counts of gender if city is not washington
    if 'Gender' in df.columns:
        print('\nCounts of gender:')
        for gender, count in df['Gender'].value_counts().items():
            print('\nCount of {} is: '.format(gender), str(count))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest year of birth: ', int(df['Birth Year'].min()), '\n')
        print('Most recent year of birth: ', int(df['Birth Year'].max()), '\n')
        print('Most common year of birth: ', int(df['Birth Year'].mode().iloc[0]), '\n')

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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
