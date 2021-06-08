def read_config():
    with open('config.yaml', 'r') as f:
        data = {}
        for line in f.readlines():
            line = line.strip()
            key, value = line.split(':')
            data[key] = value.strip()
        
        return data