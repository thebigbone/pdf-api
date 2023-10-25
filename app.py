import tabula
import pandas as pd
from flask import Flask, request, jsonify

file = "bank.pdf"
tables = tabula.read_pdf(file, pages='all', multiple_tables=True)


def clean_data(df):
    df = df.replace(r'\n', ' ', regex=True)
    df = df.replace(r'\s+', ' ', regex=True)
    df = df.dropna()
    df = df.reset_index(drop=True)
    return df


df1 = clean_data(tables[0])
df1['date'] = df1['date'].str.replace('/', '')

df2 = clean_data(tables[1])
df2['date'] = df2['date'].str.replace('/', '')

json_data1 = df1.to_json(orient='records')
json_data2 = df2.to_json(orient='records')

with open('data1.json', 'w') as f:
    f.write(json_data1)

with open('data2.json', 'w') as f:
    f.write(json_data2)

df1 = pd.read_json('data1.json')
df2 = pd.read_json('data2.json')

df = pd.concat([df1, df2])

df['date'] = pd.to_datetime(df['date'], format='%m%d%Y')

app = Flask(__name__)


@app.route('/transactions', methods=['GET'])
def get_transactions():
    return jsonify(df.to_dict('records'))


@app.route('/transactions/search', methods=['GET'])
def search_transactions():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    result = df.loc[mask]
    return jsonify(result.to_dict('records'))


df['amount'] = df['amount'].replace('[\$,]', '', regex=True).astype(float)


@app.route('/balance', methods=['GET'])
def get_balance():
    date = request.args.get('date')
    mask = df['date'] <= date
    result = df.loc[mask, 'amount'].sum()
    return jsonify({'balance': '${:,.2f}'.format(result)})


if __name__ == '__main__':
    app.run(debug=True)
