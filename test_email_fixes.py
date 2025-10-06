#!/usr/bin/env python3
"""
Test script to verify QuMail email functionality fixes
Tests QuMail to QuMail delivery and OAuth email sending
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the workspace to Python path
sys.path.insert(0, str(Path(__file__).parent))

from core.app_core import QuMailCore
from transport.email_handler import EmailHandler
from auth.identity_manager import IdentityManager
from db.secure_storage import SecureStorage
from utils.config import load_config

async def test_qumail_to_qumail_delivery():
    """Test QuMail to QuMail email delivery"""
    print("🧪 Testing QuMail to QuMail email delivery...")
    
    try:
        # Initialize core
        config = load_config()
        core = QuMailCore(config)
        await core.initialize()
        
        # Create test users
        user1_email = "sravya@qumail.com"
        user2_email = "nazia@qumail.com"
        
        # Simulate user1 authentication
        core.current_user = core.UserProfile(
            user_id="test_user_1",
            email=user1_email,
            display_name="Sravya",
            password_hash="test_hash",
            sae_id="qumail_test_user_1",
            provider="qumail_native",
            created_at=core.datetime.utcnow(),
            last_login=core.datetime.utcnow()
        )
        
        # Initialize email handler for user1
        await core.email_handler.initialize(core.current_user)
        
        print(f"✅ User1 ({user1_email}) initialized")
        
        # Send email from user1 to user2
        test_subject = "Test QuMail Delivery"
        test_body = "This is a test email sent from QuMail to QuMail to verify delivery works correctly."
        
        print(f"📧 Sending email from {user1_email} to {user2_email}")
        
        success = await core.send_secure_email(
            to_address=user2_email,
            subject=test_subject,
            body=test_body,
            security_level="L2"
        )
        
        if success:
            print("✅ Email sent successfully")
            
            # Check if email appears in user1's Sent folder
            sent_emails = core.email_handler.local_email_store.get('Sent', [])
            print(f"📤 User1 Sent folder has {len(sent_emails)} emails")
            
            if sent_emails:
                last_sent = sent_emails[-1]
                print(f"   Last sent: {last_sent.get('subject')} to {last_sent.get('receiver')}")
            
            # Check if email appears in user2's Inbox
            user2_store = core.email_handler.qumail_mock_inboxes.get(user2_email.lower(), {})
            inbox_emails = user2_store.get('Inbox', [])
            print(f"📥 User2 Inbox has {len(inbox_emails)} emails")
            
            if inbox_emails:
                last_received = inbox_emails[-1]
                print(f"   Last received: {last_received.get('subject')} from {last_received.get('sender')}")
                print(f"   Body preview: {last_received.get('preview', 'No preview')}")
                
                # Check if it's also in Quantum Vault
                vault_emails = user2_store.get('Quantum Vault', [])
                print(f"🔐 User2 Quantum Vault has {len(vault_emails)} emails")
            
            return True
        else:
            print("❌ Email sending failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        logging.error(f"QuMail to QuMail test failed: {e}", exc_info=True)
        return False

async def test_oauth_email_delivery():
    """Test OAuth email delivery to external providers"""
    print("\n🧪 Testing OAuth email delivery...")
    
    try:
        # Initialize core
        config = load_config()
        core = QuMailCore(config)
        await core.initialize()
        
        # Create test user
        user_email = "test@qumail.com"
        
        # Simulate user authentication
        core.current_user = core.UserProfile(
            user_id="test_user_oauth",
            email=user_email,
            display_name="Test User",
            password_hash="test_hash",
            sae_id="qumail_test_user_oauth",
            provider="qumail_native",
            created_at=core.datetime.utcnow(),
            last_login=core.datetime.utcnow()
        )
        
        # Initialize email handler
        await core.email_handler.initialize(core.current_user)
        
        print(f"✅ User ({user_email}) initialized")
        
        # Test sending to Gmail
        gmail_address = "test@gmail.com"
        test_subject = "Test OAuth Email"
        test_body = "This is a test email sent from QuMail to Gmail to verify OAuth delivery works."
        
        print(f"📧 Sending email from {user_email} to {gmail_address}")
        
        success = await core.send_secure_email(
            to_address=gmail_address,
            subject=test_subject,
            body=test_body,
            security_level="L2"
        )
        
        if success:
            print("✅ OAuth email sent successfully")
            
            # Check if email appears in Sent folder
            sent_emails = core.email_handler.local_email_store.get('Sent', [])
            print(f"📤 Sent folder has {len(sent_emails)} emails")
            
            if sent_emails:
                last_sent = sent_emails[-1]
                print(f"   Last sent: {last_sent.get('subject')} to {last_sent.get('receiver')}")
                print(f"   Security level: {last_sent.get('security_level')}")
            
            return True
        else:
            print("❌ OAuth email sending failed")
            return False
            
    except Exception as e:
        print(f"❌ OAuth test failed with error: {e}")
        logging.error(f"OAuth email test failed: {e}", exc_info=True)
        return False

async def test_email_display_format():
    """Test email display format and encryption handling"""
    print("\n🧪 Testing email display format...")
    
    try:
        # Initialize core
        config = load_config()
        core = QuMailCore(config)
        await core.initialize()
        
        # Create test user
        user_email = "display@qumail.com"
        
        # Simulate user authentication
        core.current_user = core.UserProfile(
            user_id="test_user_display",
            email=user_email,
            display_name="Display Test User",
            password_hash="test_hash",
            sae_id="qumail_test_user_display",
            provider="qumail_native",
            created_at=core.datetime.utcnow(),
            last_login=core.datetime.utcnow()
        )
        
        # Initialize email handler
        await core.email_handler.initialize(core.current_user)
        
        print(f"✅ User ({user_email}) initialized")
        
        # Send test email
        test_subject = "Display Format Test"
        test_body = "This email tests the display format and encryption handling in QuMail."
        
        success = await core.send_secure_email(
            to_address=user_email,  # Send to self
            subject=test_subject,
            body=test_body,
            security_level="L2"
        )
        
        if success:
            print("✅ Test email sent successfully")
            
            # Check email format
            inbox_emails = core.email_handler.local_email_store.get('Inbox', [])
            if inbox_emails:
                email = inbox_emails[-1]
                print(f"📧 Email format check:")
                print(f"   Subject: {email.get('subject')}")
                print(f"   Body: {email.get('body')}")
                print(f"   Preview: {email.get('preview')}")
                print(f"   Security Level: {email.get('security_level')}")
                print(f"   Sender: {email.get('sender')}")
                print(f"   Receiver: {email.get('receiver')}")
                
                # Check if all required fields are present
                required_fields = ['subject', 'body', 'preview', 'security_level', 'sender', 'receiver']
                missing_fields = [field for field in required_fields if not email.get(field)]
                
                if not missing_fields:
                    print("✅ All required email fields present")
                    return True
                else:
                    print(f"❌ Missing fields: {missing_fields}")
                    return False
            else:
                print("❌ No emails found in inbox")
                return False
        else:
            print("❌ Test email sending failed")
            return False
            
    except Exception as e:
        print(f"❌ Display format test failed with error: {e}")
        logging.error(f"Display format test failed: {e}", exc_info=True)
        return False

async def main():
    """Run all email functionality tests"""
    print("🚀 Starting QuMail Email Functionality Tests")
    print("=" * 50)
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    tests = [
        ("QuMail to QuMail Delivery", test_qumail_to_qumail_delivery),
        ("OAuth Email Delivery", test_oauth_email_delivery),
        ("Email Display Format", test_email_display_format)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! QuMail email functionality is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the logs for details.")
    
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)