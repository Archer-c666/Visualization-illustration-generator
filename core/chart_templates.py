import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#待扩展
# ---------- 基础模板 ----------

def bar(df,x,y):
    fig,ax=plt.subplots()
    ax.bar(df[x],df[y])
    ax.set_title("Bar Chart")
    return fig


def line(df,x,y):
    fig,ax=plt.subplots()
    ax.plot(df[x],df[y],marker="o")
    ax.set_title("Line Chart")
    return fig


def scatter(df,x,y):
    fig,ax=plt.subplots()
    ax.scatter(df[x],df[y])
    ax.set_title("Scatter")
    return fig


def pie(df,label,val):
    fig,ax=plt.subplots()
    ax.pie(df[val],labels=df[label],autopct="%1.1f%%")
    return fig


# ---------- 科研模板 ----------

def heatmap(df):
    fig,ax=plt.subplots()
    corr=df.corr(numeric_only=True)
    sns.heatmap(corr,annot=True,cmap="coolwarm",ax=ax)
    ax.set_title("Correlation Heatmap")
    return fig


def boxplot(df,col):
    fig,ax=plt.subplots()
    ax.boxplot(df[col])
    ax.set_title("Boxplot")
    return fig


def regression(df,x,y):
    fig,ax=plt.subplots()
    sns.regplot(x=df[x],y=df[y],ax=ax)
    ax.set_title("Regression Fit")
    return fig


def errorbar(df,x,y):
    fig,ax=plt.subplots()
    yerr=np.std(df[y])
    ax.errorbar(df[x],df[y],yerr=yerr,fmt='o')
    ax.set_title("Error Bar")
    return fig


def double_axis(df,x,y1,y2):
    fig,ax1=plt.subplots()
    ax2=ax1.twinx()

    ax1.plot(df[x],df[y1],'b-')
    ax2.plot(df[x],df[y2],'r-')

    ax1.set_ylabel(y1,color='b')
    ax2.set_ylabel(y2,color='r')
    return fig