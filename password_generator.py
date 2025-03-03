import re
import random
import string
import streamlit as st

def check_password_strength(password):
    """
    Analyzes password strength based on various security criteria
    Returns a score from 0-5 and appropriate feedback
    """
    score = 0
    feedback = []
    checks = {}
    
    # Length Check
    if len(password) >= 12:
        score += 1
        checks["length"] = True
    elif len(password) >= 8:
        score += 0.5
        checks["length"] = "Partial"
        feedback.append("❌ Password should ideally be at least 12 characters long for better security.")
    else:
        checks["length"] = False
        feedback.append("❌ Password must be at least 8 characters long.")
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
        checks["case"] = True
    else:
        checks["case"] = False
        feedback.append("❌ Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
        checks["digit"] = True
    else:
        checks["digit"] = False
        feedback.append("❌ Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
        checks["special"] = True
    else:
        checks["special"] = False
        feedback.append("❌ Include at least one special character (!@#$%^&*).")
    
    # Extra Check: Avoiding Common Patterns
    checks["no_patterns"] = True
    
    # Check for sequential characters
    if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|012|123|234|345|456|567|678|789|890)', password.lower()):
        feedback.append("❌ Avoid sequential characters like 'abc', '123', etc.")
        score -= 0.5
        checks["no_patterns"] = False
    
    # Check for repeated characters
    if re.search(r'(.)\1{2,}', password):
        feedback.append("❌ Avoid repeating the same character more than twice.")
        score -= 0.5
        checks["no_patterns"] = False
    
    # Check for common passwords
    common_passwords = ["password", "123456", "qwerty", "admin", "welcome", "password123"]
    if password.lower() in common_passwords:
        feedback.append("❌ This is a commonly used password and very insecure.")
        score = 0
        checks["not_common"] = False
    else:
        checks["not_common"] = True
    
    # Ensure score doesn't go negative
    score = max(0, score)
    
    # Normalize score to 0-100 for better visualization
    normalized_score = min(int(score * 25), 100)  # Max score is 4, so multiply by 25 to get to 100
    
    # Strength Rating
    if score >= 4:
        strength = "Strong"
        message = "✅ Strong Password! Your password meets all security criteria."
        color = "green"
    elif score >= 3:
        strength = "Moderate"
        message = "⚠️ Moderate Password - Consider improving using the suggestions below."
        color = "orange"
    else:
        strength = "Weak"
        message = "❌ Weak Password - Please improve it using the suggestions below."
        color = "red"
    
    return normalized_score, strength, message, feedback, checks, color

def generate_strong_password(length=12):
    """
    Generates a strong random password
    """
    if length < 8:
        length = 12  # Minimum recommended length
    
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = "!@#$%^&*"
    
    # Ensure at least one of each type
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special_chars)
    ]
    
    # Fill the rest randomly
    remaining_length = length - 4
    all_chars = lowercase + uppercase + digits + special_chars
    password.extend(random.choice(all_chars) for _ in range(remaining_length))
    
    # Shuffle the password characters
    random.shuffle(password)
    
    # Convert list to string
    return ''.join(password)

def main():
    st.set_page_config(
        page_title="Password Strength Meter",
        page_icon="🔒",
        layout="centered"
    )
    
    # App header
    st.title("🔒 Password Strength Meter")
    st.markdown("""
    This app helps you evaluate your password strength and generate secure passwords.
    """)
    
    # Create tabs
    tab1, tab2 = st.tabs(["Check Password", "Generate Password"])
    
    # Password Check Tab
    with tab1:
        st.subheader("Check Your Password Strength")
        
        # Password input with toggle for visibility
        col1, col2 = st.columns([3, 1])
        with col1:
            password_visible = st.checkbox("Show password", value=False)
        
        if password_visible:
            password = st.text_input("Enter your password:", key="visible_password")
        else:
            password = st.text_input("Enter your password:", type="password", key="hidden_password")
        
        if password:
            score, strength, message, feedback, checks, color = check_password_strength(password)
            
            # Display password strength with progress bar
            st.markdown(f"### Password Strength: **:{color}[{strength}]**")
            st.progress(score)
            st.markdown(f"**Score:** {score}/100")
            
            # Display security criteria status with custom styling
            st.subheader("Security Criteria")
            
            # Create styled checks using emojis and colors
            criteria_status = {
                "length": {"text": "Length (8+ chars, 12+ recommended)", "status": checks.get("length", False)},
                "case": {"text": "Upper & lowercase letters", "status": checks.get("case", False)},
                "digit": {"text": "Contains numbers", "status": checks.get("digit", False)},
                "special": {"text": "Contains special characters", "status": checks.get("special", False)},
                "no_patterns": {"text": "No common patterns", "status": checks.get("no_patterns", False)},
                "not_common": {"text": "Not a common password", "status": checks.get("not_common", True)}
            }
            
            # Display criteria as styled elements
            for key, item in criteria_status.items():
                if item["status"] is True:
                    st.markdown(f"✅ {item['text']}")
                elif item["status"] == "Partial":
                    st.markdown(f"⚠️ {item['text']}")
                else:
                    st.markdown(f"❌ {item['text']}")
            
            # Display feedback if any
            if feedback:
                st.subheader("Improvement Suggestions")
                for suggestion in feedback:
                    st.markdown(suggestion)
                    
            # Add a fun message based on score
            if score >= 90:
                st.balloons()
                st.success("Excellent password! Your digital security is in good hands.")
            elif score <= 30:
                st.error("This password needs significant improvement to be secure!")
    
    # Password Generator Tab
    with tab2:
        st.subheader("Generate a Strong Password")
        
        col1, col2 = st.columns(2)
        with col1:
            length = st.slider("Password Length", min_value=8, max_value=30, value=16, step=1)
        
        with col2:
            include_special = st.checkbox("Include Special Characters", value=True)
        
        if st.button("Generate Password"):
            if include_special:
                generated_password = generate_strong_password(length)
            else:
                # Modified generation without special chars
                lowercase = string.ascii_lowercase
                uppercase = string.ascii_uppercase
                digits = string.digits
                all_chars = lowercase + uppercase + digits
                
                # Ensure at least one of each required type
                password = [
                    random.choice(lowercase),
                    random.choice(uppercase),
                    random.choice(digits)
                ]
                remaining_length = length - 3
                password.extend(random.choice(all_chars) for _ in range(remaining_length))
                random.shuffle(password)
                generated_password = ''.join(password)
            
            score, strength, _, _, _, color = check_password_strength(generated_password)
            
            # Show the generated password in a "copy-friendly" container
            st.markdown("### Your Generated Password:")
            password_container = st.container(border=True)
            with password_container:
                st.markdown(f"<div style='font-family: monospace; font-size: 1.2em; word-break: break-all;'>{generated_password}</div>", unsafe_allow_html=True)
                st.markdown(f"**Strength:** :{color}[{strength}] ({score}/100)")
            
            st.info("Click to select the password, then use Ctrl+C (or Cmd+C) to copy")
    
    # Footer with info on what makes a good password
    with st.expander("Password Security Tips"):
        st.markdown("""
        ### Tips for Creating Secure Passwords
        
        - **Use Long Passwords**: Aim for at least 12 characters
        - **Mix Character Types**: Include uppercase, lowercase, numbers, and symbols
        - **Avoid Personal Information**: Don't use names, birthdates, or common words
        - **Use Different Passwords**: Each account should have a unique password
        - **Consider a Password Manager**: Tools like LastPass, 1Password, or Bitwarden can help
        - **Change Passwords Regularly**: Update important passwords every 3-6 months
        
        Remember, the strongest passwords are random and not based on predictable patterns!
        """)

if __name__ == "__main__":
    main()
