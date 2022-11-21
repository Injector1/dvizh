from telegraph import Telegraph


def get_page(title: str, raw_body: str):
    body = format_text(raw_body)
    telegraph = Telegraph()
    telegraph.create_account(short_name='dvizh_bot')
    response = telegraph.create_page(
        title=title,
        author_name='DVIZH',
        content=body,
        html_content=None
    )
    return f'https://telegra.ph/{response["path"]}'


def format_text(text: str) -> list[str]:
    return [i + '\n\n' for i in text.split('\n')]


if __name__ == '__main__':
    content = 'First line\nSecond line\nThird line'
    print(get_page('Football theme', content))
