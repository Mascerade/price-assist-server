def format_item_model(item_model):
    to_remove = [" ", "-", "_", "(", ")"]
    for x in to_remove:
        item_model = item_model.replace(x, "")

    return item_model