import requests
from bs4 import BeautifulSoup
import inspect
import webbrowser

def var_name(var):
    """ Gets the name of a given variable. """
    for fi in reversed(inspect.stack()):
        names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
        if len(names) > 0:
            return names[0]


def url2html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return str(response.content)


def download_url(url, filename):
    response = requests.get(url)
    #response = requests.get(url, headers={'Connection': 'close'})
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        file.close()
    else:
        print(f"Couldn't download: {url} --> Server status code: {str(response.status_code)}")



def construct_episode_url4download(single_episode_url):
    html = url2html(single_episode_url)
    soup = BeautifulSoup(html, "lxml")
    data_file = soup.find_all('div', class_='mouthjs-autoplay')[0]['data-file']
    stream_download_url = f"http://103fm_aod_main.streamgates.net/103fm_aod/{data_file}.mp3"
    return stream_download_url


def extract_episodes_urls(full_episodes_url):
    ''' Starting from a given 103-FM radio show url: extract all episode URLs. '''
    html = url2html(full_episodes_url)

    episode_indicator = "/programs/media.aspx?"
    episode_id = full_episodes_url[-3:]

    soup = BeautifulSoup(html, 'html.parser')
    episodes_urls = []
    for a in soup.find_all('a', href=True):
        temp_url = a['href']
        if temp_url.startswith(episode_indicator) and temp_url.endswith(episode_id):
            episodes_urls.append(f"https://103fm.maariv.co.il{temp_url}")

    episodes_download_urls = [construct_episode_url4download(episodes_url) for episodes_url in episodes_urls]
    return episodes_download_urls


def download_all_streams(episodes, dest_path, open_download_folder=True):
    for episode_id, url_complete_episodes in episodes.items():
        full_episodes_urls = extract_episodes_urls(url_complete_episodes)

        for full_episodes_url in full_episodes_urls:
            filename = full_episodes_url[full_episodes_url.rfind("/") + 1:]

            print(f"Downloading show-id: {episode_id} from url: {full_episodes_url}")
            download_url(full_episodes_url, dest_path + "\\" + filename)
            print('Done.')

    print('--> Finished all downloads.')
    if open_download_folder: webbrowser.open(dest_path)



#---------------------------------------------------------------------------------------
# Define episodes-urls: To add more lookup_ https://103fm.maariv.co.il/programs/ and add you respective show unter the menu: "תוכניות"
#---------------------------------------------------------------------------------------
zehavi   = "https://103fm.maariv.co.il/programs/complete_episodes.aspx?c41t4nzVQ=EM"
didi     = "https://103fm.maariv.co.il/programs/complete_episodes.aspx?c41t4nzVQ=EG"
caraso   = "https://103fm.maariv.co.il/programs/complete_episodes.aspx?c41t4nzVQ=FF"
iris_kol = "https://103fm.maariv.co.il/programs/complete_episodes.aspx?c41t4nzVQ=M"

episodes = dict()
episodes.update({var_name(zehavi):zehavi})
episodes.update({var_name(didi):didi})
episodes.update({var_name(caraso):caraso})
episodes.update({var_name(caraso):iris_kol})
#---------------------------------------------------------------------------------------


dest_path = r"C:\_________103FM !"
download_all_streams(episodes, dest_path)
