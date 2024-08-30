import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Top Inventors")
st.markdown("~Infringement Team GreyB")
st.markdown("*/There might be some discrepancies due to different name structures used(Somewhere First Middle Last, somewhere First Last)/*")

@st.cache_resource
def count_and_clean_inventors(df, column_name, delimiter='|'):
    df[column_name] = df[column_name].str.replace(',', '')
    df[column_name] = df[column_name].str.replace('.', '', regex=False)

    df[column_name] = df[column_name].str.replace(r'^\s*-\s*$', '', regex=True)

    df['split_inventors'] = df[column_name].str.split(delimiter)
    df_exploded = df.explode('split_inventors')

    df_exploded = df_exploded[df_exploded['split_inventors'].str.len() > 0]
    df_exploded = df_exploded.dropna(subset=['split_inventors'])

    df_exploded['split_inventors'] = df_exploded['split_inventors'].apply(lambda x: ' '.join(x.split()[1:] + [x.split()[0]]) if len(x.split()) > 1 else x)

    inventor_counts = df_exploded['split_inventors'].str.strip().value_counts()

    return inventor_counts

class UI:
    def __init__(self):
        self.initial_data = None
        self.processed_data = None

    def top_inventors(self):
        uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
        
        if uploaded_file:
            self.initial_data = pd.read_excel(uploaded_file)
            if "Inventor Name" in self.initial_data.columns:
                attribute = 'Inventor Name'
            else:
                attribute = st.text_input("Enter the Attribute Name: ")
                if not attribute:
                    return
                
                if attribute not in self.initial_data.columns:
                    st.write("Please enter correct attribute!")
                
            self.processed_data = pd.DataFrame(count_and_clean_inventors(self.initial_data, attribute))
            
            self.processed_data = self.processed_data.reset_index()
            self.processed_data.columns = ['Inventor Name', 'Number of Inventions']
          
            self.final_data = self.processed_data.sort_values(by='Number of Inventions', ascending=False)
            
            self.top_10 = self.final_data.head(10)

            st.subheader('Processed Data with Counts')
            st.write(self.processed_data)
            
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Number of Inventions', y='Inventor Name', data=self.top_10, palette="viridis")
            plt.xlabel('Number of Inventions')
            plt.ylabel('Inventor Name')
            plt.title('Top 10 Inventors by Number of Inventions')
            st.pyplot(plt)

        else:
            st.write("Please upload a XLSX File only.")

def main():
    ui = UI()
    ui.top_inventors()

if __name__ == "__main__":
    main()
