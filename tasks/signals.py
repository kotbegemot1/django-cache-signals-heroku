from django.db.models.signals import m2m_changed, post_save, pre_delete
from django.dispatch import receiver
from tasks.models import TodoItem, Category, Priority
from collections import Counter


def print_signal_info(sender, instance, action, model, **kwargs):
    print()
    print(f'sender = {sender}')
    print(f'instance = {instance}')
    print(f'action = {action}')
    print(f'model = {model.__name__}')
    print(f'kwargs')
    for key, value in kwargs.items():
        print(f'    key = {key}, value = {value}')
    print()


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_added(sender, instance, action, model, **kwargs):

    # print_signal_info(sender, instance, action, model, **kwargs)
    if action == "post_add":

        for cat in instance.category.all():
            slug = cat.slug


            new_count = 0
            for task in TodoItem.objects.all():
                new_count += task.category.filter(slug=slug).count()

            Category.objects.filter(slug=slug).update(todo_count=new_count)
    
    else:
        return
    
    
        

@receiver(pre_delete, sender=TodoItem)
def task_cats_removed(sender, instance, action='pre_delete', model=TodoItem, **kwargs):
    
    print_signal_info(sender, instance, action, model, **kwargs)

    # capi = str(instance).capitalize()
    model_ = model.objects.get(description=instance).category.all()
    for cat in model_:
        slug = cat.slug
        print(slug)

    cat_count = Category.objects.get(slug=slug).todo_count
    cat_count -= 1
    Category.objects.filter(slug=slug).update(todo_count=cat_count)

    prior_count = model.objects.get(description=instance).priority
    # print(prior_count)
    prior_count.todo_count = prior_count.todo_count - 1
    prior_count.save()

@receiver(post_save, sender=TodoItem)
def task_prts_changed(sender, instance, action='post_save', model=TodoItem, **kwargs):

    # print_signal_info(sender, instance, action, model, **kwargs)
    # capi = str(instance).capitalize()
    prior_count = TodoItem.objects.get(description=instance).priority
    prior_count.todo_count = prior_count.todo_count + 1
    prior_count.save()

