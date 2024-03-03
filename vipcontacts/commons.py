def history_diff(old_history, new_history):
    delta=new_history.diff_against(old_history)
    for change in delta.changes:
        print("{0} changed from {1} to {2}".format(change.field, change.old, change.new))
