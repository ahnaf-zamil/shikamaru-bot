async def fetch(session, url):

    response = await session.get(url)
    response = await response.read()
    return response