import requests
import csv

Headers = {'authorization': 'ProcessoSeletivoStract2025'}

class MyException(Exception):
    pass

def get_insights(platform):
    accounts = get_asset(platform=platform, asset_type="accounts")
    fields = get_asset(platform=platform, asset_type="fields")

    fields_q = ",".join(str(field["value"]) for field in fields)
    insights = []

    for account in accounts:
        response = requests.post(
            url='https://sidebar.stract.to/api/insights?platform={platform}&account={account}&token={token}&fields={fields_q}'.format(
                platform=platform,
                account=account['id'],
                token=account['token'],
                fields_q=fields_q
            ),
            headers=Headers
        )
        
        insights.extend(next(
            iter(response.json().values()), None))
        
    insights_formatted = []

    for i, insight in enumerate(insights):
        insights_formatted.append({'Platform': platform})
        insights_formatted[i].update(insight)

    return insights_formatted

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

def generate_csv(data):
    with open('data.csv', 'w') as f:
        field_names = list(data[0].keys())
        
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(data)

