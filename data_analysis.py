import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st  

# GEMINI API

from google import genai
import os

client = genai.Client(api_key=os.environ["API_GEMINI"])





new_column_names = {
    'Timestamp': 'timestamp',
    '1. What is your age?': 'age',
    '2. Gender': 'gender',
    '3. Relationship Status': 'relationship_status',
    '4. Occupation Status': 'occupation_status',
    '5. What type of organizations are you affiliated with?': 'affiliated_organizations',
    '6. Do you use social media?': 'use_social_media',
    '7. What social media platforms do you commonly use?': 'social_media_platforms',
    '8. What is the average time you spend on social media every day?': 'daily_social_media_time',
    '9. How often do you find yourself using Social media without a specific purpose?': 'frequency_social_media_no_purpose',
    '10. How often do you get distracted by Social media when you are busy doing something?': 'frequency_social_media_distracted',
    "11. Do you feel restless if you haven't used Social media in a while?": 'restless_without_social_media',
    '12. On a scale of 1 to 5, how easily distracted are you?': 'distractibility_scale',
    '13. On a scale of 1 to 5, how much are you bothered by worries?': 'worry_level_scale',
    '14. Do you find it difficult to concentrate on things?': 'difficulty_concentrating',
    '15. On a scale of 1-5, how often do you compare yourself to other successful people through the use of social media?': 'compare_to_successful_people_scale',
    '16. Following the previous question, how do you feel about these comparisons, generally speaking?': 'feelings_about_comparisons',
    '17. How often do you look to seek validation from features of social media?': 'frequency_seeking_validation',
    '18. How often do you feel depressed or down?': 'frequency_feeling_depressed',
    '19. On a scale of 1 to 5, how frequently does your interest in daily activities fluctuate?': 'interest_fluctuation_scale',
    '20. On a scale of 1 to 5, how often do you face issues regarding sleep?': 'sleep_issues_scale',
}

# LOAD AND RENAME THE DATA
df = pd.read_csv("smmh.csv")
df = df.rename(columns=new_column_names)


# DATA CLEANING
list(filter(lambda x: x not in ["Female", "Male"], df['gender'].unique()))
df = df.replace(list(filter(lambda x: x not in ["Female", "Male"], df['gender'].unique())), 'others')

df["month"], df["day"], _ = zip(*df["timestamp"].apply(lambda x: x.split('/')))
df = df.drop(columns="timestamp")

df["month"] = df["month"].apply(lambda x: int(x))
df["day"] = df["day"].apply(lambda x: int(x))

mode_val = df['affiliated_organizations'].mode()[0]
df['affiliated_organizations'].fillna(mode_val)


# GROUPING COLUMNS
all_col = df.columns.tolist()
categ_col = df.select_dtypes(include=['object']).columns.tolist()
num_col = df.select_dtypes(include=['number']).columns.tolist()


# TYPES OF GRAPHS
graphs = {

    "Univariant" : {
        "Histogram" : [num_col],
        "Box Plot" : [num_col],
        "Violin Plot" : [num_col],
        "Bar Plot" : [categ_col],
        "Pie Plot" : [categ_col],
        "Count Plot" : [categ_col],
    },

    "Bivariant" : {
        "Scatter Plot" : [num_col, num_col],
        "Histogram" : [num_col, categ_col],
        "Line Chart" : [num_col, num_col],
        "Bar Chart" : [categ_col, num_col],
        "Box Plot" : [categ_col, num_col],
        "Violin Plot" : [categ_col, num_col],
        "Heatmap" : [all_col, all_col],
    },

    "Multivariant" : {
        "Heatmap" : [all_col, all_col, num_col],
        "3D Scatter Plot" : [num_col, num_col, num_col],
    }
}


# MAIN SIDEBAR
st.sidebar.header("Graph Options")

graph_types_1 = list(graphs.keys())
graph_sel_1 = st.sidebar.selectbox("Choose no of variables", graph_types_1)
graph_types_2 = list(graphs[graph_sel_1].keys())
graph_sel_2 = st.sidebar.selectbox("Choose a Graph type", graph_types_2)
col_types = graphs[graph_sel_1][graph_sel_2]




fig, ax = plt.subplots()
cols = []

# UNIVARIANT
if graph_sel_1 == (graph_types_1[0]):    
    x_axis = st.sidebar.selectbox("Select column", col_types[0])
    cols.clear()
    cols.append(x_axis)

    match graph_sel_2:
        case "Histogram": 
            st.write(f"### Histogram of {x_axis}")
            sns.histplot(df[x_axis], kde=True, ax=ax)
        case "Box Plot": 
            st.write(f"### Box Plot of {x_axis}")
            sns.boxplot(x=df[x_axis], ax=ax)
        case "Violin Plot": 
            st.write(f"### Violin Plot of {x_axis}")
            sns.violinplot(x=df[x_axis], ax=ax)
        case "Bar Plot": 
            st.write(f"### Bar Plot of {x_axis}")
            bar_data = df[x_axis].value_counts()
            plt.bar(bar_data.index, bar_data.values)
        case "Pie Plot": 
            st.write(f"### Pie Chart of {x_axis}")
            pie_data = df[x_axis].value_counts()
            ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
        case "Count Plot": 
            st.write(f"### Count Plot of {x_axis}")
            sns.countplot(x=df[x_axis], ax=ax)

# BIVARIANT
elif graph_sel_1 == (graph_types_1[1]):
    x_axis = st.sidebar.selectbox("Select x-axis", col_types[0])
    y_axis = st.sidebar.selectbox("Select y-axis", col_types[1])

    cols.clear()
    cols.extend([x_axis, y_axis])

    match graph_sel_2:
        case "Scatter Plot":
            st.write(f"### Scatter Plot: {x_axis} vs {y_axis}")
            sns.scatterplot(x=x_axis, y=y_axis, data=df, ax=ax)
        case "Histogram": 
            st.write(f"### Histogram of {x_axis} vs {y_axis}")
            sns.histplot(data=df, x=x_axis, hue= y_axis ,kde=True, ax=ax)
        case "Line Chart":
            st.write(f"### Line Chart of {x_axis}")
            sns.lineplot(x=x_axis, y=y_axis, data=df)            
        case "Bar Chart":
            st.write(f"### Bar Plot: {x_axis} vs {y_axis}")
            sns.barplot(x=x_axis, y=y_axis, data=df, ax=ax)
        case "Box Plot":
            st.write(f"### Box Plot of {x_axis} vs {y_axis}")
            sns.boxplot(x=x_axis, y=y_axis, data=df)
        case "Violin Plot":
            st.write(f"### Violin Plot of {x_axis} vs {y_axis}")
            sns.violinplot(x=df[x_axis], y= df[y_axis], ax=ax)
        case "Heatmap" :
            st.write(f"### Correlation Heatmap: {x_axis} vs {y_axis}")
            if(x_axis in num_col and y_axis in num_col):
                corr = df[[x_axis, y_axis]].corr()
            elif(x_axis in num_col):
                corr = df.pivot_table(columns=y_axis, values=x_axis, aggfunc="mean")
            elif(y_axis in num_col):
                corr = df.pivot_table(columns=x_axis, values=y_axis, aggfunc="mean")
            else:
                corr = pd.crosstab(df[x_axis], df[y_axis])
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)

# MULTIVARIANT
elif graph_sel_1 == (graph_types_1[2]):
    x_axis = st.sidebar.selectbox("Select x-axis", col_types[0])
    y_axis = st.sidebar.selectbox("Select y-axis", list(set(col_types[1]) - set(x_axis)))
    z_axis = st.sidebar.selectbox("Select z-axis", list(set(col_types[2]) - set([x_axis, y_axis])))

    cols.clear()
    cols.extend([x_axis, y_axis, z_axis])
    
    match graph_sel_2:
        case "Heatmap":
            st.write(f"### Correlation Heatmap of selected columns")
            fig, ax = plt.subplots(figsize=(10, 7))
            temp_df = df.groupby([x_axis, y_axis])[z_axis].mean().reset_index()
            pivot_table = temp_df.pivot_table(index=x_axis, columns=y_axis, values=z_axis)
            sns.heatmap(pivot_table, annot=True, cmap='coolwarm', ax=ax)        
        
        case "3D Scatter Plot":
            st.write(f"### 3D Scatter Plot: {x_axis}, {y_axis}, {z_axis}")
            fig = px.scatter_3d(df, x=x_axis, y=y_axis, z=z_axis, color=df[x_axis])
            fig.update_layout(width=1000, height=700)
            st.plotly_chart(fig)
            fig = None

if fig:
    st.pyplot(fig)


# PROMPT FOR AI
data = df[cols]
prompt = f"""
Analyze the following data used in {graph_sel_2} with columns {cols}:
{data}

and provide only with summary of trend of the following data,

do not provide provide heading, just provide data

"""
# FEEDING PROMPT AND RETREIVING RESPONSE
response = client.models.generate_content(
    model="gemini-2.0-flash", contents=prompt
)

st.subheader("Summary of Trends:")
st.write(response.text)


# SUB SIDEBAR
st.sidebar.subheader("Statistical Analysis")
if st.sidebar.checkbox("Show Data Preview?"):    
    st.write("#### Data Preview")
    st.write(df)
if st.sidebar.checkbox("Show Descriptive Statistics"):
    st.write("#### Descriptive Statistics")
    st.write(df[num_col].describe())






# * Univariate:
#     -> histplot/hist for count of data of a column of data    
#     -> BoxPlot
#     -> violin plot
#     -> countplot
#     -> pie chart

# * Bivariate:
#     -> scatter plot
#     -> pair plot (not good)
#     -> Bar chart with 2 diff value on x and y, or with x being one col and y being its count (eg no of repsponders from male and female) 
#     -> Box plot
#     -> 2 var histogram
#     -> heatmap (correlation analysis)

# * Multivariate:
#     -> scatterplot
#     -> heatmap
#     -> PCA
#     -> 3d Scatter plot




# ---------->
# make ganders into three male female and others
# convert timestamp into month and year
# add hue as additional option for graphs 

