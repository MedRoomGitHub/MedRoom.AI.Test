ARG base_image
FROM $base_image

ARG config_path


LABEL maintainer="eneas.rodrigues25@gmail.com"

USER $root

RUN mkdir ~/.pip
RUN apt-get update
RUN apt-get install python3-dev gcc g++ -y # python setup.py install

RUN pip config list -v
ADD requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download pt_core_news_sm
RUN pip install nltk
RUN python -c "import nltk; nltk.download('stopwords')"

RUN echo 'c.NotebookApp.contents_manager_class = "notedown.NotedownContentsManager"' >> ~/.jupyter/jupyter_notebook_config.py
# NbEtensions
RUN python -m pip install --upgrade jupyterthemes
RUN python -m pip install jupyter_contrib_nbextensions
RUN jupyter contrib nbextension install --user
RUN jupyter nbextension enable contrib_nbextensions_help_item/main
RUN jupyter nbextension enable autosavetime/main
RUN jupyter nbextension enable freeze/main
RUN jupyter nbextension enable execute_time/ExecuteTime
RUN jupyter nbextension enable toc2/main
