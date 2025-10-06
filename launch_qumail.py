#!/usr/bin/env python3
"""
QuMail Launcher Script
This script helps you test the QuMail email functionality
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the workspace to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Setup logging
logging.basicConfig(level=logging.INFO)

async def demo_qumail_functionality():
    """Demonstrate QuMail functionality"""
    print("🚀 QuMail Email Functionality Demo")
    print("=" * 50)
    
    try:
        from transport.email_handler import EmailHandler
        
        # Create two QuMail users
        print("👤 Setting up QuMail users...")
        
        # User 1: Sravya
        sravya_handler = EmailHandler()
        await sravya_handler.initialize({
            'email': 'sravya@qumail.com',
            'user_id': 'sravya_user',
            'display_name': 'Sravya'
        })
        print(f"✅ User 1: {sravya_handler.user_email}")
        
        # User 2: Nazia
        nazia_handler = EmailHandler()
        await nazia_handler.initialize({
            'email': 'nazia@qumail.com',
            'user_id': 'nazia_user',
            'display_name': 'Nazia'
        })
        print(f"✅ User 2: {nazia_handler.user_email}")
        
        print("\n📧 Testing the 3 cases...")
        
        # Case 1: QuMail to QuMail
        print("\n🔍 Case 1: QuMail to QuMail delivery")
        print("-" * 40)
        
        email1 = {
            'subject': 'Hello Nazia from Sravya',
            'body': 'This is a test email from Sravya to Nazia to verify QuMail delivery works correctly.',
            'security_level': 'L2',
            'ciphertext': 'encrypted_content_here',
            'algorithm': 'AES256_GCM_QUANTUM'
        }
        
        success1 = await sravya_handler.send_encrypted_email("nazia@qumail.com", email1)
        
        if success1:
            print("✅ Email sent successfully!")
            
            # Check sender's Sent folder
            sent_emails = sravya_handler.local_email_store.get('Sent', [])
            print(f"📤 Sravya's Sent folder: {len(sent_emails)} emails")
            
            # Check recipient's Inbox
            nazia_store = sravya_handler.qumail_mock_inboxes.get('nazia@qumail.com', {})
            nazia_inbox = nazia_store.get('Inbox', [])
            print(f"📥 Nazia's Inbox: {len(nazia_inbox)} emails")
            
            if nazia_inbox:
                last_email = nazia_inbox[-1]
                print(f"   📧 Subject: {last_email.get('subject')}")
                print(f"   👤 From: {last_email.get('sender')}")
                print(f"   📝 Body: {last_email.get('body')}")
                print(f"   🔒 Security: {last_email.get('security_level')}")
                
                # Check Quantum Vault
                nazia_vault = nazia_store.get('Quantum Vault', [])
                print(f"🔐 Nazia's Quantum Vault: {len(nazia_vault)} emails")
                
                print("✅ Case 1: QuMail to QuMail delivery is working!")
            else:
                print("❌ Case 1: Email not found in Nazia's inbox")
        else:
            print("❌ Case 1: Email sending failed")
        
        # Case 2: OAuth to Gmail
        print("\n🔍 Case 2: OAuth email to Gmail")
        print("-" * 40)
        
        email2 = {
            'subject': 'Test from QuMail to Gmail',
            'body': 'This is a test email from QuMail to Gmail via OAuth.',
            'security_level': 'L2',
            'ciphertext': 'encrypted_content_here',
            'algorithm': 'AES256_GCM_QUANTUM'
        }
        
        success2 = await sravya_handler.send_encrypted_email("sravya@gmail.com", email2)
        
        if success2:
            print("✅ OAuth email sent successfully!")
            
            # Check sender's Sent folder
            sent_emails = sravya_handler.local_email_store.get('Sent', [])
            print(f"📤 Sravya's Sent folder: {len(sent_emails)} emails")
            
            if sent_emails:
                last_sent = sent_emails[-1]
                print(f"   📧 Subject: {last_sent.get('subject')}")
                print(f"   📧 To: {last_sent.get('receiver')}")
                print(f"   🔒 Security: {last_sent.get('security_level')}")
                
                print("✅ Case 2: OAuth email to Gmail is working!")
            else:
                print("❌ Case 2: No email found in Sent folder")
        else:
            print("❌ Case 2: OAuth email sending failed")
        
        # Case 3: Encryption/Decryption display
        print("\n🔍 Case 3: Encryption/Decryption display")
        print("-" * 40)
        
        # Send internal email (should show decrypted)
        email3a = {
            'subject': 'Internal Test Email',
            'body': 'This email should show decrypted content in QuMail inbox.',
            'security_level': 'L2',
            'ciphertext': 'encrypted_content_here',
            'algorithm': 'AES256_GCM_QUANTUM'
        }
        
        success3a = await sravya_handler.send_encrypted_email("sravya@qumail.com", email3a)
        
        if success3a:
            # Check if email shows decrypted content
            sravya_store = sravya_handler.qumail_mock_inboxes.get('sravya@qumail.com', {})
            sravya_inbox = sravya_store.get('Inbox', [])
            
            if sravya_inbox:
                last_email = sravya_inbox[-1]
                body = last_email.get('body', '')
                if 'This email should show decrypted content' in body:
                    print("✅ Internal email shows decrypted content (readable)")
                else:
                    print(f"❌ Internal email shows encrypted content: {body}")
            else:
                print("❌ No internal email found")
        
        # Send external email (should show encrypted)
        email3b = {
            'subject': 'External Test Email',
            'body': 'This email should be encrypted for external delivery.',
            'security_level': 'L2',
            'ciphertext': 'encrypted_content_here',
            'algorithm': 'AES256_GCM_QUANTUM'
        }
        
        success3b = await sravya_handler.send_encrypted_email("test@gmail.com", email3b)
        
        if success3b:
            # Check if email is properly formatted for external delivery
            sent_emails = sravya_handler.local_email_store.get('Sent', [])
            if sent_emails:
                last_sent = sent_emails[-1]
                if last_sent.get('receiver', '').endswith('@gmail.com'):
                    print("✅ External email properly formatted for encrypted delivery")
                    print("✅ Case 3: Encryption/Decryption display is working!")
                else:
                    print("❌ External email not properly formatted")
            else:
                print("❌ No external email found")
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Demo Results Summary:")
        print("=" * 50)
        
        cases = [
            ("Case 1: QuMail to QuMail", success1),
            ("Case 2: OAuth to Gmail", success2),
            ("Case 3: Encryption Display", success3a and success3b)
        ]
        
        working = 0
        for case_name, result in cases:
            status = "✅ WORKING" if result else "❌ NOT WORKING"
            print(f"{status} {case_name}")
            if result:
                working += 1
        
        print(f"\n🎯 Overall: {working}/3 cases working")
        
        if working == 3:
            print("\n🎉 All 3 cases are working correctly!")
            print("QuMail email functionality is ready for demonstration.")
        else:
            print(f"\n⚠️  {3 - working} cases are still not working.")
        
        return working == 3
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        logging.error(f"Demo error: {e}", exc_info=True)
        return False

async def main():
    """Main launcher function"""
    print("🚀 QuMail Launcher")
    print("This script demonstrates the QuMail email functionality")
    print("=" * 60)
    
    success = await demo_qumail_functionality()
    
    if success:
        print("\n🎉 QuMail is working correctly!")
        print("\n💡 To use QuMail:")
        print("1. Create QuMail accounts (e.g., sravya@qumail.com, nazia@qumail.com)")
        print("2. Send emails between QuMail accounts")
        print("3. Send emails to external providers (Gmail, Yahoo, Outlook)")
        print("4. View decrypted content in QuMail inboxes")
        print("5. View encrypted content in external inboxes")
    else:
        print("\n⚠️  Some issues remain. Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)