import toml


class ConfigError(Exception):
    pass

class Section:
    pass

class Config:
    _sections = {
        'app' : [ 'prefix' ],
        'database' : [ 'host', 'user', 'password', 'dbname' ]
    }

def load(path):
    config = Config()
    try:
        kv = toml.load(path)
    except Exception as e:
        raise ConfigError(e)

    for sect_name, sect_fields in Config._sections.items():
        section = Section()
        try:
            kv_section = kv[sect_name]
        except KeyError:
            raise ConfigError('Section [{}] not present'.format(sect_name))
        config.__dict__[sect_name] = section
        for field_name in sect_fields:
            try:
                section.__dict__[field_name] = kv_section[field_name]
            except KeyError:
                raise ConfigError('Field {}.{} not present'.format(sect_name, field_name))
            kv_section[field_name] = None

    for sect_name, toml_section in kv.items():
        for field_name, field_value in kv_section.items():
            if field_value is not None:
                raise ConfigError('Unknown config option {}.{}'.format(sect_name, field_name))

    return config
