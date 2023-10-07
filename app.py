import streamlit as st 
import tiktoken 

GPT_35_TURBO_PROMPT_COST = 0.0015/1000 
GPT_35_TURBO_COMPLETION_COST = 0.002/1000
GPT_4_PROMPT_COST = 0.03/1000
GPT_4_COMPLETION_COST = 0.06/1000

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    print(num_tokens)
    return num_tokens

def main():
    st.set_page_config(layout="wide")
    st.title(":robot_face: LLM Cost Calculations")
    
    prompt_text = st.text_area("Prompt Text", height=300)

    if len(prompt_text) > 0:

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.subheader("Basic Information")
            st.info("Your Input Prompt: " + prompt_text)
            token_counts = num_tokens_from_string(prompt_text, "cl100k_base")
            st.success("Token Count: " + str(token_counts))
        
        with col2:
            st.subheader("Execute a Simulation")
            option = st.selectbox('Select an LLM:', ('GPT-3.5-Turbo', 'GPT-4'))
            average_number_of_employees = st.slider("Average number of Employees", 0, 200, 0)
            average_prompt_frequency = st.slider("Average number of Prompts (Per Day)/Employee", 0, 300, 0)
            average_prompt_tokens = st.slider("Average Prompt Tokens Length", 0, 300, 0)
            average_completion_tokens = st.slider("Average Completion Tokens Length", 0, 1000, 0)

        with col3:
            st.subheader("Cost Analysis (Weekdays)") # Assume weekdays only
            if option in ['GPT-3.5-Turbo', 'GPT-4']:
                if option == 'GPT-3.5-Turbo':
                    prompt_cost = GPT_35_TURBO_PROMPT_COST
                    completion_cost = GPT_35_TURBO_COMPLETION_COST
                else:
                    prompt_cost = GPT_4_PROMPT_COST
                    completion_cost = GPT_4_COMPLETION_COST
                # Calculate average number of prompts per day
                average_prompts_per_day =  average_number_of_employees * average_prompt_frequency
                cost_per_day = average_prompts_per_day * average_prompt_tokens * prompt_cost + \
                    average_prompts_per_day * average_completion_tokens * completion_cost
                cost_per_month = cost_per_day * 365 * 5/7 / 12
                cost_per_year = cost_per_day * 365 * 5/7
                st.success("Cost Per Day: " + str(round(cost_per_day, 2)) + " $")
                st.success("Cost Per Month: " + str(round(cost_per_month, 2)) + " $")
                st.success("Cost Per Year: " + str(round(cost_per_year, 2)) + " $")
                st.write("Please Note: This calculation is based on several assumptions. "
                         "This app takes no responsibility for the accuracy of the calculation. "
                         "Please use this app at your own risk.")
            else:
                st.error("Please select a valid LLM")


if __name__ == "__main__":
    main()
