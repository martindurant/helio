from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pandas as pd
import requests
from requests.adapters import HTTPAdapter, Retry
from tqdm import tqdm

PATH = Path(__file__).parent.resolve()
URLS = pd.read_csv(PATH / "vso_export_20221118_000000.csv", header=None)[0].to_list()
HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"
}


def download_file(url):
    query = parse_qs(urlparse(url).query, separator=";")
    local_filename = PATH / "raw" / f"{query['series'][0]}_{query['record'][0]}.tar"
    if local_filename.exists():
        return local_filename

    try:
        s = requests.Session()
        retries = Retry(
            total=1000, backoff_factor=1, status_forcelist=[500, 502, 503, 504]
        )
        s.mount("http://", HTTPAdapter(max_retries=retries))

        with s.get(url, stream=True, headers=HEADERS) as r:
            r.raise_for_status()
            with open(local_filename, "wb") as f:
                ic = r.iter_content(chunk_size=8192)
                for chunk in tqdm(ic, leave=False, total=600_000):
                    f.write(chunk)
    except Exception:
        if local_filename.exists():
            local_filename.unlink()
        raise
    return local_filename


def main():
    with ThreadPoolExecutor() as ex:
        list(tqdm(ex.map(download_file, URLS), total=len(URLS)))


if __name__ == "__main__":
    main()
