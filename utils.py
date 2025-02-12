import requests
import pandas as pd

Headers = {'authorization': 'ProcessoSeletivoStract2025'}

class MyException(Exception):
    pass

def get_insights(platform):
    accounts = get_asset(platform=platform, asset_type="accounts")
    fields = get_asset(platform=platform, asset_type="fields")

    fields_q = ",".join(str(field["value"]) for field in fields)
    insights = []

    for i, account in enumerate(accounts):
        response = requests.post(
            url='https://sidebar.stract.to/api/insights?platform={platform}&account={account}&token={token}&fields={fields_q}'.format(
                platform=platform,
                account=account['id'],
                token=account['token'],
                fields_q=fields_q
            ),
            headers=Headers
        )

        insights.append({
            'Platform': platform,
            'account': account['name']})
        insights[i].update(response.json())

    return insights

def get_asset(platform, asset_type):
    session = requests.Session()
    response = session.post(
        url='https://sidebar.stract.to/api/{asset_type}?platform={platform}'.format(
            asset_type=asset_type,
            platform=platform),
        headers=Headers
    )

    if 'error' in response.json():
        raise MyException(next(iter(
            response.json().values()), None))
    
    content = next(iter(
        response.json().values()), None)

    if 'pagination' in response.json():
        number_of_pages = response.json()['pagination']['total']

        for page in range(2, number_of_pages + 1):
            response = session.post(
                url='https://sidebar.stract.to/api/{asset_type}?platform={platform}&page={page}'.format(
                    asset_type=asset_type,
                    platform=platform,
                    page=page),
                headers=Headers
            )
            content.extend(next(iter(
                response.json().values()), None))
        
        return content
    
    return content

def generate_csv(mydict, summary=False):
    df_final = pd.DataFrame()
    for i, elem in enumerate(mydict):
        if i == 0:
            df = pd.DataFrame(columns=['Platform', 'account'] + list(elem['insights'][0].keys()))
            
        if summary:
            for j, insight in enumerate(elem['insights']):
                #todo: fazer soma do resumo
                pass

            df_final.to_csv("data.csv", header=True, index=False)
        
        for j, insight in enumerate(elem['insights']):
            df.loc[len(df)] = [elem['Platform'], elem['account']] + list(insight.values())

    df_final = pd.concat([df_final, df])
    df_final.to_csv("data.csv", header=True, index=False)