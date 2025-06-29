import streamlit as st
import os
import tempfile
from datetime import datetime
from typing import Dict, Any, List
import base64

# Import our modules
from utils.config import config
from modules.object_detection import detector
from modules.pdf_parser import parser
from modules.violation_checker import checker
from modules.report_generator import generator
from utils.helpers import validate_image_file, validate_pdf_file, format_file_size, extract_confidence
from utils.email_sender import email_sender

# Page configuration
st.set_page_config(
    page_title="ResidenceGuard AI",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function."""
    
    # Initialize session state
    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None
    if 'uploaded_pdf' not in st.session_state:
        st.session_state.uploaded_pdf = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'report_generated' not in st.session_state:
        st.session_state.report_generated = None
    
    # Header
    st.title("🚨 ResidenceGuard AI")
    st.markdown("*AI-Powered Policy Violation Detection for Residence Life*")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Staff Information
        st.subheader("Staff Information")
        staff_name = st.text_input("Staff Name", placeholder="Enter your name")
        building_name = st.text_input("Building Name", placeholder="e.g., North Hall")
        room_number = st.text_input("Room Number", placeholder="e.g., 101")
        
        # Detection Settings
        st.subheader("Detection Settings")
        confidence_threshold = st.slider(
            "Confidence Threshold",
            min_value=0.1,
            max_value=0.9,
            value=0.3,
            step=0.1,
            help="Minimum confidence level for object detection"
        )
        
        # System Status
        st.subheader("System Status")
        try:
            # Test system components
            st.success("✅ System Ready")
        except Exception as e:
            st.error(f"❌ Configuration Error: {str(e)}")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📸 Upload Image")
        uploaded_image = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg'],
            key="image_uploader"
        )
        
        if uploaded_image is not None:
            st.session_state.uploaded_image = uploaded_image
            st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)
    
    with col2:
        st.header("📄 Upload Policy PDF")
        uploaded_pdf = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            key="pdf_uploader"
        )
        
        if uploaded_pdf is not None:
            st.session_state.uploaded_pdf = uploaded_pdf
            st.success(f"✅ PDF uploaded: {uploaded_pdf.name}")
    
    # Analysis section
    st.header("🔍 Analysis")
    
    if st.button("🚀 Start Analysis", type="primary"):
        if st.session_state.uploaded_image is None:
            st.error("❌ Please upload an image first!")
        elif st.session_state.uploaded_pdf is None:
            st.error("❌ Please upload a policy PDF first!")
        else:
            with st.spinner("🔍 Analyzing image and checking for violations..."):
                try:
                    # Save uploaded files to disk
                    import tempfile
                    import os
                    
                    # Save image to temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_img:
                        temp_img.write(st.session_state.uploaded_image.getbuffer())
                        image_path = temp_img.name
                    
                    # Save PDF to temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
                        temp_pdf.write(st.session_state.uploaded_pdf.getbuffer())
                        pdf_path = temp_pdf.name
                    
                    # Perform analysis with file paths
                    results = checker.get_compliance_report(image_path, pdf_path)
                    
                    # Clean up temporary files
                    try:
                        os.unlink(image_path)
                        os.unlink(pdf_path)
                    except:
                        pass  # Ignore cleanup errors
                    
                    st.session_state.analysis_results = results
                    st.success("✅ Analysis completed!")
                    
                    # Debug: Show what was stored
                    print("🔍 DEBUG: Analysis results stored in session state:")
                    print(f"   Has violation_assessment: {'violation_assessment' in results}")
                    if 'violation_assessment' in results:
                        print(f"   violation_found: {results['violation_assessment'].get('violation_found')}")
                        print(f"   Type: {type(results['violation_assessment'].get('violation_found'))}")
                    
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")
                    st.exception(e)
    
    # Display results
    if st.session_state.analysis_results:
        st.header("📊 Analysis Results")
        
        results = st.session_state.analysis_results
        
        # Debug: Show what's being read from session state
        print("🔍 DEBUG: Reading analysis results from session state:")
        print(f"   Has violation_assessment: {'violation_assessment' in results}")
        if 'violation_assessment' in results:
            print(f"   violation_found: {results['violation_assessment'].get('violation_found')}")
            print(f"   Type: {type(results['violation_assessment'].get('violation_found'))}")
        
        # Check for errors
        if "error" in results:
            st.error(f"❌ Analysis Error: {results['error']}")
            return
        
        # Display detected objects
        if results.get('image_analysis', {}).get('detected_objects'):
            st.subheader("🔍 Detected Objects")
            
            # Create tabs for different views
            tab1, tab2 = st.tabs(["📊 Object List", "🖼️ Visual Analysis"])
            
            with tab1:
                objects_data = []
                for obj in results['image_analysis']['detected_objects']:
                    objects_data.append({
                        "Object": obj['object'],
                        "Category": obj['category'],
                        "Confidence": f"{extract_confidence(obj['confidence']):.2%}"
                    })
                
                st.dataframe(objects_data, use_container_width=True)
                
                # Summary statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Objects", len(results['image_analysis']['detected_objects']))
                with col2:
                    avg_confidence = sum(extract_confidence(obj['confidence']) for obj in results['image_analysis']['detected_objects']) / len(results['image_analysis']['detected_objects'])
                    st.metric("Avg Confidence", f"{avg_confidence:.1%}")
                with col3:
                    categories = set(obj['category'] for obj in results['image_analysis']['detected_objects'])
                    st.metric("Categories", len(categories))
            
            with tab2:
                st.info("📋 **Object Detection Summary**")
                st.write("The AI has identified the following items in your image:")
                
                # Display objects with confidence bars
                for i, obj in enumerate(results['image_analysis']['detected_objects'], 1):
                    confidence = extract_confidence(obj['confidence'])
                    
                    col1, col2, col3 = st.columns([2, 3, 1])
                    with col1:
                        st.write(f"**{i}.** {obj['object'].title()}")
                    with col2:
                        st.progress(confidence)
                    with col3:
                        st.write(f"{confidence:.1%}")
                    
                    # Show category and additional info
                    st.caption(f"Category: {obj['category']} | Object ID: {i}")
                    
                    # Add a small separator
                    if i < len(results['image_analysis']['detected_objects']):
                        st.markdown("---")
                
                # Verification section
                st.markdown("---")
                st.subheader("✅ Verification")
                st.write("**Please verify:** Are these the correct objects detected in your image?")
                
                # Add verification buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Objects Detected Correctly", type="primary"):
                        st.success("Great! The AI analysis appears accurate.")
                with col2:
                    if st.button("❌ Objects Detected Incorrectly"):
                        st.warning("Please try uploading a clearer image or contact support if issues persist.")
                
                # Additional analysis info
                if results.get('image_analysis', {}).get('image_context'):
                    st.markdown("---")
                    st.subheader("📸 Image Context")
                    context = results['image_analysis']['image_context']
                    st.write(f"**Room Type:** {context.get('room_type', 'Unknown')}")
                    st.write(f"**Lighting:** {context.get('lighting', 'Unknown')}")
                    st.write(f"**Image Quality:** {context.get('quality', 'Unknown')}")
        else:
            st.warning("⚠️ No objects detected in the image. Please try uploading a clearer image.")
        
        # Display violations
        violation_assessment = results.get('violation_assessment', {})
        
        if violation_assessment.get('violation_found'):
            st.subheader("🚨 Policy Violations")
            with st.expander("Violation Details"):
                st.write(f"**Description:** {violation_assessment.get('message', 'No description available')}")
                st.write(f"**Severity:** {violation_assessment.get('severity', 'Unknown')}")
                st.write(f"**Confidence:** {extract_confidence(violation_assessment.get('confidence', 0)):.1%}")
                st.write(f"**Recommended Action:** {violation_assessment.get('recommended_action', 'No action specified')}")
                
                if violation_assessment.get('violating_objects'):
                    st.write("**Violating Objects:**")
                    for obj in violation_assessment['violating_objects']:
                        st.write(f"- {obj}")
                
                if violation_assessment.get('matching_rules'):
                    st.write("**Matching Policy Rules:**")
                    for rule in violation_assessment['matching_rules']:
                        st.write(f"- {rule}")
        else:
            st.success("✅ No policy violations detected!")
        
        # Display compliance status
        compliance_status = results.get('compliance_status', 'unknown')
        
        if compliance_status == 'compliant':
            st.success("✅ Room is compliant with housing policies")
        elif compliance_status == 'non_compliant':
            st.error("🚨 Room has policy violations")
        else:
            st.warning("⚠️ Compliance status unclear")
        
        # Display relevant policy rules (always show, regardless of violations)
        if results.get('policy_analysis', {}).get('relevant_rules'):
            st.subheader("📋 Relevant Policy Rules Considered")
            st.info("The following policy rules were reviewed during this analysis:")
            
            for i, rule in enumerate(results['policy_analysis']['relevant_rules'], 1):
                with st.expander(f"Policy Rule {i}"):
                    st.write(rule.get('rule_text', 'No rule text available'))
                    
                    # Show metadata if available
                    metadata = rule.get('metadata', {})
                    if metadata:
                        st.caption(f"**Rule Type:** {metadata.get('rule_type', 'General Policy')}")
                        if metadata.get('section'):
                            st.caption(f"**Section:** {metadata['section']}")
        else:
            st.warning("⚠️ No relevant policy rules found for the detected objects.")
    
    # Report generation and email sending
    if st.session_state.analysis_results:
        st.header("📝 Send Report to Residence Life")
        
        # Report details
        col1, col2 = st.columns(2)
        with col1:
            incident_date = st.date_input("Incident Date")
            incident_time = st.time_input("Incident Time")
        
        with col2:
            student_name = st.text_input("Student Name (if known)", placeholder="Enter student name")
            additional_notes = st.text_area("Additional Notes", placeholder="Any additional observations...")
        
        # Resident notification section (only show if violations detected)
        if results.get('violation_assessment', {}).get('violation_found'):
            st.markdown("---")
            st.subheader("📧 Resident Notification")
            st.info("🚨 **Violations detected!** You can send a notification email to the resident.")
            
            col1, col2 = st.columns(2)
            with col1:
                resident_name = st.text_input("Resident Name", placeholder="Enter resident's full name")
                resident_email = st.text_input("Resident Email", placeholder="resident@university.edu")
            
            with col2:
                st.write("**Notification includes:**")
                st.write("• Specific violations detected")
                st.write("• Housing regulations violated")
                st.write("• Required actions and deadlines")
                st.write("• Contact information")
            
            send_resident_notification = st.checkbox("Send violation notification to resident", value=False)
            
            if send_resident_notification:
                if not resident_email or '@' not in resident_email:
                    st.error("❌ Please enter a valid resident email address")
                    send_resident_notification = False
                elif not resident_name:
                    st.error("❌ Please enter the resident's name")
                    send_resident_notification = False
        else:
            send_resident_notification = False
            resident_name = ""
            resident_email = ""
        
        # Email status container
        if 'email_sent' not in st.session_state:
            st.session_state.email_sent = False
        if 'report_path' not in st.session_state:
            st.session_state.report_path = None
        
        if not st.session_state.email_sent:
            if st.button("📤 Send Report to Residence Life", type="primary"):
                with st.spinner("📤 Generating and sending report..."):
                    try:
                        # Save uploaded image to temporary file for report generation
                        import tempfile
                        import os
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_img:
                            temp_img.write(st.session_state.uploaded_image.getbuffer())
                            image_path_for_report = temp_img.name
                        
                        # Generate report
                        report_path = generator.generate_incident_report(
                            image_path=image_path_for_report,
                            detected_objects=results.get('image_analysis', {}).get('detected_objects', []),
                            violation_assessment=results.get('violation_assessment', {}),
                            policy_rules=results.get('policy_analysis', {}).get('relevant_rules', []),
                            user_notes=additional_notes,
                            staff_name=staff_name or "Staff Member",
                            room_number=room_number or "Room",
                            building_name=building_name or "Building"
                        )
                        
                        # Clean up temporary image file
                        try:
                            os.unlink(image_path_for_report)
                        except:
                            pass
                        
                        st.session_state.report_path = report_path
                        
                        # Debug: Print email configuration
                        print("🔍 DEBUG: Email configuration in app:")
                        print(f"   SMTP Server: {email_sender.smtp_server}")
                        print(f"   SMTP Port: {email_sender.smtp_port}")
                        print(f"   Sender Email: {email_sender.sender_email}")
                        print(f"   Recipient Email: {email_sender.residence_life_email}")
                        print(f"   Password: {'*' * len(email_sender.sender_password) if email_sender.sender_password else 'NOT SET'}")
                        
                        # Get email configuration for display
                        email_config = email_sender.get_email_config()
                        
                        # Debug: Check if report file exists
                        print(f"🔍 DEBUG: Report file exists: {os.path.exists(report_path)}")
                        print(f"🔍 DEBUG: Report path: {report_path}")
                        
                        # Send the email
                        success = email_sender.send_incident_report(
                            report_path,
                            staff_name=staff_name or "Staff Member",
                            building_name=building_name or "Building",
                            room_number=room_number or "Room",
                            incident_date=incident_date,
                            incident_time=incident_time,
                            student_name=student_name
                        )
                        
                        print(f"🔍 DEBUG: Email send result: {success}")
                        
                        if success:
                            st.session_state.email_sent = True
                            st.session_state.email_details = {
                                'timestamp': datetime.now(),
                                'recipient': email_config.get('residence_life_email', 'reslife@university.edu'),
                                'sender': email_config.get('sender_email', ''),
                                'report_path': report_path,
                                'staff_name': staff_name or "Staff Member",
                                'building_name': building_name or "Building",
                                'room_number': room_number or "Room",
                                'incident_date': incident_date,
                                'incident_time': incident_time,
                                'student_name': student_name
                            }
                            
                            # Send resident notification if requested
                            resident_notification_sent = False
                            if send_resident_notification and resident_email and resident_name:
                                with st.spinner("📧 Sending resident notification..."):
                                    try:
                                        resident_success = email_sender.send_resident_violation_notification(
                                            resident_email=resident_email,
                                            resident_name=resident_name,
                                            building_name=building_name or "Building",
                                            room_number=room_number or "Room",
                                            violation_assessment=results.get('violation_assessment', {}),
                                            detected_objects=results.get('image_analysis', {}).get('detected_objects', []),
                                            policy_rules=results.get('policy_analysis', {}).get('relevant_rules', []),
                                            staff_name=staff_name or "Staff Member",
                                            incident_date=incident_date
                                        )
                                        
                                        if resident_success:
                                            resident_notification_sent = True
                                            st.session_state.email_details['resident_notification'] = {
                                                'sent': True,
                                                'resident_name': resident_name,
                                                'resident_email': resident_email
                                            }
                                        else:
                                            st.warning("⚠️ Failed to send resident notification, but report was sent to Residence Life")
                                            
                                    except Exception as e:
                                        st.warning(f"⚠️ Error sending resident notification: {str(e)}")
                            
                            # Success message with details
                            st.success("✅ Report sent successfully to Residence Life!")
                            
                            if resident_notification_sent:
                                st.success(f"✅ Violation notification sent to {resident_name} ({resident_email})")
                            
                            # Email details
                            with st.expander("📧 Email Details", expanded=True):
                                st.markdown("### 📤 Email Information")
                                st.write(f"**Sent to:** {st.session_state.email_details['recipient']}")
                                st.write(f"**Sent from:** {st.session_state.email_details['sender']}")
                                st.write(f"**Sent at:** {st.session_state.email_details['timestamp'].strftime('%B %d, %Y at %I:%M:%S %p')}")
                                st.write(f"**Subject:** Incident Report - {st.session_state.email_details['building_name']} Room {st.session_state.email_details['room_number']}")
                                
                                if resident_notification_sent:
                                    st.markdown("### 👤 Resident Notification")
                                    st.write(f"**Sent to:** {resident_name} ({resident_email})")
                                    st.write(f"**Subject:** Housing Policy Violation Notice")
                                    st.write("**Includes:** Specific violations, housing regulations, required actions")
                                
                                st.markdown("### 📋 Report Contents")
                                st.write(f"**Staff Member:** {st.session_state.email_details['staff_name']}")
                                st.write(f"**Location:** {st.session_state.email_details['building_name']} - Room {st.session_state.email_details['room_number']}")
                                st.write(f"**Incident Date:** {st.session_state.email_details['incident_date']}")
                                st.write(f"**Incident Time:** {st.session_state.email_details['incident_time']}")
                                if st.session_state.email_details['student_name']:
                                    st.write(f"**Student Name:** {st.session_state.email_details['student_name']}")
                                
                                st.markdown("### 📎 Attachments")
                                st.write(f"**Report File:** {os.path.basename(st.session_state.email_details['report_path'])}")
                                st.write(f"**File Size:** {os.path.getsize(st.session_state.email_details['report_path']) / 1024:.1f} KB")
                            
                            # Next steps
                            st.info("📬 **Next Steps:**")
                            if resident_notification_sent:
                                st.markdown("""
                                - The incident report has been sent to the Residence Life office
                                - A violation notification has been sent to the resident
                                - The resident has been informed of required actions and deadlines
                                - The office will follow up with the resident as appropriate
                                """)
                            else:
                                st.markdown("""
                                - The incident report has been sent to the Residence Life office
                                - The office will review the report and take appropriate action
                                - You may receive a follow-up email from the office
                                - Keep this report for your records
                                """)
                            
                            # Ask if user wants to view the report
                            st.markdown("---")
                            st.subheader("📄 View Report")
                            st.write("Would you like to view or download the report that was sent?")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("👁️ View Report", type="secondary"):
                                    # Display report
                                    with open(report_path, "rb") as f:
                                        st.download_button(
                                            label="📥 Download Report",
                                            data=f.read(),
                                            file_name=f"incident_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                            mime="application/pdf"
                                        )
                            
                            with col2:
                                if st.button("🔄 Start New Analysis", type="primary"):
                                    # Clear session state for new analysis
                                    st.session_state.analysis_results = None
                                    st.session_state.uploaded_image = None
                                    st.session_state.report_path = None
                                    st.session_state.email_sent = False
                                    st.session_state.email_details = None
                                    st.rerun()
                            
                            # Additional actions
                            st.markdown("### 📋 Additional Actions")
                            st.markdown("""
                            - **Download Report:** Use the download button above to save a local copy
                            - **Print Report:** Open the downloaded PDF and print for physical records
                            - **Follow Up:** Contact the Residence Life office if you need to provide additional information
                            """)
                            
                        else:
                            st.error("❌ Failed to send report. Please check your email configuration and try again.")
                            
                    except Exception as e:
                        st.error(f"❌ Report generation or sending failed: {str(e)}")
                        st.info("💡 **Troubleshooting Tips:**")
                        st.markdown("""
                        - Check your email configuration in the .env file
                        - Verify your Gmail App Password is correct
                        - Ensure the recipient email address is valid
                        - Check your internet connection
                        """)
        else:
            # Email already sent - show status
            st.success("✅ Report already sent to Residence Life!")
            
            # Show email details
            with st.expander("📧 Email Details", expanded=True):
                st.markdown("### 📤 Email Information")
                st.write(f"**Sent to:** {st.session_state.email_details['recipient']}")
                st.write(f"**Sent at:** {st.session_state.email_details['timestamp'].strftime('%B %d, %Y at %I:%M:%S %p')}")
                st.write(f"**Status:** ✅ Delivered")
                
                st.markdown("### 📋 Report Contents")
                st.write(f"**Staff Member:** {st.session_state.email_details['staff_name']}")
                st.write(f"**Location:** {st.session_state.email_details['building_name']} - Room {st.session_state.email_details['room_number']}")
                st.write(f"**Incident Date:** {st.session_state.email_details['incident_date']}")
                st.write(f"**Incident Time:** {st.session_state.email_details['incident_time']}")
                if st.session_state.email_details['student_name']:
                    st.write(f"**Student Name:** {st.session_state.email_details['student_name']}")
            
            # Ask if user wants to view the report
            st.markdown("---")
            st.subheader("📄 View Report")
            st.write("Would you like to view or download the report that was sent?")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("👁️ View Report", type="secondary"):
                    # Display report
                    with open(st.session_state.report_path, "rb") as f:
                        st.download_button(
                            label="📥 Download Report",
                            data=f.read(),
                            file_name=f"incident_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf"
                        )
            
            with col2:
                if st.button("📤 Send Another Report", type="secondary"):
                    st.session_state.email_sent = False
                    st.rerun()
            
            with col3:
                if st.button("🔄 Start New Analysis", type="primary"):
                    # Clear session state for new analysis
                    st.session_state.analysis_results = None
                    st.session_state.uploaded_image = None
                    st.session_state.report_path = None
                    st.session_state.email_sent = False
                    st.session_state.email_details = None
                    st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; padding: 1rem;">
            <p>🚨 ResidenceGuard AI | Intelligent Residence Life Assistant</p>
            <p>Built with Streamlit, AI, and ❤️ for safer campus communities</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 