import matplotlib.pyplot as plt


world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
cities = geopandas.read_file(geopandas.datasets.get_path('naturalearth_cities'))

fig, ax = plt.subplots()

# set aspect to equal. This is done automatically
# when using *geopandas* plot on it's own, but not when
# working with pyplot directly.
ax.set_aspect('equal')
world.plot(ax=ax, color='white', edgecolor='black')
cities.plot(ax=ax, marker='o', color='red', markersize=5)
plt.show();

#
#
# import sys, setuptools, tokenize
# sys.argv[0] = '"'"'C:\\Users\\paul-\\AppData\\Local\\Temp\\pip-install-f42vrjm8\\python-levenshtein\\setup.py'"'"'
# __file__='"'"'C:\\Users\\paul-\\AppData\\Local\\Temp\\pip-install-f42vrjm8\\python-levenshtein\\setup.py'"'"'
# f=getattr(tokenize, '"'"'open'"'"', open)(__file__)
# code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"')
# f.close()
# exec(compile(code, __file__, '"'"'exec'"'"'))' install --record 'C:\Users\paul-\AppData\Local\Temp\pip-record-94_8dnl7\install-record.txt' --single-version-externally-managed --compile --install-headers 'C:\Users\paul-\.conda\envs\py3\Include\python-levenshtein
