import requests
import pandas as pd
import numpy as np

from abc import ABC, abstractmethod

Headers = {'authorization': 'ProcessoSeletivoStract2025'}

class MyException(Exception):
    pass

class Loader(ABC):

    @abstractmethod
    def get_insights(self):
        pass

    @abstractmethod
    def generate_csv(self):
        pass

    def get_asset(self, platform, asset_type):
        session = requests.Session()
        response = session.get(
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
                response = session.get(
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

class PlatformLoader(Loader):

    def __init__(self, platform):
        self.platform = platform

    def get_mydict(self):
        return self._mydict

    def get_insights(self):
        accounts = self.get_asset(platform=self.platform, asset_type="accounts")
        fields = self.get_asset(platform=self.platform, asset_type="fields")
        fields_q = ",".join(str(field["value"]) for field in fields)

        insights = []

        for i, account_elem in enumerate(accounts):
            response = requests.post(
                url='https://sidebar.stract.to/api/insights?platform={platform}&account={account}&token={token}&fields={fields_q}'.format(
                    platform=self.platform,
                    account=account_elem['id'],
                    token=account_elem['token'],
                    fields_q=fields_q
                ),
                headers=Headers
            )

            insights.append({
                'Platform': self.platform,
                'account': account_elem['name']})
            insights[i].update(response.json())

        self._mydict = insights

    def generate_csv(self, summary=False):
        df_final = pd.DataFrame()

        for i, elem in enumerate(self._mydict):           
            if summary:  
                df_temp = pd.DataFrame(elem['insights'], 
                                        columns=list(self._mydict[i]['insights'][0].keys()))
                sum_array = df_temp.sum(axis=0)

                with pd.option_context('future.no_silent_downcasting', True):
                    sum_array = sum_array.replace(r'.*', np.nan, regex=True).infer_objects(copy=False)

                sum_array = sum_array.to_list()
                df_temp = pd.DataFrame(columns=['Platform', 'account'] + list(self._mydict[0]['insights'][0].keys()))
                df_temp.loc[len(df_temp)] = [elem['Platform'], elem['account']] + sum_array

            else:
                df_temp = pd.DataFrame(columns=['Platform', 'account'] + list(self._mydict[0]['insights'][0].keys()))
                for j, insight in enumerate(elem['insights']):
                    df_temp.loc[len(df_temp)] = [elem['Platform'], elem['account']] + list(insight.values())

            df_final = pd.concat([df_final, df_temp])

        df_final.to_csv("data.csv", header=True, index=False)

    def get_asset(self, platform, asset_type):
        return super().get_asset(platform, asset_type)
        
class AllPlatformsLoader(Loader):

    def get_mydict(self):
        return self._mydict
    
    def __get_platforms(self):
        session = requests.Session()
        response = session.get(
            url='https://sidebar.stract.to/api/platforms',
            headers=Headers
        )

        content = response.json()
        return content

    def get_insights(self):
        content = self.__get_platforms()
        dict_list = []

        for platform_elem in content['platforms']:
            platform = PlatformLoader(platform=platform_elem['value'])
            platform.get_insights()
            dict_list.append(platform.get_mydict())

        self._mydict = dict_list      

    def generate_csv(self, summary=False):
        df_final = pd.DataFrame()
        for i, elem in enumerate(self._mydict):
            for j, sub_elem in enumerate(elem):
                df_temp = pd.DataFrame.from_dict(sub_elem, orient='columns')
                df_insights = pd.json_normalize(df_temp['insights'])
                df_temp = df_temp[['Platform', 'account']]
                df_concat = pd.concat([df_temp, df_insights], axis=1)
                df_final = pd.concat([df_final, df_concat])

        df_final.to_csv("data.csv", header=True, index=False)