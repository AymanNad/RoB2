import streamlit as st
import enum

# Define the Response and RiskOfBias Enums
class Response(enum.Enum):
    YES = "Yes"
    PROBABLY_YES = "Probably yes"
    PROBABLY_NO = "Probably no"
    NO = "No"
    NO_INFORMATION = "No information"
    NOT_APPLICABLE = "Not applicable"

class RiskOfBias(enum.Enum):
    LOW = "Low"
    HIGH = "High"
    SOME_CONCERNS = "Some concerns"

# Define assessment functions
def assess_randomization_process(q1_1, q1_2, q1_3):
    if (q1_1 in [Response.NO, Response.PROBABLY_NO]) or (q1_2 in [Response.NO, Response.PROBABLY_NO]) or (q1_3 in [Response.YES, Response.PROBABLY_YES]):
        return RiskOfBias.HIGH
    elif (q1_1 == Response.YES and q1_2 == Response.YES and q1_3 == Response.NO) or \
         (q1_1 == Response.PROBABLY_YES and q1_2 == Response.PROBABLY_YES and q1_3 == Response.PROBABLY_NO):
        return RiskOfBias.LOW
    else:
        return RiskOfBias.SOME_CONCERNS

def assess_deviations_from_intended_interventions(effect_of_interest, q2_1, q2_2, q2_3, q2_4, q2_5, q2_6, q2_7):
    if effect_of_interest == "assignment to intervention":
        if ((q2_3 in [Response.YES, Response.PROBABLY_YES] and q2_4 in [Response.YES, Response.PROBABLY_YES] and q2_5 in [Response.NO, Response.PROBABLY_NO]) or
            (q2_6 in [Response.NO, Response.PROBABLY_NO] and q2_7 in [Response.YES, Response.PROBABLY_YES])):
            return RiskOfBias.HIGH
        elif ((q2_1 == Response.NO and q2_2 == Response.NO) or
              (q2_3 in [Response.NO, Response.PROBABLY_NO]) or
              (q2_6 == Response.YES)):
            return RiskOfBias.LOW
        else:
            return RiskOfBias.SOME_CONCERNS
    elif effect_of_interest == "adhering to intervention":
        if ((q2_3 in [Response.NO, Response.PROBABLY_NO] or q2_4 in [Response.YES, Response.PROBABLY_YES] or q2_5 in [Response.YES, Response.PROBABLY_YES]) and
            q2_6 in [Response.NO, Response.PROBABLY_NO]):
            return RiskOfBias.HIGH
        elif ((q2_1 == Response.NO and q2_2 == Response.NO and q2_3 == Response.YES and q2_4 == Response.NO and q2_5 == Response.NO) or
              q2_6 == Response.YES):
            return RiskOfBias.LOW
        else:
            return RiskOfBias.SOME_CONCERNS

def assess_missing_outcome_data(q3_1, q3_2, q3_3, q3_4):
    if q3_1 in [Response.NO, Response.PROBABLY_NO, Response.NO_INFORMATION]:
        if q3_2 in [Response.NO, Response.PROBABLY_NO]:
            if q3_3 in [Response.YES, Response.PROBABLY_YES, Response.NO_INFORMATION]:
                if q3_4 in [Response.YES, Response.PROBABLY_YES]:
                    return RiskOfBias.HIGH
                else:
                    return RiskOfBias.SOME_CONCERNS
            else:
                return RiskOfBias.LOW
        else:
            return RiskOfBias.LOW
    else:
        return RiskOfBias.LOW

def assess_measurement_of_outcome(q4_1, q4_2, q4_3, q4_4, q4_5):
    if q4_1 in [Response.NO, Response.PROBABLY_NO] and q4_2 in [Response.NO, Response.PROBABLY_NO]:
        if q4_3 in [Response.YES, Response.PROBABLY_YES, Response.NO_INFORMATION]:
            if q4_4 in [Response.YES, Response.PROBABLY_YES, Response.NO_INFORMATION]:
                if q4_5 in [Response.YES, Response.PROBABLY_YES]:
                    return RiskOfBias.HIGH
                else:
                    return RiskOfBias.SOME_CONCERNS
            else:
                return RiskOfBias.LOW
        else:
            return RiskOfBias.LOW
    else:
        return RiskOfBias.HIGH

def assess_selection_of_reported_result(q5_1, q5_2, q5_3):
    if (q5_2 in [Response.YES, Response.PROBABLY_YES]) or (q5_3 in [Response.YES, Response.PROBABLY_YES]):
        return RiskOfBias.HIGH
    elif q5_1 == Response.YES and q5_2 == Response.NO and q5_3 == Response.NO:
        return RiskOfBias.LOW
    else:
        return RiskOfBias.SOME_CONCERNS

def assess_overall_bias(domain_judgments):
    if RiskOfBias.HIGH in domain_judgments:
        return RiskOfBias.HIGH
    elif RiskOfBias.SOME_CONCERNS in domain_judgments:
        return RiskOfBias.SOME_CONCERNS
    else:
        return RiskOfBias.LOW

def main():
    st.set_page_config(page_title="RoB2 Assessment Tool", layout="wide")
    st.sidebar.title("Navigation")
    st.sidebar.markdown("### RoB 2")
    st.sidebar.markdown("Other tools can be added here")

    st.title("Risk of Bias 2 (RoB 2) Assessment Tool")

    # Custom CSS to align options in a single line and handle colors
    st.markdown("""
        <style>
        .stRadio > div {
            flex-direction: row;
            flex-wrap: wrap;
        }
        .stRadio label {
            padding-right: 10px;
        }
        .green {color: green;}
        .red {color: red;}
        </style>
    """, unsafe_allow_html=True)

    def colored_radio(label, options, key):
        options_html = "".join([f'<label class="{option_color(option)}"><input type="radio" name="{key}" value="{option.value}" /> {option.value}</label>' for option in options])
        st.markdown(f'<div class="stRadio"><div>{options_html}</div></div>', unsafe_allow_html=True)

    def option_color(option):
        if option in [Response.YES, Response.PROBABLY_YES]:
            return "green"
        elif option in [Response.NO, Response.PROBABLY_NO]:
            return "red"
        return ""

    # Domain 1: Randomization process
    st.header("Domain 1: Risk of bias arising from the randomization process")
    q1_1 = st.radio("1.1 Was the allocation sequence random?", options=list(Response), format_func=lambda x: x.value, key="q1_1")
    q1_2 = st.radio("1.2 Was the allocation sequence concealed until participants were enrolled and assigned to interventions?", options=list(Response), format_func=lambda x: x.value, key="q1_2")
    q1_3 = st.radio("1.3 Did baseline differences between intervention groups suggest a problem with the randomization process?", options=list(Response), format_func=lambda x: x.value, key="q1_3")
    
    d1_judgment = assess_randomization_process(q1_1, q1_2, q1_3)
    st.markdown(f"**Domain 1 Judgment: {d1_judgment.value}**")

    # Domain 2: Deviations from intended interventions
    st.header("Domain 2: Risk of bias due to deviations from the intended interventions")
    effect_of_interest = st.radio("Select the effect of interest:", ("assignment to intervention", "adhering to intervention"))

    q2_1 = st.radio("2.1 Were participants aware of their assigned intervention during the trial?", options=list(Response), format_func=lambda x: x.value, key="q2_1")
    q2_2 = st.radio("2.2 Were carers and people delivering the interventions aware of participants' assigned intervention during the trial?", options=list(Response), format_func=lambda x: x.value, key="q2_2")

    if effect_of_interest == "assignment to intervention":
        q2_3 = st.radio("2.3 Were there deviations from the intended intervention that arose because of the trial context?", options=list(Response), format_func=lambda x: x.value, key="q2_3")
        q2_4 = st.radio("2.4 Were these deviations likely to have affected the outcome?", options=list(Response), format_func=lambda x: x.value, key="q2_4")
        q2_5 = st.radio("2.5 Were these deviations from intended intervention balanced between groups?", options=list(Response), format_func=lambda x: x.value, key="q2_5")
        q2_6 = st.radio("2.6 Was an appropriate analysis used to estimate the effect of assignment to intervention?", options=list(Response), format_func=lambda x: x.value, key="q2_6")
        q2_7 = st.radio("2.7 Was there potential for a substantial impact (on the result) of the failure to analyse participants in the group to which they were randomized?", options=list(Response), format_func=lambda x: x.value, key="q2_7")
    else:
        q2_3 = st.radio("2.3 [If applicable:] Were important non-protocol interventions balanced across intervention groups?", options=list(Response), format_func=lambda x: x.value, key="q2_3")
        q2_4 = st.radio("2.4 [If applicable:] Were there failures in implementing the intervention that could have affected the outcome?", options=list(Response), format_func=lambda x: x.value, key="q2_4")
        q2_5 = st.radio("2.5 [If applicable:] Was there non-adherence to the assigned intervention regimen that could have affected participants' outcomes?", options=list(Response), format_func=lambda x: x.value, key="q2_5")
        q2_6 = st.radio("2.6 If N/PN/NI to 2.3, or Y/PY/NI to 2.4 or 2.5: Was an appropriate analysis used to estimate the effect of adhering to the intervention?", options=list(Response), format_func=lambda x: x.value, key="q2_6")
        q2_7 = Response.NOT_APPLICABLE

    d2_judgment = assess_deviations_from_intended_interventions(effect_of_interest, q2_1, q2_2, q2_3, q2_4, q2_5, q2_6, q2_7)
    st.markdown(f"**Domain 2 Judgment: {d2_judgment.value}**")

    # Domain 3: Missing outcome data
    st.header("Domain 3: Risk of bias due to missing outcome data")
    q3_1 = st.radio("3.1 Were data for this outcome available for all, or nearly all, participants randomized?", options=list(Response), format_func=lambda x: x.value, key="q3_1")
    q3_2 = st.radio("3.2 Is there evidence that the result was not biased by missing outcome data?", options=list(Response), format_func=lambda x: x.value, key="q3_2")
    q3_3 = st.radio("3.3 Could missingness in the outcome depend on its true value?", options=list(Response), format_func=lambda x: x.value, key="q3_3")
    q3_4 = st.radio("3.4 Is it likely that missingness in the outcome depended on its true value?", options=list(Response), format_func=lambda x: x.value, key="q3_4")

    d3_judgment = assess_missing_outcome_data(q3_1, q3_2, q3_3, q3_4)
    st.markdown(f"**Domain 3 Judgment: {d3_judgment.value}**")

    # Domain 4: Measurement of the outcome
    st.header("Domain 4: Risk of bias in measurement of the outcome")
    q4_1 = st.radio("4.1 Was the method of measuring the outcome inappropriate?", options=list(Response), format_func=lambda x: x.value, key="q4_1")
    q4_2 = st.radio("4.2 Could measurement or ascertainment of the outcome have differed between intervention groups?", options=list(Response), format_func=lambda x: x.value, key="q4_2")
    q4_3 = st.radio("4.3 Were outcome assessors aware of the intervention received by study participants?", options=list(Response), format_func=lambda x: x.value, key="q4_3")
    q4_4 = st.radio("4.4 Could assessment of the outcome have been influenced by knowledge of intervention received?", options=list(Response), format_func=lambda x: x.value, key="q4_4")
    q4_5 = st.radio("4.5 Is it likely that assessment of the outcome was influenced by knowledge of intervention received?", options=list(Response), format_func=lambda x: x.value, key="q4_5")

    d4_judgment = assess_measurement_of_outcome(q4_1, q4_2, q4_3, q4_4, q4_5)
    st.markdown(f"**Domain 4 Judgment: {d4_judgment.value}**")

    # Domain 5: Selection of the reported result
    st.header("Domain 5: Risk of bias in selection of the reported result")
    q5_1 = st.radio("5.1 Were the data that produced this result analysed in accordance with a pre-specified analysis plan that was finalized before unblinded outcome data were available for analysis?", options=list(Response), format_func=lambda x: x.value, key="q5_1")
    q5_2 = st.radio("5.2 Is the numerical result being assessed likely to have been selected, on the basis of the results, from multiple eligible outcome measurements within the outcome domain?", options=list(Response), format_func=lambda x: x.value, key="q5_2")
    q5_3 = st.radio("5.3 Is the numerical result being assessed likely to have been selected, on the basis of the results, from multiple eligible analyses of the data?", options=list(Response), format_func=lambda x: x.value, key="q5_3")

    d5_judgment = assess_selection_of_reported_result(q5_1, q5_2, q5_3)
    st.markdown(f"**Domain 5 Judgment: {d5_judgment.value}**")

    if st.button("Calculate Overall Risk of Bias"):
        # Calculate overall judgment
        overall_judgment = assess_overall_bias([d1_judgment, d2_judgment, d3_judgment, d4_judgment, d5_judgment])

        # Display results in a table
        st.header("Risk of Bias Assessment Results")
        st.table({
            "Domain": ["Randomization process", "Deviations from intended interventions", "Missing outcome data", "Measurement of the outcome", "Selection of the reported result"],
            "Judgment": [d1_judgment.value, d2_judgment.value, d3_judgment.value, d4_judgment.value, d5_judgment.value]
        })
        st.write(f"**Overall risk of bias: {overall_judgment.value}**")

if __name__ == "__main__":
    main()
