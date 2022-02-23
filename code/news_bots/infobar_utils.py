import re

def Valid_URL(url):

    #regex for valid URL
    url_reg = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
    #compile
    check = re.compile(url_reg)

    #check if string is empty
    if (url == None):
        return False

    #check if string matches regex
    if (re.search(check, url)):
        return True
    else:
        return False

def Get_Publisher(url):
    reg_exp = r'\bhttps?://(?:www\.|ww2\.)?((?:[\w-]+\.){1,}\w+)\b'
    reg = re.compile(reg_exp, re.M)
    domain = reg.findall(url)[0]
    if domain.endswith(".com"):
        domain = domain[:-4]
        if domain == "nytimes":
            domain = "New York Times"
        elif domain == "newyorker":
            domain = "New Yorker"
        elif domain == "cnn":
            domain = domain.upper()
        elif domain == "oann":
            domain = "One America News Network"
        else:
            domain = domain.capitalize()


    return domain
