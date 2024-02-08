import yaml
from pathlib import Path


def load_cofing():
    # Ruta al archivo YAML
    archivo_yml = Path.cwd() / 'config.yml' 

    # Abrir y retornar la configuración
    with open(archivo_yml, 'r') as archivo:
        file = yaml.safe_load(archivo)
        return file


