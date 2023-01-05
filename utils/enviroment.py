from os import environ


def get_env_variable(variable_name, default_value=''):
    return environ.get(variable_name, default_value)


def parse_comme_str_to_list(comma_str):
    if not comma_str or not isinstance(comma_str, str):
        return []
    return [string.strip() for string in comma_str.split(',') if string]


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    print(parse_comme_str_to_list(get_env_variable('ALLOWED_HOSTS')))
