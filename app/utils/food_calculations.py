"""
Utility functions for food waste calculations and analytics.
Provides business logic for waste tracking and environmental impact.
"""

from datetime import datetime, timedelta
from app.models import FoodItem

class FoodWasteCalculator:
    """
    Static class containing methods for food waste calculations.
    No instance needed - all methods are class methods.
    """
    
    @staticmethod
    def calculate_waste_stats(user_id):
        """
        Calculate comprehensive waste statistics for a specific user.
        
        Args:
            user_id (int): ID of the user to calculate stats for
            
        Returns:
            dict: Dictionary containing waste statistics
        """
        # Get all food items belonging to the user
        food_items = FoodItem.query.filter_by(user_id=user_id).all()
        
        # Count items by status
        total_items = len(food_items)
        consumed = len([f for f in food_items if f.current_status == 'consumed'])
        wasted = len([f for f in food_items if f.current_status == 'wasted'])
        expired = len([f for f in food_items if f.current_status == 'expired'])
        donated = len([f for f in food_items if f.current_status == 'donated'])
        
        # Calculate waste percentage (avoid division by zero)
        if total_items > 0:
            waste_percentage = (wasted / total_items) * 100
            consumption_percentage = (consumed / total_items) * 100
        else:
            waste_percentage = 0
            consumption_percentage = 0
        
        # Calculate average days until consumption (for consumed items)
        consumed_items = [f for f in food_items if f.current_status == 'consumed']
        if consumed_items:
            total_consumption_days = sum([(f.purchase_date - f.created_at).days for f in consumed_items])
            avg_consumption_days = total_consumption_days / len(consumed_items)
        else:
            avg_consumption_days = 0
            
        return {
            'total_items': total_items,
            'consumed': consumed,
            'wasted': wasted,
            'expired': expired,
            'donated': donated,
            'waste_percentage': round(waste_percentage, 2),
            'consumption_percentage': round(consumption_percentage, 2),
            'avg_consumption_days': round(avg_consumption_days, 1),
            'saved_items': consumed + donated  # Items that weren't wasted
        }
    
    @staticmethod
    def get_expiring_soon_items(user_id, days_threshold=3):
        """
        Get food items that are expiring within the specified days.
        Used for generating alerts and reminders.
        
        Args:
            user_id (int): ID of the user
            days_threshold (int): Number of days to consider as "soon"
            
        Returns:
            list: List of FoodItem objects expiring soon
        """
        # Calculate threshold date
        threshold = datetime.utcnow() + timedelta(days=days_threshold)
        
        # Query for items expiring soon but not yet expired/consumed/wasted
        return FoodItem.query.filter(
            FoodItem.user_id == user_id,
            FoodItem.expiry_date <= threshold,
            FoodItem.current_status.in_(['fresh', 'expiring_soon'])
        ).order_by(FoodItem.expiry_date.asc()).all()
    
    @staticmethod
    def get_recently_added_items(user_id, days=7):
        """
        Get food items added in the last specified days.
        
        Args:
            user_id (int): ID of the user
            days (int): Number of days to look back
            
        Returns:
            list: List of recently added FoodItem objects
        """
        threshold = datetime.utcnow() - timedelta(days=days)
        
        return FoodItem.query.filter(
            FoodItem.user_id == user_id,
            FoodItem.created_at >= threshold
        ).order_by(FoodItem.created_at.desc()).all()
    
    @staticmethod
    def estimate_environmental_impact(wasted_items):
        """
        Estimate environmental impact based on number of wasted food items.
        Uses rough estimates that can be refined with more precise data.
        
        Args:
            wasted_items (int): Number of food items wasted
            
        Returns:
            dict: Environmental impact metrics
        """
        # Environmental estimates (can be calibrated with real data)
        CO2_PER_KG = 2.5      # kg CO2 emissions per kg of food waste
        WATER_PER_KG = 1000   # liters of water per kg of food production
        MEALS_PER_KG = 3      # Rough estimate: 3 meals per kg of food
        LANDFILL_PER_KG = 1.2 # kg of landfill waste per kg of food
        
        # Convert item count to weight (assuming average 0.5kg per item)
        total_kg = wasted_items * 0.5
        
        return {
            'co2_saved_kg': round(total_kg * CO2_PER_KG, 2),
            'water_saved_liters': round(total_kg * WATER_PER_KG, 2),
            'meals_saved': int(total_kg * MEALS_PER_KG),
            'landfill_saved_kg': round(total_kg * LANDFILL_PER_KG, 2),
            'food_saved_kg': round(total_kg, 2)
        }
    
    @staticmethod
    def calculate_money_saved(wasted_items, cost_per_kg=5.0):
        """
        Estimate money saved by reducing food waste.
        
        Args:
            wasted_items (int): Number of food items wasted
            cost_per_kg (float): Average cost per kg of food
            
        Returns:
            float: Estimated money saved in currency units
        """
        total_kg = wasted_items * 0.5
        return round(total_kg * cost_per_kg, 2)
    
    @staticmethod
    def get_category_insights(user_id):
        """
        Get insights about food consumption and waste by category.
        
        Args:
            user_id (int): ID of the user
            
        Returns:
            dict: Category-wise insights
        """
        food_items = FoodItem.query.filter_by(user_id=user_id).all()
        
        category_data = {}
        
        for item in food_items:
            category = item.category.value
            
            if category not in category_data:
                category_data[category] = {
                    'total': 0,
                    'consumed': 0,
                    'wasted': 0,
                    'expired': 0,
                    'donated': 0
                }
            
            category_data[category]['total'] += 1
            
            if item.current_status == 'consumed':
                category_data[category]['consumed'] += 1
            elif item.current_status == 'wasted':
                category_data[category]['wasted'] += 1
            elif item.current_status == 'expired':
                category_data[category]['expired'] += 1
            elif item.current_status == 'donated':
                category_data[category]['donated'] += 1
        
        # Calculate percentages and insights
        insights = {}
        for category, data in category_data.items():
            if data['total'] > 0:
                waste_rate = (data['wasted'] / data['total']) * 100
                consumption_rate = (data['consumed'] / data['total']) * 100
                
                insights[category] = {
                    **data,
                    'waste_rate': round(waste_rate, 2),
                    'consumption_rate': round(consumption_rate, 2),
                    'efficiency_score': round(consumption_rate - waste_rate, 2)
                }
        
        return insights
    
    @staticmethod
    def get_weekly_trend(user_id, weeks=8):
        """
        Get weekly waste and consumption trends.
        
        Args:
            user_id (int): ID of the user
            weeks (int): Number of weeks to include
            
        Returns:
            dict: Weekly trend data
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(weeks=weeks)
        
        food_items = FoodItem.query.filter(
            FoodItem.user_id == user_id,
            FoodItem.created_at >= start_date
        ).all()
        
        weekly_data = {}
        
        for item in food_items:
            # Get week number (ISO week)
            year, week, _ = item.created_at.isocalendar()
            week_key = f"{year}-W{week:02d}"
            
            if week_key not in weekly_data:
                weekly_data[week_key] = {
                    'consumed': 0,
                    'wasted': 0,
                    'added': 0
                }
            
            weekly_data[week_key]['added'] += 1
            
            if item.current_status == 'consumed':
                weekly_data[week_key]['consumed'] += 1
            elif item.current_status == 'wasted':
                weekly_data[week_key]['wasted'] += 1
        
        # Convert to sorted list
        sorted_weeks = sorted(weekly_data.keys())
        
        return {
            'weeks': sorted_weeks,
            'added': [weekly_data[week]['added'] for week in sorted_weeks],
            'consumed': [weekly_data[week]['consumed'] for week in sorted_weeks],
            'wasted': [weekly_data[week]['wasted'] for week in sorted_weeks]
        }
    
    @staticmethod
    def calculate_savings_goals(user_id, target_waste_reduction=0.2):
        """
        Calculate savings goals and progress.
        
        Args:
            user_id (int): ID of the user
            target_waste_reduction (float): Target waste reduction (e.g., 0.2 for 20%)
            
        Returns:
            dict: Savings goals and progress
        """
        stats = FoodWasteCalculator.calculate_waste_stats(user_id)
        environmental_impact = FoodWasteCalculator.estimate_environmental_impact(stats['wasted'])
        money_saved = FoodWasteCalculator.calculate_money_saved(stats['wasted'])
        
        target_waste = stats['wasted'] * (1 - target_waste_reduction)
        potential_savings = {
            'co2_kg': environmental_impact['co2_saved_kg'] * target_waste_reduction,
            'water_liters': environmental_impact['water_saved_liters'] * target_waste_reduction,
            'meals': int(environmental_impact['meals_saved'] * target_waste_reduction),
            'money': money_saved * target_waste_reduction
        }
        
        return {
            'current_waste': stats['wasted'],
            'target_waste': round(target_waste, 1),
            'reduction_target': target_waste_reduction * 100,
            'progress_percentage': min(100, (stats['wasted'] - target_waste) / stats['wasted'] * 100) if stats['wasted'] > 0 else 0,
            'potential_savings': potential_savings
        }
    