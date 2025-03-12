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
Simply fill in the JSON input form:
```json
{
    "geminiApiKey": "YOUR_GEMINI_API_KEY",
    "filter": "Location, dates, or keywords",
    "advancedFilter": "Price range, amenities, etc.",
    "bookingScrapingLimit": 40,
    "airbnbScrapingLimit": 40,
    "matchExactFilter": false
}
```

## What You Get
You'll receive a list of accommodation options with details like:
```json
[
    {
        "url": "https://www.example.com/hotel",
        "name": "Beachfront Apartment",
        "description": "A cozy 2-bedroom apartment with ocean views.",
        "location": "Barcelona, Spain",
        "rating": 4.8,
        "numberOfRatings": 120,
        "price": "$150 per night"
    }
]
```

## Pricing
💰 **Affordable & Transparent**  
- **Basic search** – $3.125 per 1,000 results.
- **Advanced filtering with AI** – Approx. 2000

## Get Started Now!
🚀 **Find the best accommodations today!** Simply enter your search criteria, and let this powerful tool do the work for you.

### Need Help?
📩 Reach out via [Discord](https://discordapp.com/users/.discouraged) or [e-mail](mailto:rizeadan99@gmail.com) for support. We're here to help!

---
**Developed by:** Dan Rizea

