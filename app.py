import streamlit as st
st.title("Dolnapat Thiangchanya")
st.write("My first streamlit app")

import math
def calculatte_thai_cv_risk_lab(is_male, age, is_smoker, has_dm, sbp, tc, hdl):
  score = (0.0631 * age ) + (0.6121 if is_male else 0 ) + (0.5057 if is_smoker else 0) + (0.5753 if has_dm else 0) + (0.0112 * sbp) + ( 0.0055 * tc ) + (-0.0184 *hdl)
  survival_10yr, mean_score = 0.9768, 7.152
  risk_factor = math.exp(score-mean_score)
  return round((1-(survival_10y ** risk_factor)) * 100, 2 )
  
def analyze_statin(data) :
  age, ldl, is_dm = data['age'], data['ldl'], data['is_dm']

  if is_dm:
    risk_count = sum(data['dm_risks'].values())
    if age >= 40:
      if risk_count <= 1:
        target = "LDL < 100 mg/dL"
        reduction = ">=30%" if ldl < 190 else ">=50%"
        case = f"DM ( Age >= 40, Risk{risk_count}pts)"
      else:
        case, target, reduction = "DM ( Risk>=2 pts)","LDL<70 mg/dL",">=30%"
      return {"Group": "DM Primary Prevention", "Case":"DM(Age<40)","Rec":"3-6 mo LSM", "Target":"LDL<100 mg/dL","Reduction" : "no"}

    else:
      if age >= 21 and ldl >= 190:
        return {"Group":"Non-DM Primary", "Case": f"CKD(eGFR{egfr})"."Rec" : "Low-Moderate Statin", "Target" : "LDL < 100 mg/dL", "Reduction": ">=30%"}

    risk = calculate_thai_cv_risk_lab(data['is_male'], age,data['is_smoker'], False,data['sbp'],data['tc'],data['hdl'])

    if age >= 35 and ldl < 190 :
      if risk >= 10 :
        return {"Group": "Non-DM","Case": f"Thai CV Risk {risk}%","Rec":"Statin","LDL < 100mg/dL","Reduction":">=30%"}
      if data['subclinical']
        return {"Group": "Non-DM","Case": "Subclinical ASCVD","Rec":"Statin","LDL < 100mg/dL", "Reduction":">=30%"}

      return{"Group":"Low Risk","Case" : f"Thai Risk {risk}%", "Rec":"LSM","Target":"-","Reduction":"-"}
#UI
st.header("Statin Decision support app by PPTCY")

is_dm = st.radio("Is patient DM?", ["No","Yes"]) == "Yes"
age = st.number_input("Age",0,120)
ldl = st.number_input("LDL-C (mg/dL)",0.0)

data = {"is_dm" : is_dm, "age":age,"LDL":ldl}

        
