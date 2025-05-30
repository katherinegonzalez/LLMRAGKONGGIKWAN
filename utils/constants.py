from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
print("BASE_DIR: ", BASE_DIR)
# Path to the saved Chroma index
INDEX_PATH = str(BASE_DIR / "chroma_index")

# Documents Paths
DOCUMENTS_DIR = BASE_DIR / "documents"
temp_paths = [
    str(DOCUMENTS_DIR / "AcademiaKongGiKwan.pdf"),
    str(DOCUMENTS_DIR / "ProgramaAscensoKongGiKwan.pdf"),
    str(DOCUMENTS_DIR / "SignificadoDeTaeguks.pdf"),
]