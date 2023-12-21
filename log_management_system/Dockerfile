FROM python:3-alpine

COPY . /log_management_system

WORKDIR /log_management_system

RUN pip install -r requirements.txt

RUN python manage.py collectstatic

EXPOSE 3000

CMD ["gunicorn", "--bind", "0.0.0.0:3000", "--workers", "3", "log_management_system.wsgi:application"]