FROM registry.gitlab.com/nomnomdata/tools/nomnomdata-engine:master as builder

COPY requirements.txt /nomnom/requirements.txt
RUN pip wheel --wheel-dir /python_packages -r /nomnom/requirements.txt

FROM registry.gitlab.com/nomnomdata/tools/nomnomdata-engine:master

COPY --from=builder /python_packages /python_packages
RUN pip install --no-index --find-links /python_packages /python_packages/* && rm -rf /python_packages
WORKDIR /nomnom/
COPY pkg/*.* /nomnom/pkg/
CMD nnd engine run pkg/executable.py
