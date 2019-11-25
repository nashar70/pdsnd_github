import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():

 print('\nHello! Let\'s explore some US bikeshare data!')

 while True:
   city = input("\nWhich city do you want to view data for: Chicago, New York City or Washington?\n").lower()
   if city not in ('chicago', 'new york city', 'washington'):
     print("Invalid City, Choose - Chicago, New York City or Washington.")
     continue
   else:
     break

 while True:
   month = input("\nWhich month do you want to view data for: January, February, March, April, May, June or all?\n").lower()
   if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
     print("Invalid Month, Choose - January, February, March, April, May, June or all.")
     continue
   else:
     break

 while True:
   day = input("\nWhich day do you want to view data for: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all?\n").lower()
   if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
     print("Invalid Day, Choose Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all.")
     continue
   else:
     break

 print('-'*40)
 return city, month, day

def load_data(city, month, day):

 df = pd.read_csv(CITY_DATA[city])

 df['Start Time'] = pd.to_datetime(df['Start Time'])

 df['month'] = df['Start Time'].dt.month
 df['day_of_week'] = df['Start Time'].dt.weekday_name

 if month != 'all':
	 	# use the index of the months list to get the corresponding int
     months = ['january', 'february', 'march', 'april', 'may', 'june']
     month = months.index(month) + 1

     df = df[df['month'] == month]

 if day != 'all':
     df = df[df['day_of_week'] == day.title()]

 return df

def time_stats(df):

 print('\nCalculating The Most Popular Times of Travel...\n')
 start_time = time.time()

 popular_month = df['month'].mode()[0]
 print('Most Popular Month:', popular_month)

 popular_day = df['day_of_week'].mode()[0]
 print('Most Popular day:', popular_day)

 df['hour'] = df['Start Time'].dt.hour
 popular_hour = df['hour'].mode()[0]
 print('Most Popular Hour:', popular_hour)

 print("\nThis took %s seconds." % (time.time() - start_time))
 print('-'*40)

def station_stats(df):

 print('\nCalculating The Most Popular Stations and Trip...\n')
 start_time = time.time()

 Start_Station = df['Start Station'].value_counts().idxmax()
 print('Most Popular Start Station:', Start_Station)

 End_Station = df['End Station'].value_counts().idxmax()
 print('\nMost Popular End Station:', End_Station)

 Start_End_Stations = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
 print('\nMost popular Start to End Station Combination:')
 print(Start_End_Stations)

 
 print("\nThis took %s seconds." % (time.time() - start_time))
 print('-'*40)

def trip_duration_stats(df):

 print('\nCalculating The Total and Mean Travel Time...\n')
 start_time = time.time()
    
 total_time = df['Trip Duration'].sum()
 mins, sec = divmod(total_time, 60)
 hour, mins = divmod(mins, 60)
 print('Total travel time: {} hours {} minutes and {} seconds'.format(hour, mins, sec))
    
 mean_time = round(df['Trip Duration'].mean())
 mins, sec = divmod(mean_time, 60)
 hour, mins = divmod(mins, 60)
 print('Mean travel time: {} hours {} minutes and {} seconds'.format(hour, mins, sec))
    
 print("\nThis took %s seconds." % (time.time() - start_time))
 print('-'*40)

def user_stats(df):

 print('\nCalculating User Stats...\n')
 start_time = time.time()

 print()
 types_of_users = df.groupby('User Type',as_index=False).count()
 print('Count by User Type:')
 for i in range(len(types_of_users)):
     print('{}s - {}'.format(types_of_users['User Type'][i], types_of_users['Start Time'][i]))

 print()
 if 'Gender' not in df:
     print('Gender data is available for this location.')
 else:
     gender_of_users = df.groupby('Gender',as_index=False).count()
     print('Count by Gender:')
     for i in range(len(gender_of_users)):
         print('{}s - {}'.format(gender_of_users['Gender'][i], gender_of_users['Start Time'][i]))
      
 print()
 if 'Birth Year' not in df:
     print('Year of Birth data is available for this location.')
 else:
     birth = df.groupby('Birth Year', as_index=False).count()
     print('Earliest Year of Birth: {}.'.format(int(birth['Birth Year'].min())))
     print('Most recent Year of Birth: {}.'.format(int(birth['Birth Year'].max())))
     print('Most common Year of Birth: {}.'.format(int(birth.iloc[birth['Start Time'].idxmax()]['Birth Year'])))

 print("\nThis took %s seconds." % (time.time() - start_time))
 print('-'*40)
 
def raw_data(df):
    start_loc = 0
    end_loc = 5

    display_data = input("Do you want to view a sampe of the data? Yes or No.\n").lower()
    if display_data == 'yes':
        while end_loc <= df.shape[0] - 1:

            print(df.iloc[start_loc:end_loc,:])
            start_loc += 5
            end_loc += 5

            end_display = input("Do want to view additional data? Yes or No\n").lower()
            if end_display == 'no':
                break
 
def main():
 while True:
     city, month, day = get_filters()
     df = load_data(city, month, day)

     time_stats(df)
     station_stats(df)
     trip_duration_stats(df)
     user_stats(df)
     raw_data(df)

     restart = input('\nWould you like to restart? Enter Yes or No.\n').lower()
     if restart.lower() != 'yes':
         break

if __name__ == "__main__":
	main()

    
    