FROM public.ecr.aws/lambda/python:3.12

COPY agresso ${LAMBDA_TASK_ROOT}/agresso
COPY barnehagefakta ${LAMBDA_TASK_ROOT}/barnehagefakta
COPY barnehageregister ${LAMBDA_TASK_ROOT}/barnehageregister
COPY better_uptime ${LAMBDA_TASK_ROOT}/better_uptime
COPY common ${LAMBDA_TASK_ROOT}/common
COPY measurements ${LAMBDA_TASK_ROOT}/measurements
COPY ssb ${LAMBDA_TASK_ROOT}/ssb
COPY statistikkbanken ${LAMBDA_TASK_ROOT}/statistikkbanken
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --no-cache-dir -r requirements.txt

CMD ["set-me-in-serverless.yaml"]
