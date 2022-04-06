# Roughly following this blog recommended by the the Jupyter Docker docs:
# https://herrmann.tech/en/blog/2021/02/08/how-to-build-custom-environment-for-jupyter-in-docker.html

FROM jupyter/datascience-notebook

# set locales, en_US.UTF-8 should already be a default but leaving this as a template for future requrirements
#RUN set -ex \
#   && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
#   && locale-gen en_US.UTF-8 \
#   && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \

# install Python packages you often use
RUN set -ex \
   && conda install --quiet --yes \
   # choose the Python packages you need
#   'plotly==4.9.0' \
   'plotly' \
#   'folium==0.11.0' \ # specific version removed due to conflict on m1 mac
   'folium' \
   'yfinance' \
   && conda clean --all -f -y \
   # install Jupyter Lab extensions you need
   && jupyter labextension install jupyterlab-plotly --no-build \
   && jupyter lab build -y \
   && jupyter lab clean -y \
   && rm -rf "/home/${NB_USER}/.cache/yarn" \
   && rm -rf "/home/${NB_USER}/.node-gyp" \
   && fix-permissions "${CONDA_DIR}" \
   && fix-permissions "/home/${NB_USER}" \
   # install coinbase SDK
   && git clone https://github.com/resy/coinbase_python3.git \
   && cd coinbase_python3 \
   && python3 setup.py install
   


