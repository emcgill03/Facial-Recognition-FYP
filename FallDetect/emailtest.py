import requests


return requests.post(
    "https://api.mailgun.net/v3/sandbox8136583a700c4d77b99a43e10c32f3db.mailgun.org/messages",
    auth=("api", "0889d1fe9657234aed02a77ad021a45c-ee13fadb-5c52799d"),
    data={"from": "Mailgun Sandbox <mailgun@sandbox8136583a700c4d77b99a43e10c32f3db.mailgun.org>",
        "to": ["emcgill03@hotmail.com"],
        "subject": "Hello",
        "text": "Testing some Mailgun awesomness!"})

