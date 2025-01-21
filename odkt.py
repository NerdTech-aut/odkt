import io
import re
import json
import time
import folium
import sqlite3
import pyogrio
import pyogrio.errors
import pyogrio.core
import pyogrio.gdal_data
import pyogrio.geopandas
import pyogrio.proj_data
import pyogrio.raw
import pyogrio.tests
import pyogrio.util
import pyogrio._compat
import pyogrio._env
import webview
import platform
import requests
import warnings
import pandas as pd
import geopandas as gpd
from zipfile import ZipFile
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from configparser import ConfigParser
from pyproj.transformer import Transformer

#https://pywebview.flowrl.com/examples/js_api.html

class Content:
    message = ""

    def read_config(self):
        """
        Function to read the config file

        Parameters:
            self
        """
        self._config = ConfigParser()
        self._config.read("config.ini")

    def get_web_debug_status_from_config(self) -> str:
        """
        Function get the web_debug variable from the config file

        Parameters:
            self

        Returns:
            web_debug (bool) : Returns the web_debug variable as a boolean
        """
        self.read_config()
        return str(self._config.get("Options", "web_debug")).strip().lower() == 'true'

    def set_message(self, msg:str):
        """
        Function to update the message variable with new content
        In addition the new content gets printed to the console

        Parameters:
        self
        msg (str) : New message content
        """
        self.message = msg
        print(">>>>> " + msg)

    def get_message(self):
        """
        Function to get the content of the message variable

        Parameters:
        self
        """
        return self.message

    def bba_decode_type(self) -> str:
        """
        Function to determine the decode type of bba 2020 and bba 2030 documents for the current platform

        Parameters:
            self

        Returns:
            decode_type (string) : The decode type for the platform
        """
        decode_type = ""
        if platform.system == "Windows":
            decode_type = "mbcs"
        elif platform.system == "Linux":
            decode_type = "unicode_escape"
        else:
            decode_type = "unicode_escape"
        return decode_type

    def update(self):
        """
        The main function to update the open data content
        Calls the specific functions for cellular, fixed and grant open data update

        Parameters:
            self
        """
        self.read_config()
        self.cellular()
        self.fixed()
        self.grant()

    def cellular(self):
        """
        Function to update cellular open data content for all operators

        Parameters:
            self
        """
        #A1
        A1_html = self.load_data(self._config.get("Content", "A1_html_url")).decode("utf-8")
        self.set_message("Schritt 1/56 - A1 HTML")
        A1_zip_links = self.cellular_A1_get_zip_links(A1_html)
        self.set_message("Schritt 2/56 - A1 ZIP links")
        A1_zip_n78 = self.load_data(A1_zip_links[0])
        self.set_message("Schritt 3/56 - A1 n78 ZIP")
        A1_csv_n78 = self.zip_to_csv_str(A1_zip_n78)
        self.set_message("Schritt 4/56 - A1 n78 CSV")
        A1_df_n78 = self.cellular_csv_str_to_df(A1_csv_n78)
        self.set_message("Schritt 5/56 - A1 n78 Dataframe")
        self.df_into_db(A1_df_n78, "A1_3500")
        self.set_message("Schritt 6/56 - A1 n78 Datenbank fertig")
        A1_zip_Speedmap = self.load_data(A1_zip_links[1])
        self.set_message("Schritt 7/56 - A1 Speedmap ZIP")
        A1_csv_Speedmap = self.zip_to_csv_str(A1_zip_Speedmap)
        self.set_message("Schritt 8/56 - A1 Speedmap CSV")
        A1_df_Speedmap = self.cellular_csv_str_to_df(A1_csv_Speedmap)
        self.set_message("Schritt 9/56 - A1 Speedmap Dataframe")
        self.df_into_db(A1_df_Speedmap, "A1_Speedmap")
        self.set_message("Schritt 10/56 - A1 Speedmap Datenbank fertig")
        #Magenta
        Magenta_html_n78 = self.load_data(self._config.get("Content", "Magenta_html_url_n78")).decode("utf-8")
        self.set_message("Schritt 11/56 - Magenta n78 HTML")
        Magenta_csv_link_n78 = self.cellular_Magenta_get_csv_link(Magenta_html_n78)
        self.set_message("Schritt 12/56 - Magenta n78 CSV link")
        Magenta_csv_n78 = self.load_data(Magenta_csv_link_n78).decode("utf-8")
        self.set_message("Schritt 13/56 - Magenta n78 CSV")
        Magenta_df_n78 = self.cellular_csv_str_to_df(Magenta_csv_n78)
        self.set_message("Schritt 14/56 - Magenta n78 Dataframe")
        self.df_into_db(Magenta_df_n78, "Magenta_3500")
        self.set_message("Schritt 15/56 - Magenta n78 Datenbank fertig")
        Magenta_html_Speedmap = self.load_data(self._config.get("Content", "Magenta_html_url_Speedmap")).decode("utf-8")
        self.set_message("Schritt 16/56 - Magenta Speedmap HTML")
        Magenta_csv_link_Speedmap = self.cellular_Magenta_get_csv_link(Magenta_html_Speedmap)
        self.set_message("Schritt 17/56 - Magenta Speedmap CSV link")
        Magenta_csv_Speedmap = self.load_data(Magenta_csv_link_Speedmap).decode("utf-8")
        self.set_message("Schritt 18/56 - Magenta Speedmap CSV")
        Magenta_df_Speedmap = self.cellular_csv_str_to_df(Magenta_csv_Speedmap)
        self.set_message("Schritt 19/56 - Magenta Speedmap Dataframe")
        self.df_into_db(Magenta_df_Speedmap, "Magenta_Speedmap")
        self.set_message("Schritt 20/56 - Magenta Speedmap Datenbank fertig")
        #Drei
        Drei_csv_n78 = self.load_data(self._config.get("Content", "Drei_csv_url_n78")).decode("utf-8")
        self.set_message("Schritt 21/56 - Drei n78 CSV")
        Drei_df_n78 = self.cellular_csv_str_to_df(Drei_csv_n78)
        self.set_message("Schritt 22/56 - Drei n78 Dataframe")
        self.df_into_db(Drei_df_n78, "Drei_3500")
        self.set_message("Schritt 23/56 - Drei n78 Datenbank fertig")
        Drei_csv_Speedmap = self.load_data(self._config.get("Content", "Drei_csv_url_Speedmap")).decode("utf-8")
        self.set_message("Schritt 24/56 - Drei Speedmap CSV")
        Drei_df_Speedmap = self.cellular_csv_str_to_df(Drei_csv_Speedmap)
        self.set_message("Schritt 25/56 - Drei Speedmap Dataframe")
        self.df_into_db(Drei_df_Speedmap, "Drei_Speedmap")
        self.set_message("Schritt 26/56 - Drei Speedmap Datenbank fertig")
        #Spusu
        Spusu_csv_n78 = self.load_data(self._config.get("Content", "Spusu_csv_url_n78")).decode("utf-8")
        self.set_message("Schritt 27/56 - Spusu n78 CSV")
        Spusu_df_n78 = self.cellular_csv_str_to_df(Spusu_csv_n78)
        self.set_message("Schritt 28/56 - Spusu n78 Dataframe")
        self.df_into_db(Spusu_df_n78, "Spusu_3500")
        self.set_message("Schritt 29/56 - Spusu n78 Datenbank fertig")
        #Liwest
        Liwest_csv_n78 = self.load_data(self._config.get("Content", "Liwest_csv_url_n78")).decode("utf-8")
        self.set_message("Schritt 30/56 - Liwest n78 CSV")
        Liwest_df_n78 = self.cellular_csv_str_to_df(Liwest_csv_n78)
        self.set_message("Schritt 31/56 - Liwest n78 Dataframe")
        self.df_into_db(Liwest_df_n78, "Liwest_3500")
        self.set_message("Schritt 32/56 - Liwest n78 Datenbank fertig")
        #Salzburg AG
        SalzburgAG_csv_n78 = self.load_data(self._config.get("Content", "SalzburgAG_csv_url_n78")).decode("utf-8")
        self.set_message("Schritt 33/56 - Salzburg AG n78 CSV")
        SalzburgAG_df_n78 = self.cellular_csv_str_to_df(SalzburgAG_csv_n78)
        self.set_message("Schritt 34/56 - Salzburg AG n78 Dataframe")
        self.df_into_db(SalzburgAG_df_n78, "CableLinkAir_3500")
        self.set_message("Schritt 35/56 - Salzburg AG n78 Datenbank fertig")
        #Graz Holding
        GrazHolding_csv_n78 = self.load_data(self._config.get("Content", "GrazHolding_csv_url_n78")).decode("utf-8")
        self.set_message("Schritt 36/56 - Graz Holding n78 CSV")
        GrazHolding_df_n78 = self.cellular_csv_str_to_df(GrazHolding_csv_n78)
        self.set_message("Schritt 37/56 - Graz Holding n78 Dataframe")
        self.df_into_db(GrazHolding_df_n78, "Citycom_3500")
        self.set_message("Schritt 38/56 - Graz Holding n78 Datenbank fertig")

    def load_data(self, url:str) -> bytes:
        """
        Function to download content from a webserver

        Parameters:
            self
            url (str) : Address to download content from

        Returns:
            response_content (bytes) : The downloaded content
        """
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            self.set_message("Daten konnten nicht geladen werden - Status" + str(response.status_code) + " " + url)            

    def cellular_A1_get_zip_links(self, html:str) -> list:
        """
        Function to extract A1 open data zip archive links from the overview html document

        Parameters:
            self
            html (str) : HTML content of the A1 open data overview page

        Returns:
            list_of_links (list) : The two extracted zip archive links
        """
        soup = BeautifulSoup(html, 'lxml')
        element = soup.find_all("span", {"class":"icon-link-download"})
        return [str(element[0]).split("href=\"")[1].split("\"")[0], str(element[1]).split("href=\"")[1].split("\"")[0]]
    
    def cellular_Magenta_get_csv_link(self, html:str) -> str:
        """
        Function to extract the Magenta open data csv link from the overview html document

        Parameters:
            self
            html (str) : HTML content of the Magenta open data overview page

        Returns:
            csv_link (list) : The extracted csv link
        """
        soup = BeautifulSoup(html, 'lxml')
        element = soup.find("a", {"class":"link icon"})
        return "https://www.magenta.at" + str(element).split("href=\"")[1].split("\" role=\"")[0]

    def zip_to_csv_str(self, zip_archive:bytes) -> str:
        """
        Function to extract a zip archive, get the csv file and return it as a string 

        Parameters:
            self
            zip_archive (bytes) : Zip archive which includes a single open data csv file 

        Returns:
            csv_link (list) : The extracted csv link
        """
        response_csv_as_string = None

        with ZipFile(io.BytesIO(zip_archive), 'r') as zip_file:
            with zip_file.open(zip_file.namelist()[0]) as file:
                response_csv_as_string = file.read()
                if type(response_csv_as_string) == bytes:
                    response_csv_as_string = response_csv_as_string.replace(b'\x93', b'\x22').replace(b'\x94', b'\x22').decode("utf-8")

        return response_csv_as_string

    def cellular_csv_str_to_df(self, csv:str) -> pd.DataFrame:
        """
        Function to convert a cellular open data csv file to pandas dataframe

        Parameters:
            self
            csv (str) : Cellular open data csv file as a string

        Returns:
            df (pd.DataFrame) : The finished dataframe
        """
        string_io = io.StringIO("operator;reference;license;rfc_date;raster;dl_normal;ul_normal;dl_max;ul_max\r" + csv[csv.find('\n'):].replace("ï»¿",""))
        df = pd.read_csv(filepath_or_buffer=string_io, sep=";")
        df['NORTH'] = df['raster'].apply(lambda x: int(x.split('mN')[1].split('E')[0]))
        df['EAST'] = df['raster'].apply(lambda x: int(x.split('E')[-1]))
        df['RFC_DATE'] = df['rfc_date'].apply(lambda x: ".".join((str(x).split("-"))[::-1]))
        df.fillna({'dl_normal': 0, 'ul_normal': 0, 'dl_max': 0, 'ul_max': 0}, inplace=True)
        df['DL_NORMAL'] = df['dl_normal'].apply(lambda x: round(int(x) / 1000000, 2))
        df['UL_NORMAL'] = df['ul_normal'].apply(lambda x: round(int(x) / 1000000, 2))
        df['DL_MAX'] = df['dl_max'].apply(lambda x: round(int(x) / 1000000, 2))
        df['UL_MAX'] = df['ul_max'].apply(lambda x: round(int(x) / 1000000, 2))
        df = df[['NORTH', 'EAST', 'RFC_DATE', 'DL_NORMAL', 'UL_NORMAL', 'DL_MAX', 'UL_MAX']]
        return df
    
    def df_into_db(self, df:pd.DataFrame, table:str):
        """
        Function to convert a cellular open data csv file to pandas dataframe

        Parameters:
            self
            df (pd.DataFrame) : Cellular open data dataframe
            table (str) : Name of the table in which the dataframe is to be saved
        """
        sqlite3_database_connection = sqlite3.connect('map_data.db')
        df.to_sql(table, sqlite3_database_connection, index=False, if_exists="replace")

    def fixed(self):
        """
        Function to update fixed broadband open data

        Parameters:
            self
        """
        fixed_json  = json.loads(self.load_data(self._config.get("Content", "Festnetz_Grant_json_url")).decode("utf-8"))
        self.set_message("Schritt 39/56 - Festnetz JSON")
        fixed_zip = self.load_data(fixed_json["result"]["resources"][0]["url"])
        self.set_message("Schritt 40/56 - Festnetz ZIP")
        fixed_csv_str = self.zip_to_csv_str(fixed_zip)
        self.set_message("Schritt 41/56 - Festnetz CSV")
        df = self.fixed_csv_str_to_df(fixed_csv_str)
        self.set_message("Schritt 42/56 - Festnetz Dataframe")
        self.df_into_db(df, "Festnetz")
        self.set_message("Schritt 43/56 - Festnetz Datenbank fertig")

    def fixed_csv_str_to_df(self, csv:str):
        """
        Function to convert a fixed broadband open data csv file to pandas dataframe

        Parameters:
            self
            csv (str) : Fixed broadband open data csv file as a string

        Returns:
            df (pd.DataFrame) : The finished dataframe
        """
        string_io = io.StringIO(csv)
        df = pd.read_csv(filepath_or_buffer=string_io, sep=",")
        df['NORTH'] = df['l000100v3'].apply(lambda x: int(x.split('mN')[1].split('E')[0]))
        df['EAST'] = df['l000100v3'].apply(lambda x: int(x.split('E')[-1]))
        df['BEARBEITUNG_BBA'] = df['bearbeitung_bbb'].apply(lambda x: ".".join(((str(x).split("T")[0]).split("-"))[::-1]))
        df = df.rename(columns={'infrastrukturanbieterin': 'INFRASTRUKTURANBIETER', 'technik': 'TECHNIK', 'download': 'DOWNLOAD', 'upload': 'UPLOAD'})
        df = df[['NORTH', 'EAST', 'INFRASTRUKTURANBIETER', 'TECHNIK', 'DOWNLOAD', 'UPLOAD', 'BEARBEITUNG_BBA']]
        return df
    
    def grant(self):
        """
        Function to update broadband grant open data

        Parameters:
            self
        """
        #GPKG
        grant_json  = json.loads(self.load_data(self._config.get("Content", "Festnetz_Grant_json_url")).decode("utf-8"))
        self.set_message("Schritt 44/56 - Grant JSON")
        grant_zip = self.load_data(grant_json["result"]["resources"][2]["url"])
        self.set_message("Schritt 45/56 - Geförderter Ausbau ZIP")
        grant_gpkg = self.zip_to_gpkg(grant_zip)
        self.set_message("Schritt 46/56 - Geförderter Ausbau GPKG")
        gdf = self.grant_gpkg_to_gdf(grant_gpkg)
        self.set_message("Schritt 47/56 - Geförderter Ausbau Dataframe")
        self.df_into_db(gdf, "Gefoerderter_Ausbau")
        self.set_message("Schritt 48/56 - Geförderter Ausbau Datenbank fertig")
        #BBA Project CSV Links
        grant_BBA_project_html = self.load_data(self._config.get("Content", "BMF_BBA_html_url")).decode("utf-8")
        self.set_message("Schritt 49/56 - Geförderter Ausbau Projekte HTML")
        grant_BBA_project_links = self.grant_bba_get_csv_links(grant_BBA_project_html)
        self.set_message("Schritt 50/56 - Geförderter Ausbau Projekte CSV links")
        #BBA2020
        grant_BBA2020_csv = self.load_data(grant_BBA_project_links[1]).decode(self.bba_decode_type())
        self.set_message("Schritt 51/56 -  Geförderter Ausbau BBA2020 CSV")
        grant_BBA2020_df = self.grant_bba_csv_str_to_df(grant_BBA2020_csv)
        self.set_message("Schritt 52/56 - Geförderter Ausbau BBA2020 Dataframe")
        #BBA2030
        grant_BBA2030_csv = self.load_data(grant_BBA_project_links[0]).decode(self.bba_decode_type())
        self.set_message("Schritt 53/56 -  Geförderter Ausbau BBA2030 CSV")
        grant_BBA2030_df = self.grant_bba_csv_str_to_df(grant_BBA2030_csv)
        self.set_message("Schritt 54/56 - Geförderter Ausbau BBA2030 Dataframe")
        grant_BBA_df = self.grant_combine_dfs(grant_BBA2020_df, grant_BBA2030_df)
        self.set_message("Schritt 55/56 - Geförderter Ausbau Dataframes kombinieren")
        self.df_into_db(grant_BBA_df, "BBA_Projekte")
        self.set_message("Schritt 56/56 - Geförderter Ausbau BBA Datenbank fertig")

    def zip_to_gpkg(self, zip_archive:bytes) -> bytes:
        """
        Function to extract a zip archive and get the gpkg file

        Parameters:
            self
            zip_archive (bytes) : Zip archive which includes a single open data gpkg file 

        Returns:
            response_gpkg (bytes) : The extracted gpkg file
        """
        response_gpkg = None

        with ZipFile(io.BytesIO(zip_archive), 'r') as zip_file:
            with zip_file.open(zip_file.namelist()[0]) as file:
                response_gpkg = file.read()
        return response_gpkg
    
    def grant_bba_get_csv_links(self, html:str) -> list:
        """
        Function to extract BBA project data csv links from the overview html document

        Parameters:
            self
            html (str) : HTML content of the BBA project data overview page

        Returns:
            list_of_links (list) : The two extracted zip archive links
        """
        soup = BeautifulSoup(html, 'lxml')
        element = soup.find_all("a", string=re.compile(r"BBA20(2|3)0 Geförderter Ausbau Q(\d)/20(\d\d)"))
        return [str(element[0]).split("href=\"")[1].split("\"")[0], str(element[1]).split("href=\"")[1].split("\"")[0]]

    def grant_gpkg_to_gdf(self, gpkg:bytes) -> gpd.GeoDataFrame:
        """
        Function to convert a broadband grant gpkg file into a geopandas dataframe

        Parameters:
            self
            gpkg (bytes) : A broadband grant gpkg file

        Returns:
            gdf (gpd.GeoDataFrame) : The finished geopandas dataframe
        """
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', message='.*GPKG application_id.*')
            bytes_io = io.BytesIO(gpkg)
            gdf = gpd.read_file(bytes_io, layer=gpd.list_layers(bytes_io).loc[0, 'name'])
            gdf['NORTH'] = gdf['l000100v3'].apply(lambda x: int(x.split('mN')[1].split('E')[0]))
            gdf['EAST'] = gdf['l000100v3'].apply(lambda x: int(x.split('E')[-1]))
            gdf['BEARBEITUNG_BBA'] = gdf['bearbeitung_bbb'].apply(lambda x: ".".join(((str(x).split(" ")[0]).split("-"))[::-1]))
            gdf = gdf.rename(columns={'technik': 'TECHNIK', 'antragsnummer': 'ANTRAGSNUMMER'})
            gdf = gdf[['NORTH', 'EAST', 'TECHNIK', 'ANTRAGSNUMMER', 'BEARBEITUNG_BBA']]
            return gdf
    
    def grant_bba_csv_str_to_df(self, csv:str) -> pd.DataFrame:
        """
        Function to convert a broadband grant csv file into a pandas dataframe

        Parameters:
            self
            csv (str) : A broadband grant csv file as a string

        Returns:
            df (pd.DataFrame) : The finished pandas dataframe
        """
        string_io = io.StringIO(csv)
        df = pd.read_csv(filepath_or_buffer=string_io, sep=";")
        df = df.rename(columns={ 'Antragsnummer': 'ANTRAGSNUMMER', 'Ausschreibung': 'AUSSCHREIBUNG', 'FördernehmerIn': 'FOERDERNEHMER', 'Projekttitel': 'PROJEKTTITEL', 'Projektkosten (Euro)': 'PROJEKTKOSTEN_EURO', 'Förderbetrag (Euro)': 'FOERDERBETRAG_EURO', 'Förderbetrag Land Anschlussförderung (Euro)': 'FOERDERBETRAG_LAND_ANSCHLUSSFOERDERUNG_EURO', 'Fördersatz (%)': 'FOERDERSATZ_PROZENT', 'Tag der Gewährung (Datum)': 'TAG_DER_GEWAEHRUNG_DATUM', 'Vertragsabschluss (Datum)': 'VERTRAGSABSCHLUSS_DATUM', 'Projektende (Datum)': 'PROJEKTENDE_DATUM', 'förderbare Kosten nach Endprüfung': 'FOERDERBARE_KOSTEN_NACH_ENDPRUEFUNG_EURO', 'Förderbetrag nach Endprüfung': 'FOERDERBETRAG_NACH_ENDPRUEFUNG_EURO', 'Projektstatus': 'PROJEKTSTATUS'})
        df = df[["ANTRAGSNUMMER", "AUSSCHREIBUNG", "FOERDERNEHMER", "PROJEKTTITEL", "PROJEKTKOSTEN_EURO", "FOERDERBETRAG_EURO", "FOERDERBETRAG_LAND_ANSCHLUSSFOERDERUNG_EURO", "FOERDERSATZ_PROZENT", "TAG_DER_GEWAEHRUNG_DATUM", "VERTRAGSABSCHLUSS_DATUM", "PROJEKTENDE_DATUM", "FOERDERBARE_KOSTEN_NACH_ENDPRUEFUNG_EURO", "FOERDERBETRAG_NACH_ENDPRUEFUNG_EURO", "PROJEKTSTATUS"]]
        df.fillna({'FOERDERBETRAG_LAND_ANSCHLUSSFOERDERUNG_EURO': 0, 'FOERDERBARE_KOSTEN_NACH_ENDPRUEFUNG_EURO': 0, 'FOERDERBETRAG_NACH_ENDPRUEFUNG_EURO': 0}, inplace=True)
        df['FOERDERBETRAG_LAND_ANSCHLUSSFOERDERUNG_EURO'] = df['FOERDERBETRAG_LAND_ANSCHLUSSFOERDERUNG_EURO'].apply(lambda x: float(str(x).replace(",", ".")))
        return df
    
    def grant_combine_dfs(self, df_BBA2020:pd.DataFrame, df_BBA2030:pd.DataFrame) -> pd.DataFrame:
        """
        Function to combine the BBA 2020 and BBA 2030 broadband grant pandas dataframes into a single pandas dataframe

        Parameters:
            self
            df_BBA2020 (pd.DataFrame) : The BBA 2020 broadband grant pandas dataframe
            df_BBA2030 (pd.DataFrame) : The BBA 2030 broadband grant pandas dataframe

        Returns:
            df (pd.DataFrame) : The combined pandas dataframe
        """
        return pd.concat([df_BBA2020, df_BBA2030], ignore_index=True)

class Map:
    message = ""

    def set_message(self, msg:str):
        """
        Function to update the message variable with new content
        In addition the new content gets printed to the console

        Parameters:
            self
            msg (str) : New message content
        """
        self.message = msg
        print(">>>>> " + msg)

    def get_message(self):
        """
        Function to get the content of the message variable

        Parameters:
            self
        """
        return self.message

    def create(self, location:str, radius:float, A1_5Gn78:bool, Magenta_5Gn78:bool, Drei_5Gn78:bool, GrazHolding_5Gn78:bool, Liwest_5Gn78:bool, MassResponse_5Gn78:bool, SalzburgAG_5Gn78:bool, A1_Speedmap:bool, Magenta_Speedmap:bool, Drei_Speedmap:bool, fixed:bool, grant:bool):
        """
        Function to create a new map with the specified location, radius and layers
        Switches to the created map once it is done

        Parameters:
            self
            location (str) : Location of the center of the map - this can be WSG84 coordinates, an ETRS89e square-id or address
            radius (float) : Radius from the center point in kilometers
            A1_5Gn78 (bool) : Boolean for the A1 5G n78 layer
            Magenta_5Gn78 (bool) : Boolean for the Magenta 5G n78 layer
            Drei_5Gn78 (bool) : Boolean for the Drei 5G n78 layer
            GrazHolding_5Gn78 (bool) : Boolean for the Graz Holding 5G n78 layer
            Liwest_5Gn78 (bool) : Boolean for the Liwest 5G n78 layer
            MassResponse_5Gn78 (bool) : Boolean for the MassResponse 5G n78 layer
            SalzburgAG_5Gn78 (bool) : Boolean for the Salzburg AG 5G n78 layer
            A1_Speedmap (bool) : Boolean for the A1 Speedmap layer
            Magenta_Speedmap (bool) : Boolean for the Magenta Speedmap layer
            Drei_Speedmap (bool) : Boolean for the Drei Speedmap layer
            fixed (bool) : Boolean for the fixed broadband layer
            grant (bool) : Boolean for the broadband grant layer
        """
        steps_cellular = A1_5Gn78 + Magenta_5Gn78 + Drei_5Gn78 + GrazHolding_5Gn78 + Liwest_5Gn78 + MassResponse_5Gn78 + SalzburgAG_5Gn78 + A1_Speedmap + Magenta_Speedmap + Drei_Speedmap
        steps = 2 + steps_cellular + int(bool(steps_cellular)) + fixed + fixed + grant + grant
        try:
            is_ETRS89e = self.check_if_ETRS89e(location)
            is_WSG84 = self.check_if_WSG84(location)
            if is_ETRS89e == True:
                center_ETRS89e = self.center_ETRS89e_from_string(location)
                center_WSG84 = self.center_WSG84_from_ETRS89e(center_ETRS89e)
            elif is_WSG84 == True:
                center_WSG84 = self.center_WSG84_from_string(location)
                center_ETRS89e = self.center_ETRS89e_from_WSG84(center_WSG84)
            else:
                center = self.convert_address_to_WSG84(location)
                if center != "":
                    center_WSG84 = self.center_WSG84_from_string(center)
                    center_ETRS89e = self.center_ETRS89e_from_WSG84(center_WSG84)
                else:
                    self.set_message("Adresse konnte nicht gefunden werden")
                    raise ValueError

            folium_map = folium.Map(location=[float(center_WSG84[0]), float(center_WSG84[1])], zoom_start=12)
            self.set_message("Schritt 1/" + str(steps) + " - Basiskarte erstellt")

            border = self.border(center_ETRS89e, center_WSG84, radius*10)
            border.add_to(folium_map)
            self.set_message("Schritt 2/" + str(steps) + " - Rahmen hinzugefügt")
            
            if bool(steps_cellular):
                cellular_layer_list = self.cellular(center_ETRS89e, radius*10, A1_5Gn78, Magenta_5Gn78, Drei_5Gn78, GrazHolding_5Gn78, Liwest_5Gn78, MassResponse_5Gn78, SalzburgAG_5Gn78, A1_Speedmap, Magenta_Speedmap, Drei_Speedmap, steps)
                if len(cellular_layer_list) > 0:
                    self.set_message("Schritt " + str(3 + steps_cellular) + "/" + str(steps) + " - Mobilfunk Schichten hinzufügen")
                    for map_layer in cellular_layer_list:
                        map_layer.add_to(folium_map)

            if fixed:
                self.set_message("Schritt " + str(3 + steps_cellular + int(bool(steps_cellular))) + "/" + str(steps) + " - Festnetz Schichten erstellen")
                fixed_layer_list = self.fixed(center_ETRS89e, radius*10)
                self.set_message("Schritt " + str(4 + steps_cellular + int(bool(steps_cellular))) + "/" + str(steps) + " - Festnetz Schichten hinzufügen")
                for map_layer in fixed_layer_list:
                    map_layer.add_to(folium_map)

            if grant:
                self.set_message("Schritt " + str(3 + steps_cellular + int(bool(steps_cellular)) + (fixed*2)) + "/" + str(steps) + " - Geförderter Ausbau erstellen")
                grant_layer = self.grant(center_ETRS89e, radius*10)
                self.set_message("Schritt " + str(4 + steps_cellular + int(bool(steps_cellular)) + (fixed*2)) + "/" + str(steps) + " - Geförderter Ausbau hinzufügen")
                grant_layer.add_to(folium_map)

            # Add a folium LayerControl to the map.
            #folium.LayerControl(position='topright', collapsed=True, autoZIndex=True).add_to(folium_map)
            folium.LayerControl(position='topright', collapsed=False, autoZIndex=True).add_to(folium_map)
            time.sleep(0.5)
            self.set_message("ODKT bereit (pywebview)")

            return folium_map.get_root().render()
        except ValueError:
            pass
    
    def check_if_ETRS89e(self, location:str) -> bool:
        """
        Function to check if the content of the location variable is an ETRS89e square-id

        Parameters:
            self
            location (str) : Location of the center of the map - this can be WSG84 coordinates, an ETRS89e square-id or address

        Returns:
            bool (bool) : Boolean value if the location variable is an ETRS89e square-id
        """
        return bool(re.match(r"\d{3}mN\d{5}E\d{5}$", location))
    
    def check_if_WSG84(self, location:str) -> bool:
        """
        Function to check if the content of the location variable is WSG84 coordinates 

        Parameters:
            self
            location (str) : Location of the center of the map - this can be WSG84 coordinates, an ETRS89e square-id or address

        Returns:
            bool (bool) : Boolean value if the location variable is WSG84 coordinates
        """
        return bool(re.match(r"\d{2}\.\d+\,\d{2}\.\d+$", location.replace(" ", "")))
    
    def convert_address_to_WSG84(self, location:str) -> str:
        """
        Function to convert a address with Nominatim to WSG84 coordinates 

        Parameters:
            self
            location (str) : Location of the center of the map as an address

        Returns:
            coordinates (str) : String representation of the coordinates - returns nothing if address not found
        """
        geolocator = Nominatim(user_agent="Open Data Map Tool - Cellular and Broadband Austria")
        location = geolocator.geocode(location)
        if location is not None:
            return str(location.latitude) + ", " + str(location.longitude)
        else:
            return ""
    
    def center_ETRS89e_from_string(self, location:str) -> tuple:
        """
        Function to convert an ETRS89e square-id into a tuple with just north and east variables 

        Parameters:
            self
            location (str) : Location of the center of the map as an ETRS89e square-id

        Returns:
            tuple (tuple) : Tuple with the north and east variables of an ETRS89e square-id
        """
        return tuple(int(entry) for entry in location.replace("100mN", "").split("E"))

    def center_WSG84_from_ETRS89e(self, location:tuple) -> tuple:
        """
        Function to convert an ETRS89e square-id tuple into a WSG84 coordinates tuple 

        Parameters:
            self
            location (tuple) : Location of the center of the map as an ETRS89e square-id as a tuple with north and east variables

        Returns:
            tuple (tuple) : Tuple with the WSG84 coordinates
        """
        return Transformer.from_crs(3035, 4326).transform((location[0] * 100), (location[1] * 100))
    
    def center_WSG84_from_string(self, location:str) -> tuple:
        """
        Function to convert WSG84 coordinates to a tuple 

        Parameters:
            self
            location (str) : Location of the center of the map as WSG84 coordinates

        Returns:
            tuple (tuple) : Tuple with the WSG84 coordinates
        """
        return tuple(float(entry) for entry in location.replace(" ", "").split(","))
    
    def center_ETRS89e_from_WSG84(self, location:tuple) -> tuple:
        """
        Function to convert a WSG84 coordinates tuple into an ETRS89e square-id tuple  

        Parameters:
            self
            location (tuple) : Location of the center of the map as a WSG84 coordinates tuple

        Returns:
            tuple (tuple) : Tuple with the ETRS89e square-id as a tuple with north and east variables
        """
        return tuple(int(entry/100) for entry in Transformer.from_crs(4326, 3035).transform(location[0], location[1]))
    
    def border(self, center_ETRS89e:tuple, center_WSG84:tuple, radius_hectometers:float) -> folium.Polygon:
        """
        Function to create the border polygon around the selected map area

        Parameters:
            self
            center_ETRS89e (tuple) : Location of the center of the map as an ETRS89e square-id as a tuple with north and east variables
            center_WSG84 (tuple) : Location of the center of the map as a WSG84 coordinates tuple
            radius_hectometers (float) : Radius around the center in hectometers

        Returns:
            border_polygon (folium.Polygon) : Border polygon
        """
        # The four transformations for the four corners of a square with a radius around the center square.
        border_lower_left_corner = Transformer.from_crs(3035, 4326).transform(((center_ETRS89e[0] - radius_hectometers) * 100), ((center_ETRS89e[1] - radius_hectometers) * 100))
        border_lower_right_corner = Transformer.from_crs(3035, 4326).transform(((center_ETRS89e[0] - radius_hectometers) * 100), ((center_ETRS89e[1] + radius_hectometers) * 100))
        border_top_right_corner = Transformer.from_crs(3035, 4326).transform(((center_ETRS89e[0] + radius_hectometers) * 100), ((center_ETRS89e[1] + radius_hectometers) * 100))
        border_top_left_corner = Transformer.from_crs(3035, 4326).transform(((center_ETRS89e[0] + radius_hectometers) * 100), ((center_ETRS89e[1] - radius_hectometers) * 100))

        # Configure the text for the tooltip of the square.
        radius_border_tooltip_text = "Rahmen für Zentrum 100mN" + str(center_ETRS89e[0]) + "E" + str(center_ETRS89e[1]) + " - " + str(center_WSG84[0]) + ", " + str(center_WSG84[1]) + " Radius: " + str(radius_hectometers/10) + " km"

        # Configure the popup of the square.
        radius_border_popup_text_string = self.border_popup_text_function(center_ETRS89e, center_WSG84, border_lower_left_corner, border_lower_right_corner, border_top_right_corner, border_top_left_corner, radius_hectometers/10)
        radius_border_popup_text = folium.Popup(radius_border_popup_text_string, max_width=len(str(center_WSG84[0]) + "," + str(center_WSG84[1])) * 25)

        # Create a polygon border around the center square and add it to the map.
        return folium.Polygon((border_lower_left_corner,border_lower_right_corner,border_top_right_corner,border_top_left_corner), popup=radius_border_popup_text, tooltip=radius_border_tooltip_text, color='#ff7800')
    
    def border_popup_text_function(self, center_ETRS89e:tuple, center_WSG84:tuple, lower_left_WSG84:tuple, lower_right_WSG84:tuple, top_right_WSG84:tuple, top_left_WSG84:tuple, radius:float) -> str:
        """
        Function to create the content of the border polygon popup from the provided variables

        Parameters:
            self
            center_ETRS89e (tuple) : Location of the center of the map as an ETRS89e square-id as a tuple with north and east variables
            center_WSG84 (tuple) : Location of the center of the map as a WSG84 coordinates tuple
            lower_left_WSG84 (tuple) : Location of the lower left corner of the map as aWSG84 coordinates tuple
            lower_right_WSG84 (tuple) : Location of the lower right corner of the map as a WSG84 coordinate tuple
            top_right_WSG84 (tuple) : Location of the top right corner of the map as a WSG84 coordinates tuple
            top_left_WSG84 (tuple) : Location of the top left corner of the map as a WSG84 coordinates tuple
            radius (float) : Radius around the center in kilometers

        Returns:
            border_popup (str) : Border popup content in html format
        """
        text = ("<table class=\"tbl\"><tr><td class=\"lls\">Zentrum:</td><td class=\"rls\">{}</td></tr><tr><td>Zentrum (lat & lon):</td><td>{}</td></tr><tr><td>Unten Links (lat & lon):</td><td>{}</td></tr><tr><td>Unten Rechts (lat & lon):</td><td>{}</td></tr><tr><td>Oben Rechts (lat & lon):</td><td>{}</td></tr><tr><td>Oben Links (lat & lon):</td><td>{}</td></tr><tr><td>Radius:</td><td>{}</td></tr></table>")\
            .format("100mN" + str(center_ETRS89e[0]) + "E" + str(center_ETRS89e[1]), str(center_WSG84[0]) + "," + str(center_WSG84[1]), str(lower_left_WSG84[0]) + "," + str(lower_left_WSG84[1]), str(lower_right_WSG84[0]) + "," + str(lower_right_WSG84[1]), str(top_right_WSG84[0]) + "," + str(top_right_WSG84[1]), str(top_left_WSG84[0]) + "," + str(top_left_WSG84[1]), str(radius)+" km")
        return text
    
    def cellular(self, center_ETRS89e:tuple, radius_hectometers:float, A1_5Gn78:bool, Magenta_5Gn78:bool, Drei_5Gn78:bool, GrazHolding_5Gn78:bool, Liwest_5Gn78:bool, MassResponse_5Gn78:bool, SalzburgAG_5Gn78:bool, A1_Speedmap:bool, Magenta_Speedmap:bool, Drei_Speedmap:bool, steps:int) -> list:
        """
        Function to create the cellular layers in the selected map area

        Parameters:
            self
            center_ETRS89e (tuple) : Location of the center of the map as an ETRS89e square-id as a tuple with north and east variables
            radius_hectometers (float) : Radius around the center in hectometers
            A1_5Gn78 (bool) : Boolean for the A1 5G n78 layer
            Magenta_5Gn78 (bool) : Boolean for the Magenta 5G n78 layer
            Drei_5Gn78 (bool) : Boolean for the Drei 5G n78 layer
            GrazHolding_5Gn78 (bool) : Boolean for the Graz Holding 5G n78 layer
            Liwest_5Gn78 (bool) : Boolean for the Liwest 5G n78 layer
            MassResponse_5Gn78 (bool) : Boolean for the MassResponse 5G n78 layer
            SalzburgAG_5Gn78 (bool) : Boolean for the Salzburg AG 5G n78 layer
            A1_Speedmap (bool) : Boolean for the A1 Speedmap layer
            Magenta_Speedmap (bool) : Boolean for the Magenta Speedmap layer
            Drei_Speedmap (bool) : Boolean for the Drei Speedmap layer
            steps (int) : Number of steps to create the map in total

        Returns:
            layer_list (list) : List of map layers
        """
        step_counter = 2
        layer_list = []
        if A1_5Gn78 == True:
            step_counter+=1
            self.set_message("Schritt " + str(step_counter) + "/" + str(steps) + " - A1 5G n78")
            layer_list.append(self.cellular_network("A1", "5G n78", "3.500", "1", "NR", "A1_3500", center_ETRS89e, radius_hectometers, ["#ee8ea7", "#e66686", "#ff2f2b", "#940a03"]))
        if Magenta_5Gn78 == True:
            step_counter+=1
            self.set_message("Schritt " + str(step_counter) + "/" + str(steps) + " - Magenta 5G n78")
            layer_list.append(self.cellular_network("Magenta", "5G n78", "3.500", "3", "LTE", "Magenta_3500", center_ETRS89e, radius_hectometers, ["#ffc1e1", "#ff79be", "#e20075", "#9d0054"]))
        if Drei_5Gn78 == True:
            step_counter+=1
            self.set_message("Schritt " + str(step_counter) + "/" + str(steps) + " - Drei 5G n78")
            layer_list.append(self.cellular_network("Drei", "5G n78", "3.500", "5", "NR", "Drei_3500", center_ETRS89e, radius_hectometers, ["#ffba8c", "#ff7d27", "#ea5e00", "#953c00"]))
        if GrazHolding_5Gn78 == True:
            step_counter+=1
            self.set_message("Schritt " + str(step_counter) + "/" + str(steps) + " - Graz Holding 5G n78")
            layer_list.append(self.cellular_network("Graz Holding Citycom", "5G n78", "3.500", "25", "NR", "Citycom_3500", center_ETRS89e, radius_hectometers, ["#99d8ea", "#8f92be", "#00a2e8", "#3f48cc"]))
        if Liwest_5Gn78 == True:
            step_counter+=1
            self.set_message("Schritt " + str(step_counter) + "/" + str(steps) + " - Liwest 5G n78")
            layer_list.append(self.cellular_network("Liwest", "5G n78", "3.500", "26", "NR", "Liwest_3500", center_ETRS89e, radius_hectometers, ["#99d8ea", "#8f92be", "#00a2e8", "#3f48cc"]))
        if MassResponse_5Gn78 == True:
            step_counter+=1
            self.set_message("Schritt " + str(step_counter) + "/" + str(steps) + " - Mass Response 5G n78")
            layer_list.append(self.cellular_network("Mass Response", "5G n78", "3.500", "17", "NR", "Spusu_3500", center_ETRS89e, radius_hectometers, ["#8eeaaa", "#95d600", "#22b14d", "#00605b"]))
        if SalzburgAG_5Gn78 == True:
            step_counter+=1
            self.set_message("Schritt " + str(step_counter) + "/" + str(steps) + " - Salzburg AG 5G n78")
            layer_list.append(self.cellular_network("Salzburg AG", "5G n78", "3.500", "17", "NR", "CableLinkAir_3500", center_ETRS89e, radius_hectometers, ["#c8c2cf", "#a69cb1", "#7b6d8b", "#484051"]))
        if A1_Speedmap == True:
            step_counter+=1
            self.set_message("Schritt " + str(step_counter) + "/" + str(steps) + " - A1 Speedmap")
            layer_list.append(self.cellular_network("A1", "Speedmap", "800/900/1500/1800/2100/2600/3600", "1", "NR", "A1_Speedmap", center_ETRS89e, radius_hectometers, ["#ee8ea7", "#e66686", "#ff2f2b", "#940a03"]))
        if Magenta_Speedmap == True:
            step_counter+=1
            self.set_message("Schritt " + str(step_counter) + "/" + str(steps) + " - Magenta Speedmap")
            layer_list.append(self.cellular_network("Magenta", "Speedmap", "700/800/900/1500/1800/2100/2600/3600", "3", "LTE", "Magenta_Speedmap", center_ETRS89e, radius_hectometers, ["#ffc1e1", "#ff79be", "#e20075", "#9d0054"]))
        if Drei_Speedmap == True:
            step_counter+=1
            self.set_message("Schritt " + str(step_counter) + "/" + str(steps) + " - Drei Speedmap")
            layer_list.append(self.cellular_network("Drei", "Speedmap", "700/900/1500/1800/2100/2600/3600", "5", "NR", "Drei_Speedmap", center_ETRS89e, radius_hectometers, ["#ffba8c", "#ff7d27", "#ea5e00", "#953c00"]))
        return layer_list

    def cellular_network(self, operator:str, layer_type:str, network_frequency:str, cellmapper_mnc:str, cellmapper_network_technology:str, table_name:str, center_ETRS89e:tuple, radius_hectometers:float, colors:list) -> folium.FeatureGroup:
        """
        Function to create a cellular layer in the selected map area

        Parameters:
            self
            operator (str) : Name of the cellular network operator
            layer_type (str) : Layer type string
            network_frequency (str) : Frequency for the open data of this layer
            cellmapper_mnc (str) : MNC of this layer for the cellmapper link
            cellmapper_network_technology (str) : Network technology for the cellmapper link
            table_name (str) : Name of the table in which the data for the current layer is stored
            center_ETRS89e (tuple) : Location of the center of the map as an ETRS89e square-id as a tuple with north and east variables
            radius_hectometers (float) : Radius around the center in hectometers
            colors (list) : List of colors in hex for the different speed tiers

        Returns:
            map_layer (folium.FeatureGroup) : Map layer
        """
        # Create a new SQLite connection
        sqlite3_database_connection = sqlite3.connect('map_data.db')
        # Set uo the transformer from EPSG:3035 (ETRS89e) aka LAEA Europe to EPSG:4326 (WSG84) aka GPS coordinates
        transform_from_ETRS89e_to_WSG84 = Transformer.from_crs(3035, 4326)
        # Create the folium map layer for the current cellular operator
        map_layer = folium.FeatureGroup(name=operator + " " + layer_type, show=False)
        # Configure the query to get the squares of the current cellular operator in the selected area from the SQLite database
        query = 'SELECT * FROM {} WHERE DL_NORMAL > 0 AND UL_NORMAL > 0 AND DL_MAX > 0 AND UL_MAX > 0 AND NORTH BETWEEN {} AND {} AND EAST BETWEEN {} AND {}'.\
            format(table_name, center_ETRS89e[0] - radius_hectometers, center_ETRS89e[0] + radius_hectometers - 1, center_ETRS89e[1] - radius_hectometers, center_ETRS89e[1] + radius_hectometers - 1)
        # Get all the squares for the current cellular operator in the selected area from the database and save them in a pandas dataframe
        dataframe_square = pd.read_sql_query(query, sqlite3_database_connection)
        # Get the 25th percentile value of the normal downlink datarate
        twentyfive = round(dataframe_square['DL_NORMAL'].quantile(0.25),2)
        # Get the median value of the normal downlink datarate
        median = round(dataframe_square['DL_NORMAL'].quantile(0.50),2)
        # Get the 75th percentile value of the normal downlink datarate
        seventyfive = round(dataframe_square['DL_NORMAL'].quantile(0.75),2)
        # Iterate through the rows of the dataframe
        for index, row in dataframe_square.iterrows():
            # The four transformations for the four corners of the square
            square_lower_left_corner = transform_from_ETRS89e_to_WSG84.transform(row.NORTH * 100, row.EAST * 100)
            square_lower_right_corner = transform_from_ETRS89e_to_WSG84.transform(row.NORTH * 100, (row.EAST + 1) * 100)
            square_top_right_corner = transform_from_ETRS89e_to_WSG84.transform((row.NORTH + 1) * 100, (row.EAST + 1) *100)
            square_top_left_corner = transform_from_ETRS89e_to_WSG84.transform((row.NORTH + 1) * 100, row.EAST * 100)
            # The transformation for the center of the square
            square_center = transform_from_ETRS89e_to_WSG84.transform(((row.NORTH + 0.5) * 100), ((row.EAST + 0.5) * 100))
            # Configure the text for the tooltip of the square
            current_square_tooltip_text = operator + " " + layer_type + " AVG Download: " + self.number_formatter(row.DL_NORMAL) + " Mbit/s"
            # Configure the popup of the square
            current_square_popup_text_string = self.cellular_popup_text_function('100mN' + str(row.NORTH) + 'E' + str(row.EAST), operator, network_frequency + " MHz", layer_type, self.number_formatter(row.DL_NORMAL), self.number_formatter(row.UL_NORMAL), self.number_formatter(row.DL_MAX), self.number_formatter(row.UL_MAX), row.RFC_DATE, square_center[0], square_center[1], cellmapper_mnc, cellmapper_network_technology)
            current_square_popup_text = folium.Popup(current_square_popup_text_string, max_width=450)
            # Create the square as a folium polygon and add it to the current operators layer. 
            folium.Polygon(locations=(square_lower_left_corner, square_lower_right_corner, square_top_right_corner, square_top_left_corner), popup=current_square_popup_text, tooltip=current_square_tooltip_text, color=self.cellular_bandwidth_color(row.DL_NORMAL, twentyfive, median, seventyfive, colors), fill=True).add_to(map_layer)
        
        print(operator + " " + layer_type + ": " + str(len(dataframe_square)) + " squares with coverage found\n")
        # Return the finished map layer
        return map_layer

    def cellular_bandwidth_color(self, download:float, twentyfive:float, median:float, seventyfive:float, colors:list) -> str:
        """
        Function to get the color for the average download bandwidth

        Parameters:
            self
            download (float) : Average download for a square
            twentyfive (float) : Twenty-fifth percentile for the average bandwidth of the current map
            median (float) : Fiftieth percentile for the average bandwidth of the current map
            seventyfive (float) : Seventy-fifth percentile for the average bandwidth of the current map
            colors (str) : List of colors in hex for the different speed tiers

        Returns:
            color_in_hex (str) : Color for the square in hex
        """
        color_in_hex = ''
        # Select the color of the square based on the average bandwidth.
        if (download < twentyfive):
            color_in_hex = colors[0]
        elif (download < median):
            color_in_hex = colors[1]
        elif (download < seventyfive):
            color_in_hex = colors[2]
        else:
            color_in_hex = colors[3]
        return color_in_hex

    def cellular_popup_text_function(self, raster_id:str, operator:str, network_frequency:str, layer_type:str, average_download:str, average_upload:str, maximum_download:str, maximum_upload:str, date:str, lat:float, lon:float, cellmapper_mnc:str, cellmapper_network_technology:str) -> str:
        """
        Function to create the content of the cellular polygon popup from the provided variables

        Parameters:
            self
            raster_id (str) : ETRS89e square-id as a string
            operator (str) : Name of the cellular network operator
            network_frequency (str) : Frequency for the open data of this layer
            layer_type (str) : Layer type string
            average_download (str) : Average download for the current square
            average_upload (str) : Average upload for the current square
            maximum_download (str) : Maximum download for the current square
            maximum_upload (str) : Maximum upload for the current square
            date (str) : Date when the data was generated
            lat (float) : Latitude of the center of the square
            lon (float) : Longitude of the center of the square
            cellmapper_mnc (str) : MNC of this layer for the cellmapper link
            cellmapper_network_technology (str) : Network technology for the cellmapper link

        Returns:
            cellular_popup (str) : Cellular square popup content in html format
        """
        return ("<table class=\"tbl\">"
        "<tr>"
        "<td class=\"lls\">Raster ID:</td>"
        "<td class=\"rls\">{}</td>"
        "</tr>"
        "<tr>"
        "<td>Anbieter:</td>"
        "<td>{}</td>"
        "</tr>"
        "<tr>"
        "<td>Frequenz:</td>"
        "<td>{}</td>"
        "</tr>"
        "<tr>"
        "<td>Technologie:</td>"
        "<td>{}</td>"
        "</tr>"
        "<tr>"
        "<td>AVG Download:</td>"
        "<td>{} Mbit/s</td>"
        "</tr>"
        "<tr>"
        "<td>AVG Upload:</td>"
        "<td>{} Mbit/s</td>"
        "</tr>"
        "<tr>"
        "<td>Max Download:</td>"
        "<td>{} Mbit/s</td>"
        "</tr>"
        "<tr>"
        "<td>Max Upload:</td>"
        "<td>{} Mbit/s</td>"
        "</tr>"
        "<tr>"
        "<td>Datum:</td>"
        "<td>{}</td>"
        "</tr>"
        "<tr>"
        "<td>Google Maps:</td>"
        "<td><a href=\"https://www.google.com/maps/search/{},+{}\" target=\"_blank\">auf Google Maps ansehen</a></td>"
        "</tr>"
        "<tr>"
        "<td>Breitbandatlas:</td>"
        "<td><a href=\"https://breitbandatlas.gv.at/{}/{}/Mobilfunknetz/{}\" target=\"_blank\">im Breitbandatlas ansehen</a></td>"
        "</tr>"
        "<tr>"
        "<td>Cellmapper:</td>"
        "<td><a href=\"https://www.cellmapper.net/map?MCC=232&MNC={}&type={}&latitude={}&longitude={}&zoom=15.3\" target=\"_blank\">auf Cellmapper ansehen</a></td>"
        "</tr>"
        "</table>").format(raster_id, operator, network_frequency, layer_type, average_download, average_upload, maximum_download, maximum_upload, date, lat, lon, lat, lon, operator, cellmapper_mnc, cellmapper_network_technology, lat, lon)
    
    def fixed(self, center_ETRS89e:tuple, radius_hectometers:float) -> list:
        """
        Function to create the fixed broadband layers in the selected map area

        Parameters:
            self
            center_ETRS89e (tuple) : Location of the center of the map as an ETRS89e square-id as a tuple with north and east variables
            radius_hectometers (float) : Radius around the center in hectometers

        Returns:
            fixed_layer_list (list) : Fixed broadband layer list
        """
        # Create a new SQLite connection
        sqlite3_database_connection = sqlite3.connect('map_data.db')
        # Set uo the transformer from EPSG:3035 (ETRS89e) aka LAEA Europe to EPSG:4326 (WSG84) aka GPS coordinates
        transform_from_ETRS89e_to_WSG84 = Transformer.from_crs(3035, 4326)
        # List of fixed network map layers
        fixed_layer_list = []
        # Configure the query to get the fixed broadband operators in the selected area from the SQLite database
        query_operators = 'SELECT DISTINCT INFRASTRUKTURANBIETER FROM Festnetz WHERE NORTH BETWEEN {} AND {} AND EAST BETWEEN {} AND {}'.\
            format(center_ETRS89e[0] - radius_hectometers, center_ETRS89e[0] + radius_hectometers - 1, center_ETRS89e[1] - radius_hectometers, center_ETRS89e[1] + radius_hectometers - 1)
        # Get the fixed broadband operators in the selected area from the database and save them in a pandas dataframe
        dataframe_operators = pd.read_sql_query(query_operators, sqlite3_database_connection)
        # Iterate through the rows of the dataframe
        for index, row_operator in dataframe_operators.iterrows():            
            # Create the folium map layer for the current fixed broadband provider
            map_layer = folium.FeatureGroup(name = row_operator.INFRASTRUKTURANBIETER, show = False)
            # Configure the query to get all the squares for the current fixed broadband operator in the selected area from the SQLite database
            query_square = 'SELECT * FROM Festnetz WHERE INFRASTRUKTURANBIETER = \'{}\' AND NORTH BETWEEN {} AND {} AND EAST BETWEEN {} AND {}'.\
                format(row_operator.INFRASTRUKTURANBIETER, center_ETRS89e[0] - radius_hectometers, center_ETRS89e[0] + radius_hectometers - 1, center_ETRS89e[1] - radius_hectometers, center_ETRS89e[1] + radius_hectometers - 1)
            # Get all the squares for the current fixed broadband operator in the selected area from the database and save them in a pandas dataframe
            dataframe_square = pd.read_sql_query(query_square, sqlite3_database_connection)
            # Iterate through the rows of the dataframe
            for index, row_square in dataframe_square.iterrows():
                # The four transformations for the four corners of the square
                coordinates_of_square_lower_left_corner = transform_from_ETRS89e_to_WSG84.transform(row_square.NORTH * 100, row_square.EAST * 100)
                coordinates_of_square_lower_right_corner = transform_from_ETRS89e_to_WSG84.transform(row_square.NORTH * 100, (row_square.EAST + 1) * 100)
                coordinates_of_square_top_right_corner = transform_from_ETRS89e_to_WSG84.transform((row_square.NORTH + 1) * 100, (row_square.EAST + 1) * 100)
                coordinates_of_square_top_left_corner = transform_from_ETRS89e_to_WSG84.transform((row_square.NORTH + 1) * 100, row_square.EAST * 100)
                # The transformation for the center of the square
                coordinates_of_square_center = transform_from_ETRS89e_to_WSG84.transform((row_square.NORTH + 0.5) * 100, (row_square.EAST + 0.5) * 100)
                # Use the fixed_fix_A1 function to correct bandwidth data for A1 xDSL to be more representative of what actual individual customers can get
                download_upload = self.fixed_fix_A1(row_square.INFRASTRUKTURANBIETER, row_square.TECHNIK, row_square.DOWNLOAD, row_square.UPLOAD)
                # Configure the text for the tooltip of the square
                current_square_tooltip_text = row_square.INFRASTRUKTURANBIETER + " " + row_square.TECHNIK + " Download: " + str(download_upload[0]) + " Mbit/s"
                # Configure the popup of the square
                current_square_popup_text_string = self.fixed_popup_text_function("100mN" + str(row_square.NORTH) + "E" + str(row_square.EAST), row_square.INFRASTRUKTURANBIETER, row_square.TECHNIK, self.number_formatter(download_upload[0]), self.number_formatter(download_upload[1]), self.number_formatter(download_upload[0]/download_upload[1]), row_square.BEARBEITUNG_BBA, coordinates_of_square_center[0], coordinates_of_square_center[1])
                current_square_popup_text = folium.Popup(current_square_popup_text_string, max_width=500)
                # Create the square as a folium polygon and add it to the current operator layer
                folium.Polygon((coordinates_of_square_lower_left_corner, coordinates_of_square_lower_right_corner, coordinates_of_square_top_right_corner, coordinates_of_square_top_left_corner), current_square_popup_text, current_square_tooltip_text, color=self.fixed_bandwidth_color(row_square.DOWNLOAD), fill=True).add_to(map_layer)
            # Append the finished map layer to the layer list
            fixed_layer_list.append(map_layer)
            # Print how many squares were found from this broadband provider in selected area
            self.set_message(row_operator.INFRASTRUKTURANBIETER + ": " + str(len(dataframe_square)) + " Quadrate gefunden")
        # Return the finished map layer list
        return fixed_layer_list
    
    def fixed_fix_A1(self, operator:str, technology:str, download:float, upload:float) -> list:
        """
        Function to correct the bandwidth data when the operator is A1 and the technology is xDSL

        Parameters:
            self
            operator (str) : Name of the fixed broadband network operator
            technology (str) : Technology used by the fixed broadband network operator in this square
            download (float) : Download bandwidth for the fixed broadband network operator in this square
            upload (float) : Upload bandwidth for the fixed broadband network operator in this square

        Returns:
            updated_bandwidth (list) : List with the updated download and upload bandwidth
        """
        if operator == "A1" and technology == "xDSL":
            download = round(download*0.5, 2)
            upload = round(upload*0.5, 2)
        return [download, upload]
    
    def fixed_bandwidth_color(self, download:float):
        """
        Function to get the color for the average download bandwidth

        Parameters:
            self
            download (float) : Average download for a square

        Returns:
            color_in_hex (str) : Color for the square in hex
        """
        color_in_hex = ''
        # Select the color of the square based on the bandwidth
        if (download < 15):
            color_in_hex = "#73ffef"
        elif (download < 50):
            color_in_hex = "#33c4b3"
        elif (download < 200):
            color_in_hex = "#3e9c91"
        elif (download < 999):
            color_in_hex = "#1f6e64"
        else:
            color_in_hex = "#143834"
        return color_in_hex

    def fixed_popup_text_function(self, raster_id:str, operator:str, technology:str, download_speed:str, upload_speed:str, download_upload_ratio:str, date:str, lat:float, lon:float) -> str:
        """
        Function to create the content of the fixed broadband polygon popup from the provided variables

        Parameters:
            self
            raster_id (str) : ETRS89e square-id as a string
            operator (str) : Name of the cellular network operator
            technology (str) : Technology used in this square
            download_speed (str) : Average download for the current square
            upload_speed (str) : Average upload for the current square
            download_upload_ratio (str) : Maximum download for the current square
            date (str) : Date when the data was generated
            lat (float) : Latitude of the center of the square
            lon (float) : Longitude of the center of the square

        Returns:
            fixed_broadband_popup (str) : Fixed broadband square popup content in html format
        """
        return ("<table class=\"tbl\">"
        "<tr>"
        "<td class=\"lls\">Raster ID:</td>"
        "<td class=\"rls\">{}</td>"
        "</tr>"
        "<tr>"
        "<td>Anbieter:</td>"
        "<td>{}</td>"
        "</tr>"
        "<tr>"
        "<td>Technologie:</td>"
        "<td>{}</td>"
        "</tr>"
        "<tr>"
        "<td>Download:</td>"
        "<td>{} Mbit/s</td>"
        "</tr>"
        "<tr>"
        "<td>Upload:</td>"
        "<td>{} Mbit/s</td>"
        "</tr>"
        "<tr>"
        "<td>Download-Upload Verhältnis:</td>"
        "<td>{}:1</td>"
        "</tr>"
        "<tr>"
        "<td>Zuletzt bearbeitet:</td>"
        "<td>{}</td>"
        "</tr>"
        "<tr>"
        "<td>Google Maps:</td>"
        "<td><a href=\"https://www.google.com/maps/search/{},+{}\" target=\"_blank\">auf Google Maps ansehen</a></td>"
        "</tr>"
        "<tr>"
        "<td>Breitbandatlas:</td>"
        "<td><a href=\"https://breitbandatlas.gv.at/{}/{}/Festnetz/\" target=\"_blank\">im Breitbandatlas ansehen</a></td>"
        "</tr>"
        "</table>").format(raster_id, operator, technology, download_speed, upload_speed, download_upload_ratio, date, lat, lon, lat, lon)
    
    def grant(self, center_ETRS89e:tuple, radius_hectometers:float) -> folium.FeatureGroup:
        """
        Function to create the broadband grant layer in the selected map area

        Parameters:
            self
            center_ETRS89e (tuple) : Location of the center of the map as an ETRS89e square-id as a tuple with north and east variables
            radius_hectometers (float) : Radius around the center in hectometers

        Returns:
            map_layer (folium.FeatureGroup) : Broadband grant layer
        """
        # Create a new SQLite connection
        sqlite3_database_connection = sqlite3.connect('map_data.db')
        # Set uo the transformer from EPSG:3035 (ETRS89e) aka LAEA Europe to EPSG:4326 (WSG84) aka GPS coordinates
        transform_from_ETRS89e_to_WSG84 = Transformer.from_crs(3035, 4326)
        # Create the folium map layer for the government supported broadband rollout
        map_layer = folium.FeatureGroup(name = "Geförderter Ausbau", show=False)
        # Configure the query to get all the squares for the government supported broadband in the selected area from the SQLite database

        query_square = 'WITH Gruppierte_BBA_Projekte AS (SELECT ANTRAGSNUMMER, AUSSCHREIBUNG, FOERDERNEHMER, PROJEKTTITEL, SUM(PROJEKTKOSTEN_EURO) AS PROJEKTKOSTEN_EURO, SUM(FOERDERBETRAG_EURO) AS FOERDERBETRAG_EURO, SUM(FOERDERBETRAG_LAND_ANSCHLUSSFOERDERUNG_EURO) AS FOERDERBETRAG_LAND_ANSCHLUSSFOERDERUNG_EURO, AVG(FOERDERSATZ_PROZENT) AS FOERDERSATZ_PROZENT, TAG_DER_GEWAEHRUNG_DATUM, VERTRAGSABSCHLUSS_DATUM, PROJEKTENDE_DATUM, SUM(FOERDERBARE_KOSTEN_NACH_ENDPRUEFUNG_EURO) AS FOERDERBARE_KOSTEN_NACH_ENDPRUEFUNG_EURO, SUM(FOERDERBETRAG_NACH_ENDPRUEFUNG_EURO) AS FOERDERBETRAG_NACH_ENDPRUEFUNG_EURO, PROJEKTSTATUS FROM BBA_Projekte GROUP BY ANTRAGSNUMMER) SELECT ag.NORTH, ag.EAST,ag.TECHNIK, BEARBEITUNG_BBA , gbp.* FROM Gefoerderter_Ausbau AS ag INNER JOIN Gruppierte_BBA_Projekte AS gbp ON ag.ANTRAGSNUMMER = gbp.ANTRAGSNUMMER WHERE ag.NORTH BETWEEN {} AND {} AND ag.EAST BETWEEN {} AND {};'.\
            format(center_ETRS89e[0] - radius_hectometers, center_ETRS89e[0] + radius_hectometers - 1, center_ETRS89e[1] - radius_hectometers, center_ETRS89e[1] + radius_hectometers - 1)
        # Get all the squares for government supported broadband in the selected area from the database and save them in a pandas dataframe
        dataframe_squares = pd.read_sql_query(query_square, sqlite3_database_connection)
        # Iterate through the rows of the dataframe
        for index, row_square in dataframe_squares.iterrows():
            # The four transformations for the four corners of the square
            coordinates_of_square_lower_left_corner = transform_from_ETRS89e_to_WSG84.transform(row_square.NORTH * 100, row_square.EAST * 100)
            coordinates_of_square_lower_right_corner = transform_from_ETRS89e_to_WSG84.transform(row_square.NORTH * 100, (row_square.EAST + 1) * 100)
            coordinates_of_square_top_right_corner = transform_from_ETRS89e_to_WSG84.transform((row_square.NORTH + 1) * 100, (row_square.EAST + 1) * 100)
            coordinates_of_square_top_left_corner = transform_from_ETRS89e_to_WSG84.transform((row_square.NORTH + 1) * 100, row_square.EAST * 100)
            # The transformation for the center of the square
            coordinates_of_square_center = transform_from_ETRS89e_to_WSG84.transform((row_square.NORTH + 0.5) * 100, (row_square.EAST + 0.5) * 100)
            # Configure the text for the tooltip of the square
            current_square_tooltip_text = row_square.FOERDERNEHMER + " sollte das Projekt " + row_square.PROJEKTTITEL + " bis " + row_square.PROJEKTENDE_DATUM + " abschließen"
            # Configure the popup of the square
            current_square_popup_text_string = self.grant_popup_text_function('100mN'+str(row_square.NORTH)+'E'+str(row_square.EAST), row_square.ANTRAGSNUMMER, row_square.AUSSCHREIBUNG, row_square.FOERDERNEHMER, row_square.PROJEKTTITEL, row_square.TECHNIK, self.number_formatter(row_square.PROJEKTKOSTEN_EURO), self.number_formatter(row_square.FOERDERBETRAG_EURO), self.number_formatter(row_square.FOERDERSATZ_PROZENT), self.number_formatter(row_square.FOERDERBETRAG_LAND_ANSCHLUSSFOERDERUNG_EURO), row_square.TAG_DER_GEWAEHRUNG_DATUM, row_square.VERTRAGSABSCHLUSS_DATUM, row_square.PROJEKTENDE_DATUM, self.number_formatter(row_square.FOERDERBARE_KOSTEN_NACH_ENDPRUEFUNG_EURO), self.number_formatter(row_square.FOERDERBETRAG_NACH_ENDPRUEFUNG_EURO), row_square.PROJEKTSTATUS, row_square.BEARBEITUNG_BBA, coordinates_of_square_center[0], coordinates_of_square_center[1])
            current_square_popup_text = folium.Popup(current_square_popup_text_string, max_width=len(row_square.PROJEKTTITEL) * 25)
            # Create the square as a folium polygon and add it to the current operators layer
            folium.Polygon((coordinates_of_square_lower_left_corner, coordinates_of_square_lower_right_corner, coordinates_of_square_top_right_corner, coordinates_of_square_top_left_corner), current_square_popup_text, current_square_tooltip_text, color="#6b798f", fill=True).add_to(map_layer)        
        # Print how many squares of government supported broadband rollout were found in the square
        print(str(len(dataframe_squares)) + " squares with government supported broadband rollout found\n")
        return map_layer
    
    def number_formatter(self, number):
        return "{:,}".format(int(float(number))).replace(',', '.') + "," + str(f"{(float(number)):.2f}").split(".")[1]

    def grant_popup_text_function(self, raster_id:str, antrangsnummer:int, ausschreibung:str, fördernehmer:str, projekttitel:str, technik:str, projektkosten:float, förderbetrag:float, fördersatz:float, förderbetrag_land:float, tag_gewährung:str, tag_vertragsabschluss:str, tag_projektende:str, förderbar_nach_prüfung:float, förderung_nach_prüfung:float, projektstatus:str, tag_bearbeitung:str, lat:float, lon:float) -> str:
        """
        Function to create the content of the fixed broadband polygon popup from the provided variables

        Parameters:
            self
            raster_id (str) : ETRS89e square-id as a string
            antrangsnummer (int) : 
            ausschreibung (str) : 
            fördernehmer (str) : 
            projekttitel (str) : 
            technik (str) : 
            projektkosten (float) : 
            förderbetrag (float) : 
            fördersatz (float) : 
            förderbetrag_land (float) : 
            tag_gewährung (str) :
            tag_vertragsabschluss (str) :
            tag_projektende (str) :
            förderbar_nach_prüfung (float) :
            förderung_nach_prüfung (float) :
            projektstatus (str) :
            tag_bearbeitung (str) : 
            lat (float) : Latitude of the center of the square
            lon (float) : Longitude of the center of the square
            
        Returns:
            fixed_broadband_popup (str) : Fixed broadband square popup content in html format
        """
        return ("<table class=\"tbl\">"
        "<tr>"
        "<td class=\"lls\">Raster ID:</td>"
        "<td class=\"rls\">{}</td>"
        "</tr>"
        "<tr>"
        "<td>Antragsnummer:</td>"
        "<td>{}</td>"
        "</tr>"
        "<tr>"
        "<td>Ausschreibung:</td>"
        "<td>{}</td>"
        "</tr>"
        "<tr>"
        "<td>Fördernehmer:</td>"
        "<td>{}</td>"
        "</tr>"
        "<tr>"
        "<td>Projekttitel:</td>"
        "<td>{}</td>"
        "</tr>"
        "<tr>"
        "<td>Technik:</td>"
        "<td>{}</td>"
        "</tr>"
        "<tr>"
        "<td>Projektkosten:</td>"
        "<td>{} €</td>"
        "</tr>"
        "<tr>"
        "<td>Förderbetrag:</td>"
        "<td>{} €</td>"
        "</tr>"
        "<tr>"
        "<td>Fördersatz:</td>"
        "<td>{} %</td>"
        "</tr>"
        "<tr>"
        "<td>Förderbetrag Land Anschlussförderung:</td>"
        "<td>{} €</td>"
        "</tr>"
        "<tr>"
        "<td>Tag der Genehmigung:</td>"
        "<td>{}</td>"
        "</tr>"
        "<tr>"
        "<td>Tag des Vertragsabschluss:</td>"
        "<td>{}</td>"
        "</tr>"
        "<tr>"
        "<td>Projektende:</td>"
        "<td>{}</td>"
        "</tr>"
        "<tr>"
        "<td>Förderbar nach Prüfung:</td>"
        "<td>{} €</td>"
        "</tr>"
        "<tr>"
        "<td>Förderung nach Prüfung:</td>"
        "<td>{} €</td>"
        "</tr>"
        "<tr>"
        "<td>Projektstatus:</td>"
        "<td>{}</td>"
        "</tr>"
        "<tr>"
        "<td>Zuletzt bearbeitet:</td>"
        "<td>{}</td>"
        "</tr>"
        "<tr>"
        "<td>Google Maps:</td>"
        "<td><a href=\"https://www.google.com/maps/search/{},+{}\" target=\"_blank\">auf Google Maps ansehen</a></td>"
        "</tr>"
        "<tr>"
        "<td>Breitbandatlas:</td>"
        "<td><a href=\"https://breitbandatlas.gv.at/{}/{}/Geförderter%20Ausbau/\" target=\"_blank\">im Breitbandatlas ansehen</a></td>"
        "</tr>"
        "</table>").format(raster_id, antrangsnummer, ausschreibung, fördernehmer, projekttitel, technik, projektkosten, förderbetrag, fördersatz, förderbetrag_land, tag_gewährung, tag_vertragsabschluss, tag_projektende, förderbar_nach_prüfung, förderung_nach_prüfung, projektstatus, tag_bearbeitung, lat, lon, lat, lon)
    
class Api:
    content = Content()
    folium_map = Map()
    html = None
    
    def init(self):
        return {"message" : "ODKT bereit (pywebview)"}

    def generateMap(self, radius, location, A1_5Gn78, Magenta_5Gn78, Drei_5Gn78, GrazHolding_5Gn78, Liwest_5Gn78, MassResponse_5Gn78, SalzburgAG_5Gn78, A1_Speedmap, Magenta_Speedmap, Drei_Speedmap, Festnetz, GeförderterAusbau):
        self.html = self.folium_map.create(location, float(str(radius).replace(",",".")), A1_5Gn78, Magenta_5Gn78, Drei_5Gn78, GrazHolding_5Gn78, Liwest_5Gn78, MassResponse_5Gn78, SalzburgAG_5Gn78, A1_Speedmap, Magenta_Speedmap, Drei_Speedmap, Festnetz, GeförderterAusbau)
        if self.html != None:
            self.html = self.html.replace("font-size: 1rem;", "font-size: 1.5rem;")
            html_copy = self.html.replace("</style>", "#back-input{position:absolute;bottom:10px;left:10px;padding:10px;width:95px;z-index:400;background-color:#5FA6AA;color:white;}#save-input{position: absolute;bottom: 10px;left: 115px;padding: 10px;z-index: 400;background-color: #5FA6AA;color: white;}#back-input:hover, #save-input:hover {background-color: #0299a3;color: white;border: 3px solid #0299a3;}.input-field {font-size: 1.5em;border-radius: 10px;background-color: #E8FEFF;padding-left: 1%;border: 3px solid #5FA6AA;}</style>")
            html_copy = html_copy.replace("</body>", "<button class=\"input-field\" id=\"back-input\" onClick=\"history.back()\">Zurück</button><button class=\"input-field\" id=\"save-input\" onClick=\"saveContent()\">Speichern unter</button></body>")
            html_copy = html_copy.replace("</script>", "function saveContent() {pywebview.api.saveMap()}</script>")
            with open("./_internal/copy.html", "w", encoding="utf-8") as cf:
                cf.write(html_copy)
            print("got html, switch to map")
            window = webview.windows[0]
            window.load_url("copy.html")

    def updateContent(self):
        self.content.update()

    def updateContentProgress(self):
        return {"message" : self.content.get_message()}

    def getMapProgress(self):
        return {"message" : self.folium_map.get_message()}
    
    def saveMap(self):
        file_types = ('HTML (*.html)', 'All files (*.*)')
        file_path = window.create_file_dialog(webview.SAVE_DIALOG, directory='/', save_filename='map.html', file_types=file_types)
        if file_path != None:
            with open(file_path, "w", encoding="utf-8") as save_file:
                save_file.write(self.html)

    def error(self):
        raise Exception('This is a Python exception')

if __name__ == '__main__':
    api = Api()
    web_debug = api.content.get_web_debug_status_from_config()
    window = webview.create_window('Open Data Karten Tool - Mobilfunk und Festnetz Österreich', url="internal-ui.html", js_api=api, min_size=(1275, 700), text_select=True)
    if platform.system() == "Windows":
        print("Windows with MS Edge Chromium")
        webview.start(gui="edgechromium", debug=web_debug, ssl=True)
    elif platform.system() == "Linux":
        print("Linux based with GTK")
        webview.start(gui="gtk", debug=web_debug, ssl=True)
    else:
        webview.start()