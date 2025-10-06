#!/usr/bin/env python3
"""
Test script to simulate the actual GUI workflow and identify issues
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the workspace to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Setup logging
logging.basicConfig(level=logging.INFO)

async def simulate_gui_email_workflow():
    """Simulate the complete GUI email workflow"""
    print("🎭 Simulating GUI Email Workflow")
    print("=" * 50)
    
    try:
        from core.app_core import QuMailCore
        from utils.config import load_config
        
        # Initialize core (simulating GUI startup)
        print("🚀 Initializing QuMail Core...")
        config = load_config()
        core = QuMailCore(config)
        await core.initialize()
        
        # Simulate user authentication (sravya@qumail.com)
        print("👤 Simulating user authentication...")
        core.current_user = core.UserProfile(
            user_id="sravya_user",
            email="sravya@qumail.com",
            display_name="Sravya",
            password_hash="test_hash",
            sae_id="qumail_sravya_user",
            provider="qumail_native",
            created_at=core.datetime.utcnow(),
            last_login=core.datetime.utcnow()
        )
        
        # Initialize email handler
        await core.email_handler.initialize(core.current_user)
        print(f"✅ User authenticated: {core.current_user.email}")
        
        # Test Case 1: Send email to another QuMail user
        print("\n📧 Test Case 1: Sending email to nazia@qumail.com")
        print("-" * 40)
        
        success1 = await core.send_secure_email(
            to_address="nazia@qumail.com",
            subject="Hello Nazia from Sravya",
            body="This is a test email from Sravya to Nazia through the GUI workflow.",
            security_level="L2"
        )
        
        if success1:
            print("✅ Case 1: Email sent successfully")
            
            # Check if email appears in sender's Sent folder
            sent_emails = core.email_handler.local_email_store.get('Sent', [])
            print(f"📤 Sender's Sent folder: {len(sent_emails)} emails")
            
            if sent_emails:
                last_sent = sent_emails[-1]
                print(f"   Subject: {last_sent.get('subject')}")
                print(f"   To: {last_sent.get('receiver')}")
                print(f"   Body: {last_sent.get('body')}")
            
            # Check if email appears in recipient's Inbox
            nazia_store = core.email_handler.qumail_mock_inboxes.get('nazia@qumail.com', {})
            nazia_inbox = nazia_store.get('Inbox', [])
            print(f"📥 Nazia's Inbox: {len(nazia_inbox)} emails")
            
            if nazia_inbox:
                last_received = nazia_inbox[-1]
                print(f"   Subject: {last_received.get('subject')}")
                print(f"   From: {last_received.get('sender')}")
                print(f"   Body: {last_received.get('body')}")
                case1_success = True
            else:
                print("❌ Case 1: Email not found in Nazia's inbox!")
                case1_success = False
        else:
            print("❌ Case 1: Email sending failed")
            case1_success = False
        
        # Test Case 2: Send email to external provider (Gmail)
        print("\n📧 Test Case 2: Sending email to Gmail")
        print("-" * 40)
        
        success2 = await core.send_secure_email(
            to_address="sravya@gmail.com",
            subject="Test from QuMail to Gmail",
            body="This is a test email from QuMail to Gmail via OAuth.",
            security_level="L2"
        )
        
        if success2:
            print("✅ Case 2: OAuth email sent successfully")
            
            # Check if email appears in sender's Sent folder
            sent_emails = core.email_handler.local_email_store.get('Sent', [])
            print(f"📤 Sender's Sent folder: {len(sent_emails)} emails")
            
            if sent_emails:
                last_sent = sent_emails[-1]
                print(f"   Subject: {last_sent.get('subject')}")
                print(f"   To: {last_sent.get('receiver')}")
                print(f"   Security: {last_sent.get('security_level')}")
                case2_success = True
            else:
                print("❌ Case 2: No email found in Sent folder")
                case2_success = False
        else:
            print("❌ Case 2: OAuth email sending failed")
            case2_success = False
        
        # Test Case 3: Test encryption/decryption display
        print("\n📧 Test Case 3: Testing encryption/decryption display")
        print("-" * 40)
        
        # Send internal email (should show decrypted)
        success3a = await core.send_secure_email(
            to_address="sravya@qumail.com",  # Send to self
            subject="Internal Test Email",
            body="This email should show decrypted content in QuMail inbox.",
            security_level="L2"
        )
        
        if success3a:
            # Check if email shows decrypted content
            inbox_emails = core.email_handler.local_email_store.get('Inbox', [])
            if inbox_emails:
                last_email = inbox_emails[-1]
                body = last_email.get('body', '')
                if 'This email should show decrypted content' in body:
                    print("✅ Case 3a: Internal email shows decrypted content")
                    case3a_success = True
                else:
                    print(f"❌ Case 3a: Internal email shows encrypted content: {body}")
                    case3a_success = False
            else:
                print("❌ Case 3a: No internal email found")
                case3a_success = False
        else:
            print("❌ Case 3a: Internal email sending failed")
            case3a_success = False
        
        # Send external email (should show encrypted)
        success3b = await core.send_secure_email(
            to_address="test@gmail.com",
            subject="External Test Email",
            body="This email should be encrypted for external delivery.",
            security_level="L2"
        )
        
        if success3b:
            # Check if email is properly formatted for external delivery
            sent_emails = core.email_handler.local_email_store.get('Sent', [])
            if sent_emails:
                last_sent = sent_emails[-1]
                if last_sent.get('receiver', '').endswith('@gmail.com'):
                    print("✅ Case 3b: External email properly formatted for encrypted delivery")
                    case3b_success = True
                else:
                    print("❌ Case 3b: External email not properly formatted")
                    case3b_success = False
            else:
                print("❌ Case 3b: No external email found")
                case3b_success = False
        else:
            print("❌ Case 3b: External email sending failed")
            case3b_success = False
        
        case3_success = case3a_success and case3b_success
        
        return case1_success, case2_success, case3_success
        
    except Exception as e:
        print(f"❌ GUI workflow simulation failed with error: {e}")
        logging.error(f"GUI workflow error: {e}", exc_info=True)
        return False, False, False

async def test_email_list_loading():
    """Test email list loading (simulating GUI refresh)"""
    print("\n📋 Testing Email List Loading")
    print("=" * 50)
    
    try:
        from core.app_core import QuMailCore
        from utils.config import load_config
        
        # Initialize core
        config = load_config()
        core = QuMailCore(config)
        await core.initialize()
        
        # Set up user
        core.current_user = core.UserProfile(
            user_id="test_user",
            email="test@qumail.com",
            display_name="Test User",
            password_hash="test_hash",
            sae_id="qumail_test_user",
            provider="qumail_native",
            created_at=core.datetime.utcnow(),
            last_login=core.datetime.utcnow()
        )
        
        await core.email_handler.initialize(core.current_user)
        
        # Send some test emails
        await core.send_secure_email("test@qumail.com", "Test 1", "Body 1", security_level="L2")
        await core.send_secure_email("test@gmail.com", "Test 2", "Body 2", security_level="L2")
        
        # Test loading emails from different folders
        folders = ["Inbox", "Sent", "Drafts", "Quantum Vault", "Spam", "Trash"]
        
        for folder in folders:
            emails = await core.get_email_list(folder, 10)
            print(f"📁 {folder}: {len(emails)} emails")
            
            if emails:
                for i, email in enumerate(emails[:3]):  # Show first 3
                    print(f"   {i+1}. {email.get('subject')} from {email.get('sender')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Email list loading failed: {e}")
        logging.error(f"Email list loading error: {e}", exc_info=True)
        return False

async def main():
    """Run comprehensive GUI workflow tests"""
    print("🚀 Comprehensive GUI Workflow Testing")
    print("Testing the actual workflow that would happen in the GUI")
    print("=" * 60)
    
    # Test 1: Complete GUI workflow
    print("\n🔍 Test 1: Complete GUI Email Workflow")
    case1, case2, case3 = await simulate_gui_email_workflow()
    
    # Test 2: Email list loading
    print("\n🔍 Test 2: Email List Loading")
    list_loading = await test_email_list_loading()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 GUI Workflow Test Results:")
    print("=" * 60)
    
    tests = [
        ("Case 1: QuMail to QuMail", case1),
        ("Case 2: OAuth to Gmail", case2),
        ("Case 3: Encryption Display", case3),
        ("Email List Loading", list_loading)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ WORKING" if result else "❌ NOT WORKING"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests working")
    
    if passed == total:
        print("\n🎉 All GUI workflow tests are working!")
        print("The issue might be in the actual GUI application or how you're testing it.")
        print("\n💡 Suggestions:")
        print("1. Make sure you're running the GUI application correctly")
        print("2. Check if there are any error messages in the GUI")
        print("3. Try refreshing the email list after sending emails")
        print("4. Check if the email composition dialog is working properly")
    else:
        print(f"\n⚠️  {total - passed} tests are failing.")
        print("Let me investigate the specific failing tests...")
    
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)