import json
import os
from typing import Any
from collections import Counter, defaultdict
from datetime import datetime

def run_analytics():
    print("Analytics Agent: Starting analysis...")
    # Load cleaned data
    if not os.path.exists('data/thefts_clean.json'):
        print("Error: data/thefts_clean.json not found. Please run data_agent.py first.")
        return None
        
    with open('data/thefts_clean.json', 'r') as f:
        data = json.load(f)
    
    if not data:
        print("Analytics Agent: No data to analyze.")
        return None

    results: dict[str, Any] = {}
    
    # 1. Total KPIs
    total_incidents = len(data)
    total_damage = sum(item['damage'] for item in data if item['damage'] is not None)
    avg_damage = total_damage / total_incidents if total_incidents > 0 else 0
    
    results['total_incidents'] = total_incidents
    results['total_damage'] = float(total_damage)
    results['avg_damage'] = float(avg_damage)
    
    # 2. Monthly Trend
    # Format: YYYY-MM
    monthly_stats = defaultdict(lambda: {'damage': 0, 'count': 0})
    for item in data:
        month_key = item['start_date'][:7] # YYYY-MM
        monthly_stats[month_key]['damage'] += item['damage'] if item['damage'] is not None else 0
        monthly_stats[month_key]['count'] += 1
        
    monthly_trend = []
    for month in sorted(monthly_stats.keys()):
        monthly_trend.append({
            'start_date': month,
            'damage': monthly_stats[month]['damage'],
            'district': monthly_stats[month]['count'] # Keeping 'district' key for compatibility with existing UI
        })
    results['monthly_trend'] = monthly_trend
    
    # 3. Top 10 Hotspots (District)
    district_counts = Counter(item['district'] for item in data)
    hotspots = []
    for district, count in district_counts.most_common(10):
        hotspots.append({'district': district, 'count': count})
    results['top_hotspots'] = hotspots
    
    # 4. Weekday Distribution
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_counts = Counter(item['weekday'] for item in data)
    weekday_dist = []
    for day in days:
        weekday_dist.append({'weekday': day, 'count': weekday_counts[day]})
    results['weekday_distribution'] = weekday_dist
    
    # 5. Hourly Distribution
    hour_counts = Counter(item['start_hour'] for item in data)
    hourly_dist = []
    for hour in range(24):
        hourly_dist.append({'hour': hour, 'count': hour_counts[str(hour)]})
    results['hourly_distribution'] = hourly_dist
    
    # 6. Bike Type Breakdown
    bike_counts = Counter(item['bike_type'] for item in data)
    bike_breakdown = []
    for bike, count in bike_counts.most_common():
        bike_breakdown.append({'bike_type': bike, 'count': count})
    results['bike_breakdown'] = bike_breakdown
    
    # 7. Damage by District
    district_damage = defaultdict(list)
    for item in data:
        if item['damage'] is not None:
            district_damage[item['district']].append(item['damage'])
            
    avg_damage_by_district = []
    for district, damages in district_damage.items():
        avg_damage_by_district.append({
            'district': district,
            'damage': sum(damages) / len(damages)
        })
    # Sort by damage descending
    avg_damage_by_district.sort(key=lambda x: x['damage'], reverse=True)
    results['avg_damage_by_district'] = avg_damage_by_district
    
    # Save results
    os.makedirs('data', exist_ok=True)
    with open('data/analytics_results.json', 'w') as f:
        json.dump(results, f, indent=2)
        
    print("Analytics Agent: Analysis complete results saved to data/analytics_results.json")
    return results

if __name__ == "__main__":
    run_analytics()
