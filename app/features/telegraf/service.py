from telegraph import Telegraph
from time import localtime


def get_page(title: str, raw_body: str):
    body = [i + '\n\n' for i in raw_body.split('\n')]
    telegraph = Telegraph()
    telegraph.create_account(short_name='dvizh_bot')
    response = telegraph.create_page(
        title=title,
        author_name=f'DVIZH•{localtime().tm_hour} : {localtime().tm_min}',
        content=body,
        html_content=None
    )
    return f'https://telegra.ph/{response["path"]}'
