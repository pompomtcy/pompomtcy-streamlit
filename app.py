import streamlit as st
st.title("Dolnapat Thiangchanya")
st.write("My first streamlit app")

import math
def calculatte_thai_cv_risk_lab(is_male, age, is_smoker, has_dm, sbp, tc, hdl):
  score = (0.0631 * age ) + (0.6121 if is_male else 0 ) + (0.5057 if is_smoker else 0) + (0.5753 if has_dm else 0) + (0.0112 * sbp) + ( 0.0055 * tc ) + (-0.0184 *hdl)
  survival_10yr, mean_score = 0.9768, 7.152
  risk_factor = math.exp(score-mean_score)
  return round((1-(survival_10y ** risk_factor)) * 100, 2 )
  
