def change_model_image(model, img_url, **kwargs):
    if model == 'user':
        instance = kwargs['request'].user
        instance.img_url = img_url
        instance.save()
