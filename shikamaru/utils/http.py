async def fetch(session, url):

    response = await session.get(url)
    response = await response.read()
    return response


async def post(session, url, data):
    response = await session.post(url, data=data)
    response = await response.read()
    return response
