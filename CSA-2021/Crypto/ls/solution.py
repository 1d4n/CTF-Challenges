from requests import post


def send_zip(url, file_path):
    with open(file_path, 'rb') as f:
        return post(url, headers={"Content-Type": "application/zip"}, data=f.read()).json()["body"]


if __name__ == '__main__':
    URL = "https://ls.csa-challenge.com/upload-zip"

    print("good.zip:", send_zip(URL, r"collision\result\good.zip"), sep="\t")
    print("evil.zip:", send_zip(URL, r"collision\result\evil.zip"), sep="\t")
