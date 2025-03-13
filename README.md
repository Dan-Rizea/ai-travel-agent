# Find the Best Travel Deals – Fast & Easy!

## What is this tool?
This Apify actor helps you quickly find accommodation listings from top travel websites like **Booking.com** and **Airbnb**. Get the best options that match your preferences—without the hassle of manually searching multiple sites.

## Why use it?
✅ **Search multiple platforms at once** – No need to check different sites separately.  
✅ **Smart filtering** – Use simple or advanced filters to find exactly what you need.  
✅ **AI-powered search** – Uses Google's Gemini AI model to refine your results.  
✅ **Fast & efficient** – Get the best deals in just a few clicks.  
✅ **Easy data access** – Download results in structured formats like JSON for easy use.

## How to Use
1. **Enter your search criteria** – Choose your location, dates, and preferences.
2. **Customize your filters** – Set price range, amenities, and more.
3. **Start the search** – The actor scans Booking.com and Airbnb for the best matches.
4. **Get your results** – See a list of top accommodations tailored to your needs.
5. **Download & use the data** – Export results for reports, planning, or further analysis.

## Input Settings
Simply fill in the Input form:
```json
{
    "geminiApiKey": "YOUR_GEMINI_API_KEY",
    "filter": "Looking for a 2-bedroom accommodation in Barcelona with ratings above 4.0 and a price between $100 and $300 per night",
    "advancedFilter": "I want the property to have a beautiful sea-side view. I also want to only see discounted properties with air conditioning and a private kitchen.",
    "bookingScrapingLimit": 40,
    "airbnbScrapingLimit": 40,
    "matchExactFilter": false
}
```

- **geminiApiKey*** - You can get this parameter from here: [API Key Link](https://aistudio.google.com/u/1/apikey). The free tier Gemini tier can work well for 50 total scraping requests, but will fail if more are used. To prevent that, please use the **Tier 1** pricing model. You can find more information on pricing [here](https://ai.google.dev/gemini-api/docs/pricing#gemini-2.0-flash-lite) and on rate limits [here](https://ai.google.dev/gemini-api/docs/rate-limits?hl=en#current-rate-limits).  
- **filter*** - You can use this to specify parameters used within the used Airbnb and Booking scrapers. 
- **advancedFilter** - You can use this to filter the results received from Airbnb and Booking.
- **bookingScrapingLimit*** - Specifies how many results the Booking scraper should retrieve 
- **airbnbScrapingLimit*** - Specifies how many results the Airbnb scraper should retrieve
- **matchExactFilter** - If enabled, you can use this parameter to make Gemini give you more accurate/specific outputs, ignoring results that do not exactly match your requests 

## What You Get
You'll receive a list of accommodation options with details like:
```json
[
    {
      "url": "https://www.airbnb.com/rooms/42151836?locale=en-US&currency=USD&adults=1&children=0&infants=0&pets=0&check_in=2024-01-01&check_out=2024-01-08",
      "name": "Chic Penthouse in the center with private terrace",
      "description": "HUTB-005661-39Situated in the coolest neighborhood in the world (TIME OUT ranking 2020), this fantastic penthouse has one cosy terrace with direct access from the flat and one private rooftop terrace. It has a comfy table and chairs to work with your computer and super fast reliable internet connection. It is also well located to go sightseeing (15min walk - 2 metro stops from  Placara Catalunya). The apartment was renovated in February 2020 and fully equipped for your maximum comfort.The spaceThe apartment is very bright, it is tastefully decorated and has been prepared for your maximum comfort. Both terraces are super pleasant and have views of different highlights of the city, like Tibidabo, Sangrada Familia or Montjuic.The same level terrace has sofas, umbrella and table to relax. The rooftop terrace has a shower, chill out and sun loungers. In addition, it has a table and umbrella so you can organize your breakfast, lunch or dinner there.Within the apartment you will find:- one bedroom with a double bed and direct exit to the same level terrace- one bedroom with twin separated beds- living room with sofa (where 1 person can sleep), fully equipped kitchen and dinning area- full bathroom with rain showerThe apartment is fully equipped with good quality towels, linens and kitchenware. It has air conditioning for summer and heating system to stay comfortable in winter.Other things to noteIn order to ensure the well-being of other guests and neighbors, we have installed decibel meters in the common areas of the apartment. If the maximum established by law is exceeded, an agent will contact you to ask you to lower the noise level.Please notice that the sofa in the living room is a standard sofa (not a sofa bed) but one person can sleep there as it is super comfortable and spacious (280cm long, 90 cm guide). Bedsheets and towels for that person are under the chaise longue.Registration numberHUTB-005661",
      "location": "Barcelona",
      "rating": 4.852857142857142,
      "numberOfRatings": 284,
      "price": "$214"
    }
]
```

## Pricing
💰 **Affordable & Transparent**  
- **AI Travel Agent** – $3.125 per 1,000 results scraped from either **Booking** or **Airbnb**.
- **Bookings** – $5.000 per 1,000 results scraped from **Booking**
- **Airbnb** – $1.250 per 1,000 results scraped from **Airbnb**.
- **Gemini** – All Gemini token costs will be charged through the provided API Key. This scraper uses Gemini's 2.0-flash-lite model which has a cost of 0.075$ per 1 million tokens. This approximates to 0.15\$ per 1000 scraped results.
- **Overview** - The total cost for 1000 analyzed accommodations (500 from Booking and 500 from Airbnb) would amount to 6.400$ 
## Get Started Now!
🚀 **Find the best accommodations today!** Simply enter your search criteria, and let this powerful tool do the work for you.

### Need Help?
📩 Reach out via [Discord](https://discordapp.com/users/.discouraged) or [e-mail](mailto:rizeadan99@gmail.com) for support. I'm here to help!

---
**Developed by:** Dan Rizea

