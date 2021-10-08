import regex as re
import requests
from bs4 import BeautifulSoup
import json

file = "headers.txt"
all_func = {}

with open(file) as file_in:
    for line in file_in:
        if line.startswith("#$ header function"):
            func_name = re.findall("function (.*?)\(", line)[0]
            print(func_name)
            link = "http://www.netlib.org/lapack/explore-html/globals_func_" + func_name[0] + ".html"
            request = requests.get(link, headers={"User-agent": "Mozilla/5.0"})
            soup = BeautifulSoup(request.text, 'lxml')
            a = soup.find_all("a", {"class": "el"})
            for e in a:
                l_func_name = func_name + ".f"
                if e.text == l_func_name:
                    f_link = "http://www.netlib.org/lapack/explore-html/" + e["href"]
                    f_request = requests.get(
                        f_link, headers={"User-agent": "Mozilla/5.0"}
                    )
                    f_soup = BeautifulSoup(f_request.text, 'lxml')
                    print(f_link)
                    tr = f_soup.find("table", {"class": "memname"}).find_all("tr")
                    all_func[func_name] = {}
                    for x in tr:
                        paramname = x.find("td", {"class": "paramname"})
                        paramtype = x.find("td", {"class": "paramtype"})
                        if paramname is None:
                            pass
                        else:
                            all_func[func_name][
                                paramname.text.replace(",", "").strip()
                            ] = paramtype.text.replace("\xa0", "")
                            print(paramname.text, "\t", paramtype.text)
                    print("-------------------------------------------")

with open('subroutines.json', 'w') as fp:
    json.dump(all_func, fp)