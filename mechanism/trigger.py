from celery import shared_task


@shared_task()
def hello_dodo(x):
    print("beat beat",x)
