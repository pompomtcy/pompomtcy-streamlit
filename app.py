import streamlit as st
st.title("Dolnapat Thiangchanya")
st.write("My first streamlit app 🙂")

import math
import streamlit as st

# ===== CV RISK =====
def calculate_thai_cv_risk_lab(is_male, age, is_smoker, has_dm, sbp, tc, hdl):
    score = (
        (0.0631 * age)
        + (0.6121 if is_male else 0)
        + (0.5057 if is_smoker else 0)
        + (0.5753 if has_dm else 0)
        + (0.0112 * sbp)
        + (0.0055 * tc)
        + (-0.0184 * hdl)
    )
    survival_10yr, mean_score = 0.9768, 7.152
    risk_factor = math.exp(score - mean_score)
    return round((1 - (survival_10yr ** risk_factor)) * 100, 2)


# ===== ANALYSIS =====
def analyze_statin(data):
    age = data.get('age')
    ldl = data.get('ldl')
    is_dm = data.get('is_dm')

    # ===== DM =====
    if is_dm:
        risk_count = sum(data.get('dm_risks', {}).values())

        if age >= 40:
            if risk_count <= 1:
                case = f"DM (Age ≥40, Risk {risk_count})"
                target = "LDL < 100 mg/dL"
                reduction = ">=30%" if ldl < 190 else ">=50%"
            else:
                case = "DM (Risk ≥2)"
                target = "LDL < 70 mg/dL"
                reduction = ">=50%"

            return {
                "Group": "DM, Primary Prevention",
                "Case": case,
                "Rec": "Start Statin",
                "Target": target,
                "Reduction": reduction
            }

        else:
            return {
                "Group": "DM, Primary Prevention",
                "Case": "DM (Age <40)",
                "Rec": "Lifestyle modification",
                "Target": "LDL < 100 mg/dL",
                "Reduction": "-"
            }

    # ===== Non-DM =====
    egfr = data.get('egfr')

    if age >= 21 and ldl >= 190:
        return {
            "Group": "High risk, Primary prevention",
            "Case": f"LDL ≥190",
            "Rec": "High-intensity statin",
            "Target": "LDL < 100 mg/dL",
            "Reduction": ">=50%"
        }

    # calculate risk
    risk = calculate_thai_cv_risk_lab(
        data.get('is_male'),
        age,
        data.get('is_smoker'),
        False,
        data.get('sbp'),
        data.get('tc'),
        data.get('hdl')
    )

    if age >= 35 and ldl < 190:
        if risk >= 10:
            return {
                "Group": "Non-DM High Risk, Primary prevention",
                "Case": f"Thai CV Risk {risk}%",
                "Rec": "Statin",
                "Target": "LDL < 100 mg/dL",
                "Reduction": ">=30%"
            }

        if data.get('subclinical'):
            return {
                "Group": "Non-DM",
                "Case": "Subclinical ASCVD",
                "Rec": "Statin",
                "Target": "LDL < 100 mg/dL",
                "Reduction": ">=30%"
            }

        return {
            "Group": "Low Risk",
            "Case": f"Thai CV Risk {risk}%",
            "Rec": "Lifestyle modification",
            "Target": "-",
            "Reduction": "-"
        }

    # fallback กัน error
    return {
        "Group": "Unknown",
        "Case": "Insufficient data",
        "Rec": "-",
        "Target": "-",
        "Reduction": "-"
    }


# ===== UI =====
st.header("Statin Decision support App ")
st.subheader("By PPtcy")
errors = []

is_dm = st.radio("Is patient DM?", ["No","Yes"]) == "Yes"

age = st.number_input("Age", 0, 120, value=None, placeholder="Enter age")
ldl = st.number_input("LDL-C (mg/dL)", min_value=0.0, value=None, placeholder="Enter LDL")

data = {"is_dm": is_dm, "age": age, "ldl": ldl}

# ===== VALIDATE BASIC =====
if age is None:
    errors.append("Age is required")
if ldl is None:
    errors.append("LDL is required")

# ===== DM =====
if is_dm:
    st.subheader("DM Risk Factors")
    risks = ["Long duration DM","Obesity","Smoking","HT","Family History","CKD","Albuminuria"]
    data['dm_risks'] = {r: st.checkbox(r) for r in risks}

# ===== NON-DM =====
else:
    st.subheader("Non-DM Assessment")

    gender = st.radio("Gender", ["Female", "Male"], index=None)
    data['is_male'] = (gender == "Male")

    if gender is None:
        errors.append("Gender is required")

    data['is_smoker'] = st.checkbox("Smoking")

    data['sbp'] = st.number_input("SBP (mmHg)", value=None, placeholder="e.g. 120")
    data['tc'] = st.number_input("Total cholesterol", value=None)
    data['hdl'] = st.number_input("HDL", value=None)
    data['egfr'] = st.number_input("eGFR", value=None)
    data['subclinical'] = st.checkbox("Subclinical ASCVD")

    if data['sbp'] is None:
        errors.append("SBP is required")
    if data['tc'] is None:
        errors.append("Total cholesterol is required")
    if data['hdl'] is None:
        errors.append("HDL is required")

# ===== SHOW ERRORS =====
if errors:
    st.error("⚠️ Please fill required fields:")
    for e in errors:
        st.write(f"- {e}")

# ===== BUTTON =====
if st.button("Check", disabled=len(errors) > 0):
    result = analyze_statin(data)

    st.success("Result")
    st.write("#DLP with", result['Group'])
    st.write("->", result['Case'])
    st.write("Recommendation:", result['Rec'])
    st.write("Target :", result['Target'])
    st.write("Reduction goal:", result['Reduction'])
