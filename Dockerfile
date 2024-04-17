FROM public.ecr.aws/lambda/python:3.11

COPY agresso ${LAMBDA_TASK_ROOT}/agresso
COPY better_uptime ${LAMBDA_TASK_ROOT}/better_uptime
COPY common ${LAMBDA_TASK_ROOT}/common
COPY measurements ${LAMBDA_TASK_ROOT}/measurements
COPY okdata_disruptive ${LAMBDA_TASK_ROOT}/okdata_disruptive
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --no-cache-dir -r requirements.txt

CMD ["set-me-in-serverless.yaml"]
