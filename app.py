import streamlit as st
st.title("Dolnapat Thiangchanya")
st.write("My first streamlit app")
import math

def calculate_thai_cv_risk_lab(is_male, age, is_smoker, has_diabetes, sbp, tc, hdl):
    """Calculates 10-year Thai CV Risk (Lab-based EGAT Equation)"""
    score = (0.0631 * age) + (0.6121 if is_male else 0) + (0.5057 if is_smoker else 0) + \
            (0.5753 if has_diabetes else 0) + (0.0112 * sbp) + (0.0055 * tc) + (-0.0184 * hdl)
   
    survival_10yr, mean_score = 0.9678, 7.152
    risk_factor = math.exp(score - mean_score)
    return round((1 - (survival_10yr ** risk_factor)) * 100, 2)

def analyze_statin(data):
    """Core logic for Statin Intensity & Target Classification"""
    age, ldl, is_dm = data['age'], data['ldl'], data['is_dm']
   
    # --- GROUP 1: DM PATIENTS ---
    if is_dm:
        risk_count = sum(data['dm_risks'].values())
        if age >= 40:
            if risk_count <= 1:
                target, reduction = "LDL < 100 mg/dL", ">= 30%" if ldl < 190 else ">= 50%"
                case = f"DM (Age >= 40, Risk {risk_count} pts, LDL {'< 190' if ldl < 190 else '>= 190'})"
            else:
                case, target, reduction = "DM (Age >= 40, Risk >= 2 pts)", "LDL < 70 mg/dL", ">= 30%"
            return {"Group": "DM Primary Prevention", "Case": case, "Rec": "Statin + LSM", "Target": target, "Reduction": reduction}
        else:
            return {"Group": "DM Primary Prevention", "Case": "DM (Age < 40)", "Rec": "3-6 mo LSM", "Target": "LDL < 100 mg/dL", "Reduction": "N/A"}

    # --- GROUP 2: NON-DM PATIENTS ---
    else:
        # Case 1: Extreme LDL
        if age >= 21 and ldl >= 190:
            return {"Group": "Non-DM Primary", "Case": "Case 1: LDL >= 190", "Rec": "Moderate-Intensity Statin", "Target": "LDL < 100 mg/dL", "Reduction": "N/A"}
       
        # New Case: CKD (eGFR <= 60, Age > 50, LDL >= 100)
        egfr = data.get('egfr', 100)
        if age > 50 and egfr <= 60 and ldl >= 100:
            return {"Group": "Non-DM Primary (CKD Group)", "Case": f"CKD Stage 3-5 (eGFR {egfr})", "Rec": "Low-Moderate Intensity Statin", "Target": "LDL < 100 mg/dL", "Reduction": "OR >= 30% reduction"}

        # Risk Calculation for other Non-DM cases
        risk = calculate_thai_cv_risk_lab(data['is_male'], age, data['is_smoker'], False, data['sbp'], data['tc'], data['hdl'])
       
        if age >= 35 and ldl < 190:
            if risk >= 10.0:
                return {"Group": "Non-DM Primary", "Case": f"Case 2: Thai Risk {risk}% (>= 10%)", "Rec": "Low-Mod Intensity", "Target": "LDL < 100 mg/dL", "Reduction": ">= 30%"}
            if data['subclinical']:
                return {"Group": "Non-DM Primary", "Case": f"Case 3: Subclinical AT (Risk {risk}%)", "Rec": "Low-Mod Intensity", "Target": "LDL < 100 mg/dL", "Reduction": ">= 30%"}
       
        return {"Group": "Non-DM", "Case": f"Low Risk (Thai Risk {risk}%)", "Rec": "LSM / Monitoring", "Target": "Standard Care", "Reduction": "N/A"}

# --- Main Interface ---
def main():
    print("--- Integrated Statin Decision Support Tool ---")
   
    is_dm = input("1. Is the patient Diabetic (DM)? (y/n): ").lower() == 'y'
    age = int(input("2. Patient Age (years): "))
    ldl = float(input("3. LDL-C (mg/dL): "))
   
    patient_data = {'is_dm': is_dm, 'age': age, 'ldl': ldl}

    if is_dm:
        print("\n[Risk Factors Checklist (y/n)]")
        risks = ["Long duration DM", "Obesity", "Smoking", "HT", "Fam Hx of premature CVS disease", "CKD", "Albuminuria"]
        patient_data['dm_risks'] = {r: input(f"- {r}: ").lower() == 'y' for r in risks}
    else:
        print("\n[Non-DM Assessment Data]")
        patient_data.update({
            'is_male': input("- Gender (m/f): ").lower() == 'm',
            'is_smoker': input("- Current Smoker? (y/n): ").lower() == 'y',
            'sbp': float(input("- Systolic BP (mmHg): ")),
            'tc': float(input("- Total Cholesterol (mg/dL): ")),
            'hdl': float(input("- HDL-C (mg/dL): ")),
            'egfr': float(input("- eGFR (mL/min/1.73m²): ")),
            'subclinical': input("- Evidence of Subclinical Atherosclerosis? (y/n): ").lower() == 'y'
        })

    result = analyze_statin(patient_data)
   
    print("\n" + "="*70)
    print(f"PATIENT GROUP : {result['Group']}")
    print(f"CLASSIFICATION: {result['Case']}")
    print(f"RECOMMENDATION: {result['Rec']}")
    print(f"TARGET LDL    : {result['Target']}")
    print(f"REDUCTION GOAL: {result['Reduction']}")
    print("="*70)

if __name__ == "__main__":
    main()
