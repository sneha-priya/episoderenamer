#!/home/vinay/anaconda3/bin/python
# -*- coding: utf-8 -*-

import os
import glob
import urllib.request

import bs4


def get_episode_no(episode_path):
    """ Returns episode number"""
    import re

    s = re.search("S[0-9][0-9]E[0-9][0-9]",episode_path)
    return s.group()
   
def main():
    """This is the main function."""
    episode_list = get_episode_list("https://en.wikipedia.org/wiki/List_of_Game_of_Thrones_episodes")
    formats = ['mkv', 'mp4', 'avi']
    
    folder_path = "/media/disks/storage/series/live_action/Game of Thrones/"
    file_list = []
    for format_ in formats:
        file_list += glob.glob(folder_path+ "*.{}".format(format_) )

    for file_ in file_list:
        if os.path.isfile(file_):
            episode_no = get_episode_no(file_)
            try:
                episode_name = episode_list[episode_no]
                containing_folder = os.path.dirname(file_)
                old_file_name = os.path.basename(file_)
                ext = os.path.splitext(file_)[1]
                new_file_name = "{}_{}{}".format(episode_no, episode_name, ext)
                new_file_path = os.path.join(containing_folder, new_file_name)
                os.rename(file_, new_file_path)
            except KeyError: 
                print("no data found for : {}".format(episode_no))


def get_episode_list(page):
    episode_list = {}
    with urllib.request.urlopen(page) as response:
        wikipedia_html = response.read()
        soup = bs4.BeautifulSoup(wikipedia_html, "lxml")
        table_soup = soup.find_all('table', attrs= {"class":"wikiepisodetable"})
        for season, table in enumerate(table_soup):

            row_soup = table.find_all('tr', attrs = {"class":"vevent"})

            for episode_no, row in enumerate(row_soup):
                td_soup =row.find_all('td', attrs = {"class": "summary"})  
                td = td_soup[0]
                episode_name = td.text
                episode_name = episode_name.replace('"',"")
                episode_name = episode_name.replace(" ","_")
                episode_name = episode_name.replace(":", "")
                episode_name = episode_name.lower()
                season_episode = "S{:02d}E{:02d}".format(season+1,episode_no+1)
                episode_list[season_episode] = episode_name
            
    return episode_list
            


if __name__ == "__main__":
    main()