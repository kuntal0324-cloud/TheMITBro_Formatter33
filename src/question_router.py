
from pathlib import Path
from .question_bank_store import QuestionBankStore
def route(record, source, root):
    return QuestionBankStore(Path(root)).add(record, Path(source))
