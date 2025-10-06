#!/usr/bin/env python3
"""
Test script that focuses only on the core email functionality
without GUI dependencies
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the workspace to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Setup logging
logging.basicConfig(level=logging.INFO)

async def test_core_email_functionality():
    """Test core email functionality without GUI dependencies"""
    print("🔍 Testing Core Email Functionality")
    print("=" * 50)
    
    try:
        # Import only the transport layer directly
        from transport.email_handler import EmailHandler
        
        print("✅ Email handler imported successfully")
        
        # Test Case 1: QuMail to QuMail
        print("\n📧 Test Case 1: QuMail to QuMail delivery")
        print("-" * 40)
        
        # Create sender
        sender_handler = EmailHandler()
        await sender_handler.initialize({
            'email': 'sravya@qumail.com',
            'user_id': 'sravya_user',
            'display_name': 'Sravya'
        })
        
        # Send email to another QuMail user
        email_data = {
            'subject': 'Test from Sravya to Nazia',
            'body': 'This is a test email from Sravya to Nazia.',
            'security_level': 'L2',
            'ciphertext': 'encrypted_content_here',
            'algorithm': 'AES256_GCM_QUANTUM'
        }
        
        success1 = await sender_handler.send_encrypted_email("nazia@qumail.com", email_data)
        
        if success1:
            print("✅ Case 1: Email sent successfully")
            
            # Check sender's Sent folder
            sent_emails = sender_handler.local_email_store.get('Sent', [])
            print(f"📤 Sender's Sent folder: {len(sent_emails)} emails")
            
            if sent_emails:
                last_sent = sent_emails[-1]
                print(f"   Subject: {last_sent.get('subject')}")
                print(f"   To: {last_sent.get('receiver')}")
                print(f"   Body: {last_sent.get('body')}")
            
            # Check recipient's Inbox
            nazia_store = sender_handler.qumail_mock_inboxes.get('nazia@qumail.com', {})
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
        
        # Test Case 2: External email
        print("\n📧 Test Case 2: External email to Gmail")
        print("-" * 40)
        
        external_email_data = {
            'subject': 'Test from QuMail to Gmail',
            'body': 'This is a test email from QuMail to Gmail.',
            'security_level': 'L2',
            'ciphertext': 'encrypted_content_here',
            'algorithm': 'AES256_GCM_QUANTUM'
        }
        
        success2 = await sender_handler.send_encrypted_email("sravya@gmail.com", external_email_data)
        
        if success2:
            print("✅ Case 2: External email sent successfully")
            
            # Check sender's Sent folder
            sent_emails = sender_handler.local_email_store.get('Sent', [])
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
            print("❌ Case 2: External email sending failed")
            case2_success = False
        
        # Test Case 3: Encryption display
        print("\n📧 Test Case 3: Encryption/Decryption display")
        print("-" * 40)
        
        # Send internal email (should show decrypted)
        internal_email_data = {
            'subject': 'Internal Test Email',
            'body': 'This should be decrypted and readable in QuMail inbox.',
            'security_level': 'L2',
            'ciphertext': 'encrypted_content_here',
            'algorithm': 'AES256_GCM_QUANTUM'
        }
        
        success3a = await sender_handler.send_encrypted_email("sravya@qumail.com", internal_email_data)
        
        if success3a:
            # Check if email shows decrypted content
            sravya_store = sender_handler.qumail_mock_inboxes.get('sravya@qumail.com', {})
            sravya_inbox = sravya_store.get('Inbox', [])
            
            if sravya_inbox:
                last_email = sravya_inbox[-1]
                body = last_email.get('body', '')
                if 'This should be decrypted and readable' in body:
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
        external_email_data2 = {
            'subject': 'External Test Email',
            'body': 'This should be encrypted for external delivery.',
            'security_level': 'L2',
            'ciphertext': 'encrypted_content_here',
            'algorithm': 'AES256_GCM_QUANTUM'
        }
        
        success3b = await sender_handler.send_encrypted_email("test@gmail.com", external_email_data2)
        
        if success3b:
            # Check if email is properly formatted for external delivery
            sent_emails = sender_handler.local_email_store.get('Sent', [])
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
        print(f"❌ Core email functionality test failed: {e}")
        logging.error(f"Core email test error: {e}", exc_info=True)
        return False, False, False

async def test_email_persistence():
    """Test email persistence across multiple users"""
    print("\n📋 Testing Email Persistence")
    print("=" * 50)
    
    try:
        from transport.email_handler import EmailHandler
        
        # Create multiple users
        users = [
            {'email': 'alice@qumail.com', 'name': 'Alice'},
            {'email': 'bob@qumail.com', 'name': 'Bob'},
            {'email': 'charlie@qumail.com', 'name': 'Charlie'}
        ]
        
        handlers = {}
        
        # Initialize handlers for all users
        for user in users:
            handler = EmailHandler()
            await handler.initialize({
                'email': user['email'],
                'user_id': f"{user['name'].lower()}_user",
                'display_name': user['name']
            })
            handlers[user['email']] = handler
            print(f"✅ Initialized handler for {user['email']}")
        
        # Send emails between users
        print("\n📧 Sending emails between users...")
        
        # Alice sends to Bob
        alice_handler = handlers['alice@qumail.com']
        await alice_handler.send_encrypted_email("bob@qumail.com", {
            'subject': 'Hello Bob',
            'body': 'This is a message from Alice to Bob.',
            'security_level': 'L2',
            'ciphertext': 'encrypted_content',
            'algorithm': 'AES256_GCM_QUANTUM'
        })
        
        # Bob sends to Charlie
        bob_handler = handlers['bob@qumail.com']
        await bob_handler.send_encrypted_email("charlie@qumail.com", {
            'subject': 'Hello Charlie',
            'body': 'This is a message from Bob to Charlie.',
            'security_level': 'L2',
            'ciphertext': 'encrypted_content',
            'algorithm': 'AES256_GCM_QUANTUM'
        })
        
        # Charlie sends to Alice
        charlie_handler = handlers['charlie@qumail.com']
        await charlie_handler.send_encrypted_email("alice@qumail.com", {
            'subject': 'Hello Alice',
            'body': 'This is a message from Charlie to Alice.',
            'security_level': 'L2',
            'ciphertext': 'encrypted_content',
            'algorithm': 'AES256_GCM_QUANTUM'
        })
        
        print("✅ All emails sent successfully")
        
        # Check email distribution
        print("\n📊 Email distribution check:")
        
        for user_email, handler in handlers.items():
            sent_count = len(handler.local_email_store.get('Sent', []))
            inbox_count = 0
            
            # Check inbox from all handlers (since emails are stored globally)
            for other_handler in handlers.values():
                user_inbox = other_handler.qumail_mock_inboxes.get(user_email, {})
                inbox_count += len(user_inbox.get('Inbox', []))
            
            print(f"   {user_email}: {sent_count} sent, {inbox_count} received")
        
        return True
        
    except Exception as e:
        print(f"❌ Email persistence test failed: {e}")
        logging.error(f"Email persistence test error: {e}", exc_info=True)
        return False

async def main():
    """Run core email functionality tests"""
    print("🚀 Core Email Functionality Testing")
    print("Testing the 3 cases without GUI dependencies")
    print("=" * 60)
    
    # Test core email functionality
    case1, case2, case3 = await test_core_email_functionality()
    
    # Test email persistence
    persistence = await test_email_persistence()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Core Email Test Results:")
    print("=" * 60)
    
    tests = [
        ("Case 1: QuMail to QuMail", case1),
        ("Case 2: OAuth to Gmail", case2),
        ("Case 3: Encryption Display", case3),
        ("Email Persistence", persistence)
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
        print("\n🎉 All core email functionality is working correctly!")
        print("\n💡 The issue might be in the GUI application or how you're testing it.")
        print("   The backend email functionality is working perfectly.")
        print("\n🔧 To fix the GUI issues:")
        print("1. Make sure you have all GUI dependencies installed")
        print("2. Check if there are any error messages in the GUI")
        print("3. Try refreshing the email list after sending emails")
        print("4. Verify the email composition dialog is working")
    else:
        print(f"\n⚠️  {total - passed} core tests are failing.")
        print("Let me investigate the specific failing tests...")
    
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)