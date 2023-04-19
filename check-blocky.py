import yaml
import tempfile
import requests
from urllib.parse import urlparse

BLOCKY_CFG = "/nix/store/crlmqidvaq697p2ax9ym3l3jfph9sj8b-config.yaml"

with open(BLOCKY_CFG, "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

blacklists = data["blocking"]["blackLists"]["normal"]


tmp_dir = tempfile.mkdtemp()
print(tmp_dir)

for blacklist in blacklists:
    r = requests.get(blacklist)
    filename = urlparse(blacklist).netloc.replace(".", "-") + ".txt"
    fpath = f"{tmp_dir}/{filename}"
    with open(fpath, "w+") as f:
        f.write(r.text)
