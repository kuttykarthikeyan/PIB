from tqdm import tqdm



def time_age_function(publist_date):
    from datetime import datetime

    # Define the target datetime
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # target_datetime = datetime.strptime(publist_date, date_format)
    target_datetime = publist_date

    # Get the current datetime
    current_datetime = datetime.now()

    # Calculate the time difference
    time_difference = current_datetime - target_datetime

    # Extract the time difference components (days, seconds, etc.)
    days = time_difference.days
    seconds = time_difference.seconds

    # Calculate hours, minutes, and remaining seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Print the time difference
    return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds ago"
    
    
def state_wise_news_for_each_department(state,department,language,max_results,past_no_of_hours):
    
    from gnews import GNews
    import pandas as pd
    from datetime import datetime  
    
    date_format = "%a, %d %b %Y %H:%M:%S GMT"

    google_news = GNews()
    google_news.period =  str(past_no_of_hours)+ 'h'  # News from last 7 days
    google_news.max_results = max_results  # number of responses across a keyword
    google_news.country = 'India'  # News from a specific country 
    google_news.language = language  # News in a specific language
    google_news.exclude_websites = ['yahoo.com', 'cnn.com']
    json_resp = google_news.get_news( department + " for Government of " + state + " when:"+str(past_no_of_hours)+"h")
    if len(json_resp) != 0:
        d = [ pd.DataFrame([i]) for i in json_resp]
        df = pd.concat(d)
        df['publisher'] = [ i['title']  for i in df['publisher']]
        df['published date']  = [ datetime.strptime(i, date_format) for i in df['published date']]
        df["published time ago"] = [ time_age_function(i)  for i in df['published date']]
        df['published date'] = pd.to_datetime(df['published date'])
        df.sort_values('published date',ascending=False)

        # description_list = []
        # for i in range(len(json_resp)):
        #     try:
        #         article = google_news.get_full_article(json_resp[i]['url'])
        #         description_list.append(article.text)
        #     except:
        #         article = "None"
        #         description_list.append(article)
            
            
        # df['description'] = description_list
        
        df['State'] = [ state for i in range(len(df))]
        df['Department'] = [ department for i in range(len(df))]
        
        
        return df
    else:
        return []
 




states_list = ['Delhi', 'Mumbai', 'Hyderabad', 'Chennai', 'Chandigarh', 'Kolkata', 'Bengaluru', 'Bhubaneswar', 'Ahmedabad', 'Guwahati', 'Thiruvananthpuram', 'Imphal', 'Aizawl', 'Agartala', 'Gangtok', 'Kohima', 'Shillong', 'Itanagar', 'Lucknow', 'Bhopal', 'Jaipur', 'Patna', 'Ranchi', 'Shimla', 'Raipur']
text_content = ["President's Secretariat", "Vice President's Secretariat", "Prime Minister's Office", "Cabinet", "Cabinet Committee Decisions", "Cabinet Committee on Economic Affairs (CCEA)", "Cabinet Secretariat", "Cabinet Committee on Infrastructure", "Cabinet Committee on Price", "Cabinet Committee on Investment", "AYUSH", "Other Cabinet Committees", "Department of Space", "Department of Ocean Development", "Department of Atomic Energy", "Election Commission", "Finance Commission", "Ministry of Agriculture & Farmers Welfare", "Ministry of Agro & Rural Industries", "Ministry of Chemicals and Fertilizers", "Ministry of Civil Aviation", "Ministry of Coal", "Ministry of Commerce & Industry", "Ministry of Communications", "Ministry of Company Affairs", "Ministry of Consumer Affairs, Food & Public Distribution", "Ministry of Cooperation", "Ministry of Corporate Affairs", "Ministry of Culture", "Ministry of Defence", "Ministry of Development of North-East Region", "Ministry of Disinvestment", "Ministry of Drinking Water & Sanitation", "Ministry of Earth Sciences", "Ministry of Education", "Ministry of Electronics & IT", "Ministry of Environment, Forest and Climate Change", "Ministry of External Affairs", "Ministry of Finance", "Ministry of Fisheries, Animal Husbandry & Dairying", "Ministry of Food Processing Industries", "Ministry of Health and Family Welfare", "Ministry of Heavy Industries", "Ministry of Home Affairs", "Ministry of Housing & Urban Affairs", "Ministry of Information & Broadcasting", "Ministry of Jal Shakti", "Ministry of Labour & Employment", "Ministry of Law and Justice", "Ministry of Micro, Small & Medium Enterprises", "Ministry of Mines", "Ministry of Minority Affairs", "Ministry of New and Renewable Energy", "Ministry of Overseas Indian Affairs", "Ministry of Panchayati Raj", "Ministry of Parliamentary Affairs", "Ministry of Personnel, Public Grievances & Pensions", "Ministry of Petroleum & Natural Gas", "Ministry of Planning", "Ministry of Power", "Ministry of Railways", "Ministry of Road Transport & Highways", "Ministry of Rural Development", "Ministry of Science & Technology", "Ministry of Ports, Shipping and Waterways", "Ministry of Skill Development and Entrepreneurship", "Ministry of Social Justice & Empowerment", "Ministry of Statistics & Programme Implementation", "Ministry of Steel", "Ministry of Surface Transport", "Ministry of Textiles", "Ministry of Tourism", "Ministry of Tribal Affairs", "Ministry of Urban Development", "Ministry of Water Resources, River Development and Ganga Rejuvenation", "Ministry of Women and Child Development", "Ministry of Youth Affairs and Sports", "NITI Aayog", "PM Speech", "EAC-PM", "UPSC", "Special Service and Features", "PIB Headquarters", "Office of Principal Scientific Advisor to GoI", "National Financial Reporting Authority", "Competition Commission of India", "IFSC Authority", "National Security Council Secretariat"]

final_dataframe_list = []
import pandas as pd

for i in tqdm(states_list[0:1]):
    print("Collecting news from " + i + " state")
    for j in tqdm(text_content):
        
        result = state_wise_news_for_each_department(state=i,department=j,language="english",max_results=5,past_no_of_hours=2)
        
        if len(result) != 0:
            final_dataframe_list.append(result)
        else:
            pass

        print(i,"==> ",j ,"length => ",len(result))
        
        


final_data = pd.concat([ i for i in final_dataframe_list if len(i) != []], ignore_index=True)

final_data.to_csv("final_data.csv")
        
        
        


    