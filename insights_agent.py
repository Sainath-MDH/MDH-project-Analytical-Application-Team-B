import json

def generate_insights():
    print("AI Insights Agent: Generating narrative summary...")
    with open('data/analytics_results.json', 'r') as f:
        data = json.load(f)
    
    total_incidents = data['total_incidents']
    top_district = data['top_hotspots'][0]['district']
    top_district_count = data['top_hotspots'][0]['count']
    avg_damage = data['avg_damage']
    most_common_bike = data['bike_breakdown'][0]['bike_type']
    
    # Simple logic to find busiest hour
    top_hour_data = sorted(data['hourly_distribution'], key=lambda x: x['count'], reverse=True)[0]
    top_hour = top_hour_data['hour']
    
    # Simple logic to find busiest day
    top_day_data = sorted(data['weekday_distribution'], key=lambda x: x['count'], reverse=True)[0]
    top_day = top_day_data['weekday']

    insights = [
        f"A total of {total_incidents:,} bike thefts were recorded in the dataset.",
        f"The most affected district is {top_district} with {top_district_count:,} reported incidents.",
        f"The average financial damage per theft is approximately €{avg_damage:.2f}.",
        f"The most frequently stolen bike type is the {most_common_bike}.",
        f"Thefts peak on {top_day}s, with the most common reporting time being around {top_hour}:00."
    ]
    
    with open('data/insights.json', 'w') as f:
        json.dump({"insights": insights}, f, indent=2)
        
    print("AI Insights Agent: Narrative summary saved to data/insights.json")
    return insights

if __name__ == "__main__":
    generate_insights()
