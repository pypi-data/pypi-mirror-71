import json
import logging
import os

from code_manager.core.configuration import ConfigurationAware
from code_manager.utils.read_input import promt_yes_no


class CacheContainer(ConfigurationAware):

    loaded = False
    dirty = False
    cache = {}

    def __init__(self):
        pass

    def _internal_rebuild(self):
        for pack, _ in self.packages.items():
            root = self._get_root(pack)
            pack_root = os.path.join(self.code_dir, root)
            if os.path.exists(os.path.join(pack_root, '.code_manager_cache')):
                with open(os.path.join(root, '.code_manager_cache')) as c:
                    node = json.load(c)
                self.cache[pack] = node

    def load_cache(self):
        logging.debug('Loading cache from the cache file %s ', self.cache_file)

        try:
            self.cache = json.load(open(self.cache_file))
        except json.decoder.JSONDecodeError:
            logging.debug('Invalid or empty cache. Starting with clean cache')

            if not promt_yes_no('Cache file is invalid. Should it be erased and build again?'):
                raise SystemExit

            self._internal_rebuild()

        self.preupdate_cache()
        self.loaded = True

    def preupdate_cache(self):
        for group, packages in self.packages_list.items():
            for package in packages:
                if package not in self.cache.keys():
                    self.cache[package] = dict()
                    self.cache[package]['node'] = (
                        self.config['packages'][package]
                    )
                    self.cache[package]['installed'] = False
                    self.cache[package]['fetched'] = False
                    self.cache[package]['built'] = False
                    self.cache[package]['group'] = group
                    self.cache[package]['root'] = ''

        self.save_cache()

    def save_cache(self):
        logging.debug('Dumping the cache in the cache file.')
        json.dump(
            self.cache, open(self.cache_file, 'w'),
            indent=4, separators=(',', ' : '),
        )

        for pack, p in self.cache.items():
            if not p['fetched']:
                continue

            json.dump(
                p, open(os.path.join(self.code_dir, p['root'], '.code_manager_cache'), 'w'),
                indent=4, separators=(',', ' : '),
            )

        self.dirty = False

    def update_cache(self, name, prop, value):
        assert name is not None
        assert prop is not None
        assert value is not None

        if name not in self.cache.keys():
            logging.debug('%s is not in the cache', name)
            return False
        self.cache[name][prop] = value
        self.dirty = True
        return True

    def rebuild(self, pack, root):
        with open(os.path.join(root, '.code_manager_cache')) as c:
            node = json.load(c)
        self.cache[pack] = node
        self.dirty = True

    def check_cache(self, name, prop='installed'):
        assert name is not None

        if name not in self.cache.keys():
            logging.debug('%s is not in the cache', name)
            return False

        return self.cache[name][prop]

    def set_installed(self, name, value):
        return self.update_cache(name, prop='installed', value=value)

    def set_fetched(self, name, value):
        return self.update_cache(name, prop='fetched', value=value)

    def set_built(self, name, value):
        return self.update_cache(name, prop='built', value=value)

    def set_root(self, name, value):
        return self.update_cache(name, prop='root', value=value)

    def is_installed(self, name):
        return self.check_cache(name, prop='installed')

    def is_fetched(self, name):
        return self.check_cache(name, prop='fetched')

    def is_built(self, name):
        return self.check_cache(name, prop='built')

    def get_root(self, name):
        return self.check_cache(name, prop='root')

    def in_cache(self, name):
        return name in self.cache.keys()

    def get_packages(self):
        return self.cache.values()

    def drop(self, name):
        if name not in self.cache.keys():
            logging.debug('%s is not in the cache', name)
            return False
        self.cache.pop(name, None)
        self.dirty = True
        return True

    def __enter__(self):
        if not self.loaded:
            self.load_cache()
        return self

    def __exit__(self, type_, value, traceback):
        if self.dirty:
            self.save_cache()

    def __getitem__(self, name):
        if name in self.cache.keys():
            return self.cache[name]
        return None

    def __call__(self, name):
        return name in self.cache.keys()
