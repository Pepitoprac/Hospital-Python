import os
from Hospitalsangabriel.vistas.Loguearse import IniciarPrograma
from rutadb import DB as RutaDb

DB = RutaDb

def VerificarBaseDeDatos():
    print(f"🔍 Verificando base de datos en: {DB}")

    if not os.path.exists(DB):
        print("❌ No se encontró el archivo de base de datos.")
        return False

    if not os.path.isfile(DB):
        print("⚠️ La ruta existe, pero no es un archivo válido de base de datos.")
        return False

    print("✅ Base de datos encontrada correctamente.")
    return True


if __name__ == "__main__":
    if VerificarBaseDeDatos():
        IniciarPrograma(DB)
    else:
        print("\n💥 ERROR: No se pudo iniciar el programa porque falta la base de datos.")
