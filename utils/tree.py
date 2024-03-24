import aiohttp
import asyncio
import json
from pathlib import Path
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

LIBRARIES_IO_API_KEYS = [
    '7165ca9cc733d1abd00a87a930d9d714',
    '10b8f9c2a81b273a6c0db61fb96fb212',
    '53d6ec55fcbfdedb9ac6bd44ae42050c'
]
API_KEY_INDEX = 0
SEM = asyncio.Semaphore(10)  # Adjust according to your rate limit allowance

async def fetch_runtime_dependencies(session, library, version):
    global API_KEY_INDEX
    try:
        async with SEM:
            api_key = LIBRARIES_IO_API_KEYS[API_KEY_INDEX]
            url = f'https://libraries.io/api/pypi/{library}/{version}/dependencies?api_key={api_key}'
            async with session.get(url) as response:
                if response.status == 429:
                    API_KEY_INDEX = (API_KEY_INDEX + 1) % len(LIBRARIES_IO_API_KEYS)
                    return await fetch_runtime_dependencies(session, library, version)
                response.raise_for_status()
                data = await response.json()
                return [(dep['name'], dep['requirements'], dep['latest_stable']) for dep in data['dependencies'] if dep['kind'] == 'runtime']
    except Exception as e:
        print(f"Failed to fetch data for {library}: {str(e)}")
        return []

async def fetch_dependencies_tree(session, library, version, level=0):
    deps = await fetch_runtime_dependencies(session, library, version)
    print("finding dependencies for" + library + " - " + version)
    tree = {}
    for name, _, latest_stable in deps:
        sub_tree = await fetch_dependencies_tree(session, name, latest_stable, level + 1) if latest_stable else {}
        tree[name] = {"version": latest_stable, "dependencies": sub_tree}
    return tree

def format_dependency_tree(tree, prefix=''):
    lines = []
    for lib, info in tree.items():
        line = f"{prefix}{lib} - {info['version']}"
        lines.append(line)
        if info['dependencies']:
            lines.extend(format_dependency_tree(info['dependencies'], prefix + '  '))
    return '\n'.join(lines)

async def main(library, version):
    async with aiohttp.ClientSession() as session:
        dep_tree = await fetch_dependencies_tree(session, library, version)
        formatted_tree = format_dependency_tree(dep_tree)
        print(formatted_tree)

# Example usage
library = "tensorflow"
version = "2.15.0"
asyncio.run(main(library, version))
