from httpx import AsyncClient
import hashlib
import base64
import json
import os
from time import time

token = os.getenv('SSENSS_TOKEN')
host = 'https://www.ssenss.com'
system_id = 489

headers = {'x-request-token': token}



def base64_sha256(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return str(base64.urlsafe_b64encode((h.digest())), 'UTF-8').strip('=')

async def _upload_file(fp):
    url = f'{host}/api/file/run/'
    async with AsyncClient() as client:
        rsp = await client.post(
            url,
            files={'file': fp},
            headers=headers,
            timeout=None,
        )
        return rsp.json()['data']


async def upload_file(file_path):
    with open(file_path, 'rb') as fp:
        return await _upload_file(fp)


async def get_system():
    url = f'{host}/api/system/one?id={system_id}'
    async with AsyncClient() as client:
        rsp = await client.get(url, headers=headers, timeout=None)
        return rsp.json()['system']


async def save_system(**system):
    url = f'{host}/api/system/save/'
    system['id'] = system_id
    async with AsyncClient() as client:
        rsp = await client.post(
            url,
            content=json.dumps(system),
            headers=headers,
            timeout=None,
        )

        return rsp.json()['system']


async def get_doc_map():
    system = load_system()
    if not system:
        system = await get_system()
        save_system_file(system)

    data = system['system_data']
    docs = data.get('docs', [])

    doc_map = {}

    for doc in docs:
        doc_map[doc['file_key']] = doc

    return doc_map


def load_system():
    if not os.path.isfile('system.json'):
        return None

    try:
        with open('system.json', 'r') as fp:
            data = json.load(fp)
            if data['updated_at'] + 60 > time():
                return data

    except Exception:
        pass

    return None


def save_system_file(system):
    system['updated_at'] = int(time())
    with open('system.json', 'w') as fp:
        fp.write(json.dumps(system, ensure_ascii=False, indent=2))


def get_file_hash(file_path):
    with open(file_path, 'rb') as fp:
        return base64_sha256(fp.read())


async def main(file_path):
    print('upload_file', file_path)
    doc_map = await get_doc_map()

    file_key = get_file_hash(file_path)

    if doc_map.get(file_key):
        return

    ret = await upload_file(file_path)

    meta = ret['meta']

    new_doc = {
        'id': ret['id'],
        'name': ret['name'],
        'fid': meta['id'],
        'file_key': meta['file_key'],
        'file_ext': meta['file_ext'],
        'pages': meta['pages'],
        'embedding_hash': meta['embedding_hash'],
        'url': 'https://docs.kazuo.ai/' + file_path[:-3]
    }

    print(new_doc)

    new_docs = [new_doc]
    required_update = False
    removed = []

    for doc in doc_map.values():
        if doc['name'] == new_doc['name']:
            if doc['id'] == new_doc:
                break
            else:
                removed.append(doc)
                required_update = True
                continue

        new_docs.append(doc)


    system = await save_system(system_data={'docs': new_docs})
    save_system_file(system)


if __name__ == '__main__':
    import sys
    import asyncio
    asyncio.run(main(sys.argv[1]))
