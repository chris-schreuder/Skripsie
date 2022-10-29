from turtle import color
from flask import Flask, render_template, request, jsonify
import pandas as pd
from coding.admin import BaseValidation, Visualization

app = Flask(__name__, static_folder='static')

context = {}


@app.route('/')
def admin():
    return render_template('main-admin.html')

@app.route('/base_validation')
def base_validation():
    # resultsObject = BaseValidation()
    # resultsObject.getAccuracy()
    # df1 = resultsObject.getAlCostDf()
    # df2 = resultsObject.getResultsDf()
    # df3 = resultsObject.getAccuracyDf()

    df1 = pd.read_csv('data/base_allCosts1.csv')
    df1.drop(['testSeq', 'trainSeq'], inplace=True, axis=1)
    df2 = pd.read_csv('data/base_results1.csv')
    df2.drop(['testSeq', 'trainSeq'], inplace=True, axis=1)
    df3 = pd.read_csv('data/base_accuracy1.csv')

    
    return render_template('base_validation.html', tables1=[df1.to_html()], titles1=df1.columns.values, tables2=[df2.to_html()], titles2=df2.columns.values, tables3=[df3.to_html()], titles3=df3.columns.values)

@app.route('/signal_visualization', methods=['GET','POST'])
def signal_visualization():

    visualizationObject = Visualization()

    df1 = visualizationObject.getResults()
    df2 = visualizationObject.getCosts()
    instructions = ['eat', 'fetch', 'lay', 'name', 'sit', '---']

    dfFilter = {}

    if request.method == 'POST':
        if request.form['button'] == 'instruction':
            instructionType = request.form.get('instructionType')
            dfFilter = df2[df2['test'] == instructionType]
            instructionNum = int(request.form.get('instructionNum'))
            rowStart = 20*5*(instructionNum - 1)
            rowEnd = rowStart + 20*5
            dfFilter = dfFilter.iloc[rowStart:rowEnd, :]
            dfFilter = dfFilter.sort_values(by=['costNorm'])
            plot = dfFilter.plot(kind='scatter', x='costNorm', y='train', color='blue')
            fig = plot.get_figure()
            fig.savefig("plot.png")
            
        elif request.form['button'] == 'top':
            topNum = int(request.form.get('topNum'))
        return render_template('signal_visual.html', dataframe=[df1.to_html()], titles=df1.columns.values, instructionsDf=[df2.to_html()], titlesInstructions=df2.columns.values, instructions=instructions, filterDf=[dfFilter.to_html()], titlesFilter=dfFilter.columns.values, costPlot=plot)
    else:
        return render_template('signal_visual.html', dataframe=[df1.to_html()], titles=df1.columns.values, instructionsDf=[df2.to_html()], titlesInstructions=df2.columns.values, instructions=instructions)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)