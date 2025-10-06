#!/usr/bin/env python3
"""
Debug script to identify the specific 3 cases that are not working
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the workspace to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Setup logging
logging.basicConfig(level=logging.INFO)

async def test_case_1_qumail_to_qumail():
    """Test Case 1: QuMail to QuMail delivery"""
    print("🔍 Testing Case 1: QuMail to QuMail delivery")
    print("=" * 50)
    
    try:
        from transport.email_handler import EmailHandler
        
        # Create sender (sravya@qumail.com)
        sender_handler = EmailHandler()
        await sender_handler.initialize({
            'email': 'sravya@qumail.com',
            'user_id': 'sravya_user',
            'display_name': 'Sravya'
        })
        
        print(f"✅ Sender initialized: {sender_handler.user_email}")
        
        # Create recipient (nazia@qumail.com) 
        recipient_handler = EmailHandler()
        await recipient_handler.initialize({
            'email': 'nazia@qumail.com',
            'user_id': 'nazia_user', 
            'display_name': 'Nazia'
        })
        
        print(f"✅ Recipient initialized: {recipient_handler.user_email}")
        
        # Send email from Sravya to Nazia
        email_data = {
            'subject': 'Test from Sravya to Nazia',
            'body': 'This is a test email from Sravya to Nazia to verify delivery.',
            'security_level': 'L2',
            'ciphertext': 'encrypted_content_here',
            'algorithm': 'AES256_GCM_QUANTUM'
        }
        
        print(f"📧 Sending email: '{email_data['subject']}'")
        success = await sender_handler.send_encrypted_email("nazia@qumail.com", email_data)
        
        if success:
            print("✅ Email sent successfully")
            
            # Check sender's Sent folder
            sent_emails = sender_handler.local_email_store.get('Sent', [])
            print(f"📤 Sender's Sent folder: {len(sent_emails)} emails")
            
            if sent_emails:
                last_sent = sent_emails[-1]
                print(f"   Subject: {last_sent.get('subject')}")
                print(f"   To: {last_sent.get('receiver')}")
                print(f"   Body: {last_sent.get('body')}")
                print(f"   Security: {last_sent.get('security_level')}")
            
            # Check if email appears in Nazia's inbox
            nazia_store = sender_handler.qumail_mock_inboxes.get('nazia@qumail.com', {})
            nazia_inbox = nazia_store.get('Inbox', [])
            print(f"📥 Nazia's Inbox: {len(nazia_inbox)} emails")
            
            if nazia_inbox:
                last_received = nazia_inbox[-1]
                print(f"   Subject: {last_received.get('subject')}")
                print(f"   From: {last_received.get('sender')}")
                print(f"   Body: {last_received.get('body')}")
                print(f"   Security: {last_received.get('security_level')}")
                
                # Check if it's in Quantum Vault
                nazia_vault = nazia_store.get('Quantum Vault', [])
                print(f"🔐 Nazia's Quantum Vault: {len(nazia_vault)} emails")
                
                return True
            else:
                print("❌ Email not found in Nazia's inbox!")
                return False
        else:
            print("❌ Email sending failed")
            return False
            
    except Exception as e:
        print(f"❌ Case 1 failed with error: {e}")
        logging.error(f"Case 1 error: {e}", exc_info=True)
        return False

async def test_case_2_oauth_to_gmail():
    """Test Case 2: OAuth email to Gmail"""
    print("\n🔍 Testing Case 2: OAuth email to Gmail")
    print("=" * 50)
    
    try:
        from transport.email_handler import EmailHandler
        
        # Create sender
        sender_handler = EmailHandler()
        await sender_handler.initialize({
            'email': 'sravya@qumail.com',
            'user_id': 'sravya_user',
            'display_name': 'Sravya'
        })
        
        print(f"✅ Sender initialized: {sender_handler.user_email}")
        
        # Send email to Gmail
        email_data = {
            'subject': 'Test from QuMail to Gmail',
            'body': 'This is a test email from QuMail to Gmail via OAuth.',
            'security_level': 'L2',
            'ciphertext': 'encrypted_content_here',
            'algorithm': 'AES256_GCM_QUANTUM'
        }
        
        print(f"📧 Sending email to Gmail: '{email_data['subject']}'")
        success = await sender_handler.send_encrypted_email("sravya@gmail.com", email_data)
        
        if success:
            print("✅ OAuth email sent successfully")
            
            # Check sender's Sent folder
            sent_emails = sender_handler.local_email_store.get('Sent', [])
            print(f"📤 Sender's Sent folder: {len(sent_emails)} emails")
            
            if sent_emails:
                last_sent = sent_emails[-1]
                print(f"   Subject: {last_sent.get('subject')}")
                print(f"   To: {last_sent.get('receiver')}")
                print(f"   Security: {last_sent.get('security_level')}")
                
                # Check if it's encrypted for external delivery
                if last_sent.get('receiver', '').endswith('@gmail.com'):
                    print("✅ Email properly formatted for external delivery")
                    return True
                else:
                    print("❌ Email not properly formatted for external delivery")
                    return False
            else:
                print("❌ No emails found in Sent folder")
                return False
        else:
            print("❌ OAuth email sending failed")
            return False
            
    except Exception as e:
        print(f"❌ Case 2 failed with error: {e}")
        logging.error(f"Case 2 error: {e}", exc_info=True)
        return False

async def test_case_3_encryption_display():
    """Test Case 3: Encryption/Decryption display"""
    print("\n🔍 Testing Case 3: Encryption/Decryption display")
    print("=" * 50)
    
    try:
        from transport.email_handler import EmailHandler
        
        # Create sender
        sender_handler = EmailHandler()
        await sender_handler.initialize({
            'email': 'test@qumail.com',
            'user_id': 'test_user',
            'display_name': 'Test User'
        })
        
        print(f"✅ Sender initialized: {sender_handler.user_email}")
        
        # Test 1: QuMail to QuMail (should show decrypted)
        print("\n📧 Test 3a: QuMail to QuMail (should show decrypted)")
        qumail_email = {
            'subject': 'QuMail Internal Email',
            'body': 'This should be decrypted and readable in QuMail inbox.',
            'security_level': 'L2',
            'ciphertext': 'encrypted_content_here',
            'algorithm': 'AES256_GCM_QUANTUM'
        }
        
        success1 = await sender_handler.send_encrypted_email("test@qumail.com", qumail_email)
        
        if success1:
            # Check if email shows decrypted content
            qumail_store = sender_handler.qumail_mock_inboxes.get('test@qumail.com', {})
            qumail_inbox = qumail_store.get('Inbox', [])
            
            if qumail_inbox:
                last_email = qumail_inbox[-1]
                body = last_email.get('body', '')
                if 'This should be decrypted and readable' in body:
                    print("✅ QuMail to QuMail shows decrypted content")
                    qumail_success = True
                else:
                    print(f"❌ QuMail to QuMail shows encrypted content: {body}")
                    qumail_success = False
            else:
                print("❌ No email found in QuMail inbox")
                qumail_success = False
        else:
            print("❌ QuMail to QuMail email failed")
            qumail_success = False
        
        # Test 2: QuMail to External (should show encrypted)
        print("\n📧 Test 3b: QuMail to External (should show encrypted)")
        external_email = {
            'subject': 'QuMail External Email',
            'body': 'This should be encrypted for external delivery.',
            'security_level': 'L2',
            'ciphertext': 'encrypted_content_here',
            'algorithm': 'AES256_GCM_QUANTUM'
        }
        
        success2 = await sender_handler.send_encrypted_email("external@gmail.com", external_email)
        
        if success2:
            # Check if email shows encrypted content for external delivery
            sent_emails = sender_handler.local_email_store.get('Sent', [])
            if sent_emails:
                last_sent = sent_emails[-1]
                if last_sent.get('receiver', '').endswith('@gmail.com'):
                    print("✅ External email properly formatted for encrypted delivery")
                    external_success = True
                else:
                    print("❌ External email not properly formatted")
                    external_success = False
            else:
                print("❌ No external email found in Sent folder")
                external_success = False
        else:
            print("❌ External email sending failed")
            external_success = False
        
        return qumail_success and external_success
        
    except Exception as e:
        print(f"❌ Case 3 failed with error: {e}")
        logging.error(f"Case 3 error: {e}", exc_info=True)
        return False

async def main():
    """Run all 3 test cases to identify issues"""
    print("🚀 Debugging QuMail Email Issues")
    print("Testing the 3 cases that are not working")
    print("=" * 60)
    
    test_cases = [
        ("Case 1: QuMail to QuMail", test_case_1_qumail_to_qumail),
        ("Case 2: OAuth to Gmail", test_case_2_oauth_to_gmail),
        ("Case 3: Encryption Display", test_case_3_encryption_display)
    ]
    
    results = []
    
    for case_name, test_func in test_cases:
        print(f"\n🔍 Running: {case_name}")
        try:
            result = await test_func()
            results.append((case_name, result))
        except Exception as e:
            print(f"❌ {case_name} failed with exception: {e}")
            results.append((case_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Debug Results Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for case_name, result in results:
        status = "✅ WORKING" if result else "❌ NOT WORKING"
        print(f"{status} {case_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} cases working")
    
    if passed == total:
        print("🎉 All 3 cases are working correctly!")
    else:
        print(f"⚠️  {total - passed} cases are still not working.")
        print("\nLet me investigate the specific issues...")
    
    return results

if __name__ == "__main__":
    results = asyncio.run(main())
    
    # Show which specific cases are failing
    failing_cases = [name for name, result in results if not result]
    if failing_cases:
        print(f"\n🔍 Failing cases: {', '.join(failing_cases)}")
        print("Let me fix these specific issues...")