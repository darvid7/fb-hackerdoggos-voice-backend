class ConfigParser:

    @staticmethod
    def load_config(path):
        config = {}
        with open(path, 'r') as f:
            for line in f:
                key, data = line.split(':')
                key = key.lstrip().rstrip()
                data = data.lstrip().rstrip()
                if key in config:
                    raise KeyError('Config item: %s already parsed' % key)
                config[key] = data
        return config


if __name__ == '__main__':
    config_loader = ConfigParser()
    config = config_loader.load_config('fb_app_config')
    print(config)
