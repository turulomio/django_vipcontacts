from pydicts import lod
        
def lod_model_history(object, console=False):
    lod_=object.history.order_by("history_date").values()
    if console is True:
        lod.lod_print(lod_)
    return lod_
