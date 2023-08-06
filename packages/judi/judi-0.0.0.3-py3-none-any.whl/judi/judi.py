import pandas as pd

JUDI_PARAM = pd.DataFrame({'JUDI': ['*']})

def add_param(param_info, name = None):
  global JUDI_PARAM
  if isinstance(param_info, list):
    param_info = {name: param_info}
  if isinstance(param_info, dict):
    param_info = pd.DataFrame(param_info)
  if isinstance(param_info, pd.Series):
    param_info = pd.DataFrame([param_info])
  if not isinstance(param_info, pd.DataFrame):
    print("Error! input data must be a list, series or dataframe!!!")
    exit(-1)
  JUDI_PARAM = JUDI_PARAM.assign(key=1).merge(param_info.assign(key=1), on='key', how='outer').drop('key', 1)


def show_param_db():
  print("JUDI_PARAM:\n", JUDI_PARAM)


def copy_param_db():
  return JUDI_PARAM.copy()


def mask_global_param_db(mask_cols):
  param = JUDI_PARAM.copy()
  masked = JUDI_PARAM.copy()
  param_cols = list(set(param.columns) - set(mask_cols))
  param = param.drop(mask_cols, 1).drop_duplicates()
  masked = masked.drop(param_cols, 1).drop_duplicates()
  return(param, masked)


def mask_param_db(param_db, mask_cols):
  pdb = param_db.copy()
  pdb = pdb.drop(mask_cols, 1).drop_duplicates()
  return pdb


def param_diff(big, small):
  diff_cols = list(set(big.param.columns) - set(small.param.columns))
  return big.param[diff_cols].drop_duplicates()


import os
def ensure_dir(file_path):
  directory = os.path.dirname(file_path)
  if directory and not os.path.exists(directory):
    print("Creating new directory", directory)
    os.makedirs(directory)


import json
def get_cfg_str(x):
  # json.dumps(r.to_dict(), sort_keys=True, separators = (',', '~'))[1:-1]
  # It seems DoIt does not allow equal (=) char in task name
  return ",".join(['{}~{}'.format(k,v) for (k,v) in sorted(x.to_dict().items()) if k not in ['JUDI', 'name']])


def combine_csvs_base(params, infiles, outfile):
  df = pd.DataFrame()
  for indx, r in params.assign(infile = infiles).iterrows():
    tmp = pd.read_csv(r['infile'])
    for col in params.columns:
      tmp[col] = r[col]
    df = df.append(tmp, ignore_index=True)
  df.to_csv(outfile, index=False)


def combine_csvs(big, small):
  infiles = big['path'].tolist()
  outfile = small['path'].tolist()[0]
  params = big.drop(columns=['name', 'path'])
  combine_csvs_base(params, infiles, outfile)


class File(object):
  file_db = pd.DataFrame(columns = ['name', 'path'])
  def __init__(self, name, param = pd.DataFrame(), mask = None, path = None, root = './judi_files'):
    self.param = (JUDI_PARAM if param.empty else param).copy()
    if mask: self.param = mask_param_db(self.param, mask)
    if not self.param.empty:
      if len(set(param.columns) - set(self.param.columns)):
        print("Error: columns of param do not match with global param!!")
        exit(-1)
      self.param['name'] = name
      if not path:
        self.param['path'] = self.param.apply(lambda x: get_cfg_str(x), axis='columns')
        self.param['path'] = self.param.apply(lambda x: "/".join([e for e in [root, x['path'], x['name']] if e != '']), axis = 'columns')
      elif callable(path):
        self.param['path'] = self.param.apply(path, axis='columns')
      else:
        self.param['path'] = path
      for path in self.param['path'].tolist():
        ensure_dir(path)
      File.file_db = File.file_db.append(self.param, sort=False, ignore_index=True)


def print_cfg(cfg):
  for i, row in cfg.iterrows():
    for col, val in row.to_dict().items():
      if isinstance(val, pd.DataFrame):
        print(col, "=\n", val)
      else:
        print(col, "=", val)

def get_file_paths(pdb_row, file_key):
  return pdb_row[file_key]['path'].tolist()


class Task(object):
  @classmethod
  def create_doit_tasks(cls):
    show_details = 1
    if show_details:
      print(f"\n=================== Working on {cls} =============\n")
    if cls is Task:
        return # avoid create tasks from base class 'Task'
    # Build a dictionary from the class variables
    kw = dict((a, getattr(cls, a)) for a in dir(cls) if not a.startswith('_')) 
    # We are interested only in few class variables
    kw = {k:v for k,v in kw.items() if k in ['param', 'mask', 'inputs', 'targets', 'run', 'actions']}
    kw['doc'] = cls.__doc__
    kw['basename'] = cls.__name__ 

    global JUDI_PARAM
    param = kw.pop('param') if 'param' in kw else JUDI_PARAM
    mask = kw.pop('mask') if 'mask' in kw else None
    if mask: param = mask_param_db(param, mask)

    inputs = kw.pop('inputs')
    targets = kw.pop('targets')

    cfg_cols = param.columns.tolist()

    # For each input/target file f create D_{t,f} table
    # and merge the information to the param db
    engroup = lambda x: pd.DataFrame({'dtf':[x.drop(cfg_cols, axis=1)]})
    for files in [inputs, targets]:
      for fkey in files.keys():
        dtf = files[fkey].param.groupby(cfg_cols).apply(engroup).rename(columns={'dtf':fkey})
        dtf.index = dtf.index.droplevel(len(cfg_cols))
        dtf = dtf.reset_index()
        param = param.merge(dtf)

    # add name only after saving the original config columns
    param['name'] = param[cfg_cols].apply(lambda x: get_cfg_str(x), axis='columns')

    for (j, t) in param.iterrows():
      newkw = kw.copy()
      newkw['name'] = t['name'] 
      newkw['targets'] = [p for f in targets.keys() for p in get_file_paths(t, f)]
      newkw['file_dep'] = [p for f in inputs.keys() for p in get_file_paths(t, f)]

      if 'actions' not in newkw:
        #get the name of the arguments of run
        varnames = newkw['run'].__code__.co_varnames[1:] # first variable is 'self' which should be ignored
        newkw['actions'] = [(newkw.pop('run'), [get_file_paths(t, v) for v in varnames])] # TODO: list as argument
      else:
        actions = []
        for (act, args) in newkw['actions']:
          newargs = []
          for arg in args:
            if isinstance(arg, str):
              if arg[0] == '$':
                plist = t[arg[1:]]['path'].tolist()
                newargs.append(plist[0] if len(plist) == 1 else plist)
              elif arg[0] == '#':
                newargs.append(t[arg[1:]])
              else:
                newargs.append(arg)
            else:
              newargs.append(arg)
          if isinstance(act, str):
            for i, v in enumerate(newargs):
              if isinstance(v, list):
                newargs[i] = ' '.join(v)
            newact = act.format(*newargs)
            newargs = []
          else:
            newact = act
          actions += [(newact, newargs) if len(newargs) else (newact)]
        newkw['actions'] = actions
      if show_details:
        print("------------------")
        for key, val in newkw.items():
          print(key, "\t:", val)
      yield newkw


DOIT_CONFIG = {'verbosity': 2}
