from src.load_data import get_data

def get_highpaying_customers(filepath):
        data_historical_bookings=get_data(filepath)
        data_historical_bookings.to_csv("Data Ingestion/curated/historical_bookings.csv",index=False)
        print("Historical Bookings data dumped to curated")
        avg_price_history = data_historical_bookings['total_price'].mean()
        #Historical Segmentation
        high_paying_customers=data_historical_bookings[data_historical_bookings['total_price']>avg_price_history]
        print("High Valued Customers extracted")
        high_paying_customers.to_csv("Data Ingestion/curated/high_paying_customers.csv",index=False)
        print("High Paying customers Data Dumped in Curated")
        return high_paying_customers

high_paying_customers= get_highpaying_customers("Data Ingestion/Staging/historical_bookings.csv")
