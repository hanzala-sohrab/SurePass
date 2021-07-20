import requests
import foo


def check(phone):
    url = f"{foo.APIUrl}checkPhone?phone={phone}&token={foo.token}"

    headers = dict()
    headers["Content-Type"] = "application/json"

    resp = requests.get(url, headers=headers).json()
    return resp


if __name__ == "__main__":
    print(check(919031738598))
