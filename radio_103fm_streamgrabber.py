import os
import inspect
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from datetime import datetime
import webbrowser

def name(var):
    """ Gets the name of the given variable. """
    for fi in reversed(inspect.stack()):
        names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
        if len(names) > 0: return names[0]


def download_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return str(response.content)
    else:
        print(response.raise_for_status())


def download_episode(episode_url, filename):
    response = requests.get(episode_url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
    else:
        print(response.raise_for_status())


def reformat_date(date_str):
    date = date_str[3:][:6]
    clean_date = datetime.strptime(date, '%d%m%y').strftime("%d.%m.%Y")
    return clean_date


def construct_episode_url4download(single_episode_url):
    soup = BeautifulSoup(download_html(single_episode_url), "lxml")
    data_file = soup.find_all('div', class_='mouthjs-autoplay')[0]['data-file']
    stream_download_url = f'https://awaod01.streamgates.net/103fm_aw/{data_file}.mp3'
    return stream_download_url


def extract_episodes_urls(full_episodes_url):
    ''' Given an 103-FM radio show url --> extract all episode URLs. '''

    episode_indicator = '/programs/media.aspx?'
    episode_id = full_episodes_url[-3:]
    soup = BeautifulSoup(download_html(full_episodes_url), 'html.parser')
    episodes_urls = []

    for a in soup.find_all('a', href=True):
        temp_url = a['href']
        if temp_url.startswith(episode_indicator) and temp_url.endswith(episode_id):
            episodes_urls.append(f'https://103fm.maariv.co.il{temp_url}')

    episodes_download_urls = [construct_episode_url4download(episodes_url) for episodes_url in episodes_urls]
    return episodes_download_urls


def download_all_streams(episodes, dest_folder='', create_nonexisting_dir=True, open_download_folder=False,
                         pretty_print_filename=False, verbose=0):
    if not os.path.exists(dest_folder) and create_nonexisting_dir:
        os.mkdir(dest_folder)

    for episode_id, url_complete_episodes in tqdm(episodes.items()):
        full_episodes_urls = extract_episodes_urls(url_complete_episodes)

        for full_episodes_url in full_episodes_urls:
            filename = full_episodes_url[full_episodes_url.rfind('/') + 1:]
            full_episode_date = reformat_date(filename[:-3])

            if pretty_print_filename:
                filename = f'{filename[:3]}_{full_episode_date}.mp3'

            if verbose == 2:
                print(f'\nDownloading stream [{episode_id}] --> date: {full_episode_date} from url:\n{full_episodes_url}')

            if dest_folder == '':
                download_episode(full_episodes_url, filename)
            else:
                download_episode(full_episodes_url, dest_folder + '\\' + filename)
            if verbose == 2: print('Done.')

    if verbose == 1:
        print('--> Finished all downloads.')

    if open_download_folder:
        webbrowser.open(dest_folder)


if __name__ == '__main__':
    # ---------------------------------------------------------------------------------------
    # Define episodes-urls: To add more just lookup_ https://103fm.maariv.co.il/programs/ and
    # add the respective show unter the menu: "תוכניות"
    # ---------------------------------------------------------------------------------------
    adam = 'https://103fm.maariv.co.il/programs/complete_episodes.aspx?c41t4nzVQ=HEM'
    zehavi = "https://103fm.maariv.co.il/programs/complete_episodes.aspx?c41t4nzVQ=EM"
    didi = "https://103fm.maariv.co.il/programs/complete_episodes.aspx?c41t4nzVQ=EG"
    caraso = "https://103fm.maariv.co.il/programs/complete_episodes.aspx?c41t4nzVQ=FF"
    iris_kol = "https://103fm.maariv.co.il/programs/complete_episodes.aspx?c41t4nzVQ=M"

    episodes = dict()
    episodes[name(adam)] = adam
    episodes[name(zehavi)] = zehavi
    episodes[name(didi)] = didi
    episodes[name(caraso)] = caraso
    episodes[name(iris_kol)] = iris_kol
    # ---------------------------------------------------------------------------------------

    dest_folder = r'YOUR_DESTINATION_FOLDER'
    download_all_streams(episodes, dest_folder, pretty_print_filename=True, verbose=2)
