#!/usr/bin/env python3
"""
Simple test script to verify QuMail email functionality
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the workspace to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Setup logging
logging.basicConfig(level=logging.INFO)

async def test_email_handler_directly():
    """Test email handler directly without full core initialization"""
    print("🧪 Testing Email Handler directly...")
    
    try:
        from transport.email_handler import EmailHandler
        
        # Create email handler
        handler = EmailHandler()
        
        # Simulate user profile
        user_profile = {
            'email': 'sravya@qumail.com',
            'user_id': 'test_user_1',
            'display_name': 'Sravya'
        }
        
        # Initialize handler
        await handler.initialize(user_profile)
        
        print(f"✅ Email handler initialized for {user_profile['email']}")
        
        # Test QuMail to QuMail delivery
        test_encrypted_data = {
            'subject': 'Test QuMail Delivery',
            'body': 'This is a test email sent from QuMail to QuMail.',
            'security_level': 'L2',
            'ciphertext': 'encrypted_content_here',
            'algorithm': 'AES256_GCM_QUANTUM'
        }
        
        print("📧 Sending test email to nazia@qumail.com")
        
        success = await handler.send_encrypted_email("nazia@qumail.com", test_encrypted_data)
        
        if success:
            print("✅ Email sent successfully")
            
            # Check sender's Sent folder
            sent_emails = handler.local_email_store.get('Sent', [])
            print(f"📤 Sender's Sent folder has {len(sent_emails)} emails")
            
            if sent_emails:
                last_sent = sent_emails[-1]
                print(f"   Last sent: '{last_sent.get('subject')}' to {last_sent.get('receiver')}")
                print(f"   Body: {last_sent.get('body', 'No body')}")
                print(f"   Security: {last_sent.get('security_level')}")
            
            # Check recipient's Inbox
            recipient_store = handler.qumail_mock_inboxes.get('nazia@qumail.com', {})
            inbox_emails = recipient_store.get('Inbox', [])
            print(f"📥 Recipient's Inbox has {len(inbox_emails)} emails")
            
            if inbox_emails:
                last_received = inbox_emails[-1]
                print(f"   Last received: '{last_received.get('subject')}' from {last_received.get('sender')}")
                print(f"   Body: {last_received.get('body', 'No body')}")
                print(f"   Security: {last_received.get('security_level')}")
                
                # Check if it's also in Quantum Vault
                vault_emails = recipient_store.get('Quantum Vault', [])
                print(f"🔐 Quantum Vault has {len(vault_emails)} emails")
            
            return True
        else:
            print("❌ Email sending failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        logging.error(f"Email handler test failed: {e}", exc_info=True)
        return False

async def test_external_email():
    """Test external email sending"""
    print("\n🧪 Testing external email sending...")
    
    try:
        from transport.email_handler import EmailHandler
        
        # Create email handler
        handler = EmailHandler()
        
        # Simulate user profile
        user_profile = {
            'email': 'test@qumail.com',
            'user_id': 'test_user_2',
            'display_name': 'Test User'
        }
        
        # Initialize handler
        await handler.initialize(user_profile)
        
        print(f"✅ Email handler initialized for {user_profile['email']}")
        
        # Test external email
        test_encrypted_data = {
            'subject': 'Test External Email',
            'body': 'This is a test email sent from QuMail to Gmail.',
            'security_level': 'L2',
            'ciphertext': 'encrypted_content_here',
            'algorithm': 'AES256_GCM_QUANTUM'
        }
        
        print("📧 Sending test email to test@gmail.com")
        
        success = await handler.send_encrypted_email("test@gmail.com", test_encrypted_data)
        
        if success:
            print("✅ External email sent successfully")
            
            # Check sender's Sent folder
            sent_emails = handler.local_email_store.get('Sent', [])
            print(f"📤 Sender's Sent folder has {len(sent_emails)} emails")
            
            if sent_emails:
                last_sent = sent_emails[-1]
                print(f"   Last sent: '{last_sent.get('subject')}' to {last_sent.get('receiver')}")
                print(f"   Security: {last_sent.get('security_level')}")
            
            return True
        else:
            print("❌ External email sending failed")
            return False
            
    except Exception as e:
        print(f"❌ External email test failed with error: {e}")
        logging.error(f"External email test failed: {e}", exc_info=True)
        return False

async def main():
    """Run email functionality tests"""
    print("🚀 Starting QuMail Email Functionality Tests")
    print("=" * 50)
    
    tests = [
        ("QuMail to QuMail Delivery", test_email_handler_directly),
        ("External Email Delivery", test_external_email)
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