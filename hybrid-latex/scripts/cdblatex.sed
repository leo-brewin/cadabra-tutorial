# add global SED edits here

# remove superfluous \discretionary{}{}{}
# s!\\discretionary\{\}\{\}\{\}!!g  # maybe could use this
s!\\discretionary\{\}\{\}\{\}!{}!g  # but this is safer
