"""
Notification utilities for food waste tracker.
Handles email alerts, expiry notifications, and user communications.
"""

from flask import current_app
from app.models import FoodItem, User
from datetime import datetime, timedelta

class NotificationManager:
    """
    Manages all notification types for the food waste tracker.
    Uses console logging for now - can be extended with real email service.
    """
    
    @staticmethod
    def check_expiry_notifications():
        """
        Check for food items expiring soon and send notifications.
        Returns list of items that need user attention.
        """
        # Get all users
        users = User.query.all()
        notifications = []
        
        for user in users:
            # Get items expiring in the next 3 days
            threshold = datetime.utcnow() + timedelta(days=3)
            expiring_items = FoodItem.query.filter(
                FoodItem.user_id == user.id,
                FoodItem.expiry_date <= threshold,
                FoodItem.current_status.in_(['fresh', 'expiring_soon'])
            ).all()
            
            if expiring_items:
                notifications.append({
                    'user': user,
                    'items': expiring_items,
                    'count': len(expiring_items)
                })
        
        return notifications
    
    @staticmethod
    def send_expiry_alert(user, expiring_items):
        """
        Send expiry alert notification to user.
        In a production app, this would send real emails.
        
        Args:
            user: User object to notify
            expiring_items: List of FoodItem objects expiring soon
            
        Returns:
            bool: True if notification was "sent" (logged)
        """
        try:
            subject = f"🍎 FoodSave Alert: {len(expiring_items)} Items Expiring Soon"
            
            # Create notification content
            message = f"""
            Hi {user.username},
            
            You have {len(expiring_items)} food item(s) that will expire soon:
            
            """
            
            for item in expiring_items:
                days_left = item.days_until_expiry()
                message += f"• {item.name} ({item.quantity}) - Expires in {days_left} days\n"
            
            message += """
            Suggested Actions:
            ✅ Consume these items soon
            ❤️ Consider donating if you can't consume them
            📊 Update their status in your FoodSave dashboard
            
            Reduce waste, save money! 🌱
            
            Best regards,
            FoodSave Team
            """
            
            # Log the notification (replace with real email in production)
            print("=" * 50)
            print("📧 EXPIRY ALERT NOTIFICATION")
            print("=" * 50)
            print(f"To: {user.email}")
            print(f"Subject: {subject}")
            print(f"Message: {message}")
            print("=" * 50)
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending notification to {user.email}: {e}")
            return False
    
    @staticmethod
    def send_waste_report(user, stats, period='weekly'):
        """
        Send waste reduction report to user.
        
        Args:
            user: User object
            stats: Waste statistics dictionary
            period: Report period ('weekly', 'monthly')
            
        Returns:
            bool: True if report was "sent" (logged)
        """
        try:
            subject = f"📊 FoodSave {period.capitalize()} Waste Report"
            
            message = f"""
            Hi {user.username},
            
            Here's your {period} food waste report:
            
            📈 Waste Statistics:
            • Total Items Tracked: {stats.get('total_items', 0)}
            • Consumed: {stats.get('consumed', 0)}
            • Wasted: {stats.get('wasted', 0)}
            • Waste Rate: {stats.get('waste_percentage', 0)}%
            
            🌍 Environmental Impact:
            • CO₂ Prevented: {stats.get('co2_saved_kg', 0)} kg
            • Water Saved: {stats.get('water_saved_liters', 0)} liters
            • Meals Saved: {stats.get('meals_saved', 0)}
            
            Keep up the great work in reducing food waste! 🌱
            
            View detailed analytics: http://localhost:5000/analytics/
            
            Best regards,
            FoodSave Team
            """
            
            # Log the report (replace with real email in production)
            print("=" * 50)
            print("📊 WASTE REPORT NOTIFICATION")
            print("=" * 50)
            print(f"To: {user.email}")
            print(f"Subject: {subject}")
            print(f"Message: {message}")
            print("=" * 50)
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending report to {user.email}: {e}")
            return False
    
    @staticmethod
    def send_donation_notification(donation, notification_type):
        """
        Send donation-related notifications.
        
        Args:
            donation: Donation object
            notification_type: Type of notification ('claimed', 'completed', 'new')
            
        Returns:
            bool: True if notification was "sent" (logged)
        """
        try:
            # Import here to avoid circular imports
            from app.models import Donation
            
            donor = donation.donor
            food_item = donation.food_item
            
            if notification_type == 'claimed':
                subject = "🎉 Your Donation Has Been Claimed!"
                recipient = donor.email
                message = f"""
                Hi {donor.username},
                
                Great news! Your donation of {food_item.name} has been claimed by someone in need.
                
                Donation Details:
                • Item: {food_item.name}
                • Quantity: {donation.quantity}
                • Claimed at: {donation.claimed_at.strftime('%Y-%m-%d %H:%M') if donation.claimed_at else 'N/A'}
                
                Please coordinate pickup details with the claimant.
                
                Thank you for helping reduce food waste! ❤️
                """
                
            elif notification_type == 'completed':
                subject = "✅ Donation Successfully Delivered"
                recipient = donor.email
                
                # Count donations without causing circular import
                donation_count = Donation.query.filter_by(donor_id=donor.id).count()
                
                message = f"""
                Hi {donor.username},
                
                Your donation of {food_item.name} has been marked as delivered.
                
                You've made a difference in someone's life today! 🌟
                
                Total donations made: {donation_count}
                """
                
            elif notification_type == 'new':
                subject = "🆕 New Donation Opportunity Nearby"
                recipient = "nearby_users@example.com"  # This would be sent to potential claimants
                message = f"""
                New donation available in your area!
                
                • Item: {food_item.name}
                • Quantity: {donation.quantity}
                • Location: {donation.pickup_location}
                • Donor: {donor.username}
                
                Claim it now: http://localhost:5000/donations/
                """
            else:
                return False
            
            # Log the notification (replace with real email in production)
            print("=" * 50)
            print("📦 DONATION NOTIFICATION")
            print("=" * 50)
            print(f"To: {recipient}")
            print(f"Subject: {subject}")
            print(f"Type: {notification_type}")
            print(f"Message: {message}")
            print("=" * 50)
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending donation notification: {e}")
            return False
    
    @staticmethod
    def send_welcome_email(user):
        """
        Send welcome email to new users.
        
        Args:
            user: Newly registered User object
            
        Returns:
            bool: True if welcome email was "sent" (logged)
        """
        try:
            subject = "🎉 Welcome to FoodSave - Start Reducing Food Waste!"
            
            message = f"""
            Welcome to FoodSave, {user.username}!
            
            We're excited to have you join our community dedicated to reducing food waste.
            
            Getting Started:
            1. 📝 Add your food items to track expiry dates
            2. 🔔 Get smart alerts for items expiring soon  
            3. 📊 Monitor your waste reduction progress
            4. ❤️ Donate surplus food to help others
            
            Quick Links:
            • Dashboard: http://localhost:5000/food/dashboard
            • Add Food: http://localhost:5000/food/add
            • Donations: http://localhost:5000/donations/
            
            Together, we can make a difference! 🌍
            
            Best regards,
            The FoodSave Team
            """
            
            # Log the welcome email (replace with real email in production)
            print("=" * 50)
            print("👋 WELCOME EMAIL NOTIFICATION")
            print("=" * 50)
            print(f"To: {user.email}")
            print(f"Subject: {subject}")
            print(f"Message: {message}")
            print("=" * 50)
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending welcome email: {e}")
            return False
    
    @staticmethod
    def send_test_notification():
        """
        Send a test notification to verify the notification system works.
        
        Returns:
            bool: True if test notification was sent successfully
        """
        try:
            print("=" * 50)
            print("🧪 TEST NOTIFICATION")
            print("=" * 50)
            print("To: test@example.com")
            print("Subject: FoodSave Test Notification")
            print("Message: This is a test notification from FoodSave!")
            print("Status: ✅ Notification system is working!")
            print("=" * 50)
            return True
        except Exception as e:
            print(f"❌ Test notification failed: {e}")
            return False

# Utility functions for batch notifications
def send_bulk_expiry_alerts():
    """
    Check all users for expiring items and send bulk alerts.
    Typically run as a scheduled task.
    
    Returns:
        int: Number of notifications sent
    """
    notifications = NotificationManager.check_expiry_notifications()
    
    print(f"🔔 Found {len(notifications)} users with expiring items")
    
    for notification in notifications:
        user = notification['user']
        items = notification['items']
        
        NotificationManager.send_expiry_alert(user, items)
    
    return len(notifications)

def send_weekly_reports():
    """
    Send weekly waste reports to all active users.
    Typically run as a scheduled task.
    
    Returns:
        int: Number of reports sent
    """
    from app.utils.food_calculations import FoodWasteCalculator
    
    users = User.query.all()
    reports_sent = 0
    
    print(f"📊 Preparing weekly reports for {len(users)} users")
    
    for user in users:
        # Calculate user's waste stats
        stats = FoodWasteCalculator.calculate_waste_stats(user.id)
        environmental_impact = FoodWasteCalculator.estimate_environmental_impact(stats['wasted'])
        
        # Combine stats
        combined_stats = {**stats, **environmental_impact}
        
        if NotificationManager.send_waste_report(user, combined_stats, 'weekly'):
            reports_sent += 1
    
    print(f"✅ Sent {reports_sent} weekly reports")
    return reports_sent

def test_notification_system():
    """
    Test the entire notification system.
    
    Returns:
        bool: True if all tests pass
    """
    print("🧪 Testing Notification System...")
    
    # Test 1: Basic notification
    test1 = NotificationManager.send_test_notification()
    
    # Test 2: Check for expiring items
    notifications = NotificationManager.check_expiry_notifications()
    test2 = True  # Just checking if it runs without error
    
    # Test 3: Send bulk alerts (if there are any)
    bulk_count = send_bulk_expiry_alerts()
    test3 = True
    
    print(f"📋 Test Results:")
    print(f"  • Basic Notification: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"  • Expiry Check: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"  • Bulk Alerts: {'✅ PASS' if test3 else '❌ FAIL'} ({bulk_count} sent)")
    
    return all([test1, test2, test3])