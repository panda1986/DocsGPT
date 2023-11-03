import os
from application.vectorstore.base import BaseVectorStore
from langchain.vectorstores import FAISS
from application.core.settings import settings

class FaissStore(BaseVectorStore):

    def __init__(self, path, embeddings_key, docs_init=None):
        super().__init__()
        # set faiss loglevel to verbose
        
        print("FaissStore, path:%s, embeddings_key:%s, docs_init:%s" % (path, embeddings_key, docs_init))
        # if not path startwith /, change path to absolute path
        if not path.startswith("/"):
            # get current path
            current_path = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(current_path, "../../", path)
            print("current_path:%s, path=%s" % (current_path, path))

        self.path = path
        if docs_init:
            self.docsearch = FAISS.from_documents(
                docs_init, self._get_embeddings(settings.EMBEDDINGS_NAME, embeddings_key)
            )
        else:
            self.docsearch = FAISS.load_local(
                self.path, self._get_embeddings(settings.EMBEDDINGS_NAME, settings.EMBEDDINGS_KEY)
            )

    def search(self, *args, **kwargs):
        return self.docsearch.similarity_search(*args, **kwargs)

    def add_texts(self, *args, **kwargs):
        return self.docsearch.add_texts(*args, **kwargs)
    
    def save_local(self, *args, **kwargs):
        return self.docsearch.save_local(*args, **kwargs)


